"""Agent Service — orchestrates the AI analysis workflow.

Flow:
  User Query → LLM reasoning → Tool routing → Tool execution
  → Results collected → LLM explanation → Structured response
"""

import json
from typing import Any, AsyncGenerator

import pandas as pd

from app.core.logging_config import get_logger
from app.core.exceptions import AnalysisError
from app.services.llm_service import (
    ANALYSIS_TOOLS,
    build_system_prompt,
    call_llm_with_tools,
    call_llm_for_explanation,
)
from app.services.analysis_service import (
    compute_descriptive_stats,
    compute_correlations,
    compute_groupby_aggregation,
    compute_value_counts,
    detect_null_summary,
)
from app.services.chart_service import create_chart, create_interactive_chart
from app.services.file_service import load_file_as_dataframe, get_file_metadata
from app.tools.python_executor import execute_python_code
from app.tools.file_loader import inspect_dataset
from app.schemas.analysis import AnalysisResponse, ChartInfo, StatisticsInfo

logger = get_logger(__name__)

MAX_TOOL_ITERATIONS = 10


def _format_dataset_info(df: pd.DataFrame, metadata: dict) -> str:
    """Format dataset info for the LLM system prompt with hyper-compression."""
    columns_desc = []
    
    # Sort columns by importance (numeric first, then others)
    input_cols = metadata.get("columns", [])
    
    # Aggressive truncation for 6000 TPM limit
    max_cols = 20
    if len(input_cols) > max_cols:
        logger.warning(f"Dataset has {len(input_cols)} columns. Hyper-truncating schema for LLM context.")
        input_cols = input_cols[:max_cols]
        suffix = f"\n  ...and {len(metadata.get('columns', [])) - max_cols} more columns."
    else:
        suffix = ""

    for col_info in input_cols:
        # Micro-samples to save tokens
        samples = [str(s)[:15] for s in col_info.get('sample_values', [])]
        columns_desc.append(
            f"  - {col_info['name']} ({col_info['dtype']}): samples {samples}"
        )

    header = f"Rows: {metadata['row_count']}, Cols: {metadata['column_count']}\n"
    return header + "Columns:\n" + "\n".join(columns_desc) + suffix


def _execute_tool(
    tool_name: str,
    tool_args: dict,
    df: pd.DataFrame,
    file_id: str,
) -> dict:
    """Execute a single tool and return its result.

    Args:
        tool_name: Name of the tool to execute.
        tool_args: Arguments for the tool.
        df: The dataset DataFrame.
        file_id: File ID for chart storage.

    Returns:
        Dictionary with the tool's output.
    """
    args_summary = list(tool_args.keys()) if isinstance(tool_args, dict) else "None"
    logger.info(f"Executing tool: {tool_name} with args: {args_summary}")

    try:
        if tool_name == "compute_statistics":
            return compute_descriptive_stats(df)

        elif tool_name == "compute_correlations":
            return compute_correlations(df)

        elif tool_name == "group_and_aggregate":
            return compute_groupby_aggregation(
                df,
                group_column=tool_args["group_column"],
                agg_column=tool_args["agg_column"],
                agg_func=tool_args.get("agg_func", "sum"),
            )

        elif tool_name == "value_counts":
            return compute_value_counts(
                df,
                column=tool_args["column"],
                top_n=tool_args.get("top_n", 10),
            )

        elif tool_name == "null_analysis":
            return detect_null_summary(df)

        elif tool_name == "create_chart":
            return create_chart(
                df=df,
                chart_type=tool_args["chart_type"],
                file_id=file_id,
                title=tool_args["title"],
                x=tool_args.get("x"),
                y=tool_args.get("y"),
                column=tool_args.get("column"),
            )

        elif tool_name == "interactive_chart":
            return create_interactive_chart(
                df=df,
                chart_type=tool_args["chart_type"],
                title=tool_args["title"],
                x=tool_args.get("x"),
                y=tool_args.get("y"),
                column=tool_args.get("column"),
            )


        elif tool_name == "run_python_code":
            return execute_python_code(
                code=tool_args["code"],
                df=df,
            )

        else:
            return {"error": f"Unknown tool: {tool_name}"}

    except Exception as e:
        logger.error(f"Tool '{tool_name}' failed: {e}")
        return {"error": f"Tool execution failed: {str(e)}"}


async def run_analysis_stream(
    file_id: str, 
    query: str,
    chat_history: list[dict] | None = None
) -> AsyncGenerator[dict, None]:
    """Run the agent analysis workflow and yield intermediate updates.

    Yields:
        Dictionaries containing event type and data (thought, tool_call, tool_result, final_result).
    """
    logger.info(f"Starting streaming analysis for file {file_id}: '{query[:80]}...'")
    yield {"event": "status", "data": "Loading dataset..."}

    # Load the dataset
    try:
        df = load_file_as_dataframe(file_id)
        metadata = get_file_metadata(file_id)
    except Exception as e:
        yield {"event": "error", "data": {"detail": f"Failed to load dataset: {str(e)}"}}
        return

    dataset_info = _format_dataset_info(df, metadata)
    yield {"event": "status", "data": "Initializing AI agent..."}

    # Build initial messages
    system_prompt = build_system_prompt(dataset_info)
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history for multi-turn (Very limited to save TPM)
    if chat_history:
        messages.extend(chat_history[-4:])  # Last 2 turns
        
    messages.append({"role": "user", "content": query})

    # Iterative tool-calling loop
    tool_results: list[dict] = []
    tool_names_used: list[str] = []
    charts: list[ChartInfo] = []
    statistics_info: StatisticsInfo | None = None

    for iteration in range(MAX_TOOL_ITERATIONS):
        yield {"event": "thought", "data": f"Reasoning (Iteration {iteration + 1})..."}
        
        response_message = call_llm_with_tools(messages, tools=ANALYSIS_TOOLS)
        tool_calls = getattr(response_message, "tool_calls", None)

        if not tool_calls:
            yield {"event": "status", "data": "Analysis complete. Generating explanation..."}
            break

        # Log reasoning content if available
        if response_message.content:
            yield {"event": "thought", "data": response_message.content}

        # Add the assistant message with tool calls
        messages.append({
            "role": "assistant",
            "content": response_message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in tool_calls
            ],
        })

        # Execute each tool call
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            yield {"event": "status", "data": f"Executing tool: {tool_name.replace('_', ' ').capitalize()}..."}
            
            try:
                args_str = tool_call.function.arguments
                tool_args = json.loads(args_str) if args_str else {}
                if not isinstance(tool_args, dict):
                    tool_args = {}
            except json.JSONDecodeError:
                tool_args = {}

            result = _execute_tool(tool_name, tool_args, df, file_id)
            tool_names_used.append(tool_name)
            tool_results.append({"tool": tool_name, "args": tool_args, "result": result})

            # Track charts (standard)
            if tool_name == "create_chart" and "url" in result:
                chart = ChartInfo(
                    title=result.get("title", "Chart"),
                    url=result["url"],
                    chart_type=result.get("chart_type", ""),
                )
                charts.append(chart)
                yield {"event": "chart", "data": chart.model_dump()}

            # Track interactive charts
            if (tool_name == "interactive_chart" or result.get("is_interactive")) and "plotly_data" in result:
                chart = ChartInfo(
                    title=result.get("title", "Interactive Chart"),
                    plotly_data=result["plotly_data"],
                    chart_type=result.get("chart_type", ""),
                    is_interactive=True
                )
                charts.append(chart)
                yield {"event": "chart", "data": chart.model_dump()}

            # Track statistics
            if tool_name == "compute_statistics" and "descriptive" in result:
                numeric_cols = list(result["descriptive"].keys())
                statistics_info = StatisticsInfo(
                    row_count=int(metadata["row_count"]),
                    column_count=int(metadata["column_count"]),
                    numeric_columns=numeric_cols,
                    descriptive_stats=result["descriptive"],
                )
                yield {"event": "statistics", "data": statistics_info.model_dump()}

            # Add tool result message (Optimized for Groq TPM)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, default=str)[:1200],
            })

    # Generate final explanation
    try:
        explanation = call_llm_for_explanation(
            user_query=query, 
            dataset_info=dataset_info, 
            tool_results=tool_results,
            chat_history=chat_history
        )
    except Exception as e:
        explanation = "Analysis completed. See the results above for details."

    summary, insights = _parse_explanation(explanation)

    if not statistics_info:
        inspect_data = inspect_dataset(df)
        statistics_info = StatisticsInfo(
            row_count=metadata["row_count"],
            column_count=metadata["column_count"],
            numeric_columns=inspect_data.get("numeric_columns", []),
            categorical_columns=inspect_data.get("categorical_columns", []),
        )

    response = AnalysisResponse(
        summary=summary,
        insights=insights,
        statistics=statistics_info,
        charts=charts,
        data_preview=[],
        tool_calls=list(set(tool_names_used)),
    )
    
    yield {"event": "final_result", "data": response.model_dump()}


async def run_analysis(file_id: str, query: str, chat_history: list[dict] | None = None) -> AnalysisResponse:
    """Run the complete agent analysis workflow and return the final result."""
    final_response = None
    async for update in run_analysis_stream(file_id, query, chat_history):
        if update["event"] == "final_result":
            final_response = AnalysisResponse(**update["data"])
        elif update["event"] == "error":
            raise AnalysisError(update["data"])
    
    if not final_response:
        raise AnalysisError("Analysis failed to produce a final result.")
    
    return final_response


import re

def _parse_explanation(explanation: str) -> tuple[str, list[str]]:
    """Parse the LLM explanation using robust regex to handle bolding and whitespace."""
    summary = ""
    insights = []
    
    # Normalize markdown bolding and common patterns for robust splitting
    # Matches 'Summary:', '**Summary:**', '### Summary', etc.
    summary_pattern = re.compile(r"(?i)(?:\**\s*Summary\s*:?\s*\**)")
    insights_pattern = re.compile(r"(?i)(?:\**\s*Insights\s*:?\s*\**)")
    
    # Find positions
    s_match = summary_pattern.search(explanation)
    i_match = insights_pattern.search(explanation)
    
    if i_match:
        # We have an insights header
        i_pos = i_match.start()
        
        # Extract summary text
        if s_match and s_match.start() < i_pos:
            summary_text = explanation[s_match.end():i_pos].strip()
        else:
            summary_text = explanation[:i_pos].strip()
            
        summary = summary_text
        
        # Extract insights from after the header
        insights_text = explanation[i_match.end():].strip()
        for line in insights_text.split("\n"):
            line = line.strip()
            if not line: continue
            # Handle list markers
            if line.startswith(("- ", "• ", "* ", "– ")) or (line[:1].isdigit() and "." in line[:3]):
                insight = line.lstrip("-•*– 1234567890. ").strip()
                if insight: insights.append(insight)
    else:
        # Fallback: Treat start as summary, look for bullets anywhere
        lines = explanation.strip().split("\n")
        summary_parts = []
        in_insights = False

        for line in lines:
            stripped = line.strip()
            if not stripped: continue
            if stripped.startswith(("- ", "• ", "* ", "– ")) or (stripped[:1].isdigit() and "." in stripped[:3]):
                in_insights = True
                insight = stripped.lstrip("-•*– 1234567890. ").strip()
                if insight: insights.append(insight)
            elif not in_insights:
                # Clean header if it leaked in
                clean_line = summary_pattern.sub("", stripped).strip()
                if clean_line: summary_parts.append(clean_line)
        
        summary = " ".join(summary_parts) if summary_parts else explanation[:500]

    return summary, insights
