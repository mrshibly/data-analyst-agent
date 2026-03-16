"""LLM Service — isolated LLM client supporting Groq and OpenAI with function calling."""

import json
from typing import Any

from app.core.config import settings
from app.core.exceptions import LLMError
from app.core.logging_config import get_logger

logger = get_logger(__name__)

# Tool definitions for function calling
ANALYSIS_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "compute_statistics",
            "description": "Compute descriptive statistics (mean, median, std, min, max, etc.) for all numeric columns in the dataset.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compute_correlations",
            "description": "Compute pairwise correlation matrix for all numeric columns. Use this to find relationships between variables.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "group_and_aggregate",
            "description": "Group the data by a categorical column and compute an aggregate (sum, mean, count, min, max, median) of a numeric column.",
            "parameters": {
                "type": "object",
                "properties": {
                    "group_column": {
                        "type": "string",
                        "description": "Column to group by (usually categorical).",
                    },
                    "agg_column": {
                        "type": "string",
                        "description": "Column to aggregate (usually numeric).",
                    },
                    "agg_func": {
                        "type": "string",
                        "enum": ["sum", "mean", "count", "min", "max", "median"],
                        "description": "Aggregation function to apply.",
                    },
                },
                "required": ["group_column", "agg_column", "agg_func"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "value_counts",
            "description": "Get the count of each unique value in a column. Useful for finding top categories, distributions, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "Column to count values for.",
                    },
                    "top_n": {
                        "type": "integer",
                        "description": "Number of top values to return.",
                        "default": 10,
                    },
                },
                "required": ["column"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "null_analysis",
            "description": "Analyze null/missing values across all columns in the dataset.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_chart",
            "description": "Generate a chart/visualization. Supported types: line, bar, histogram, scatter, heatmap.",
            "parameters": {
                "type": "object",
                "properties": {
                    "chart_type": {
                        "type": "string",
                        "enum": ["line", "bar", "histogram", "scatter", "heatmap"],
                        "description": "Type of chart to create.",
                    },
                    "title": {
                        "type": "string",
                        "description": "Title for the chart.",
                    },
                    "x": {
                        "type": "string",
                        "description": "Column for x-axis (for line, bar, scatter charts).",
                    },
                    "y": {
                        "type": "string",
                        "description": "Column for y-axis (for line, bar, scatter charts).",
                    },
                    "column": {
                        "type": "string",
                        "description": "Column to plot (for histogram).",
                    },
                },
                "required": ["chart_type", "title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "interactive_chart",
            "description": "Generate an interactive Plotly chart. Use this for superior user experience allowing hover, zoom, and pan. Supported types: line, bar, histogram, scatter, pie, box.",
            "parameters": {
                "type": "object",
                "properties": {
                    "chart_type": {
                        "type": "string",
                        "enum": ["line", "bar", "histogram", "scatter", "pie", "box"],
                        "description": "Type of interactive chart to create.",
                    },
                    "title": {
                        "type": "string",
                        "description": "Title for the chart.",
                    },
                    "x": {
                        "type": "string",
                        "description": "Column for x-axis (for line, bar, scatter charts).",
                    },
                    "y": {
                        "type": "string",
                        "description": "Column for y-axis (for line, bar, scatter, box charts).",
                    },
                    "column": {
                        "type": "string",
                        "description": "Column to plot (for histogram, pie, or box charts).",
                    },
                },
                "required": ["chart_type", "title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_python_code",
            "description": "Execute custom Python code for advanced analysis. The code has access to 'df' (the dataset as a pandas DataFrame), 'pd', 'np', 'plt', and 'sns'. Store the result in a variable called 'result'. Use this for complex operations like filtering, custom calculations, pivot tables, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute. Access the dataset via 'df'. Store output in 'result'.",
                    },
                },
                "required": ["code"],
            },
        },
    },
]


def _get_client_and_model() -> tuple[Any, str]:
    """Get the appropriate LLM client and model name."""
    provider = settings.llm_provider.lower()

    if provider == "groq":
        from groq import Groq
        if not settings.groq_api_key:
            raise LLMError("GROQ_API_KEY not configured")
        client = Groq(api_key=settings.groq_api_key)
        return client, settings.groq_model

    elif provider == "openai":
        from openai import OpenAI
        if not settings.openai_api_key:
            raise LLMError("OPENAI_API_KEY not configured")
        client = OpenAI(api_key=settings.openai_api_key)
        return client, settings.openai_model

    else:
        raise LLMError(f"Unsupported LLM provider: {provider}")


def build_system_prompt(dataset_info: str) -> str:
    """Build a token-optimized system prompt."""
    return f"""You are a data analyst. Data structure:
{dataset_info}

Guidelines:
1. Use tools for numbers/charts (prefer interactive_chart).
2. For distributions: histogram/box. 
3. For comparisons: bar/line/pie.
4. For complex logic: run_python_code.
5. Be concise and specific."""


def call_llm_with_tools(
    messages: list[dict],
    tools: list[dict] | None = None,
) -> dict:
    """Make an LLM API call with optional function calling.

    Args:
        messages: List of message dictionaries.
        tools: Optional list of tool definitions.

    Returns:
        The LLM response message.
    """
    client, model = _get_client_and_model()

    try:
        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 4096,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message

    except Exception as e:
        logger.error(f"LLM API call failed: {e}")
        raise LLMError(str(e))


def call_llm_for_explanation(
    user_query: str,
    dataset_info: str,
    tool_results: list[dict],
    chat_history: list[dict] | None = None,
) -> str:
    """Call LLM to generate a final explanation of the analysis results.

    Args:
        user_query: The original user question.
        dataset_info: String description of the dataset schema.
        tool_results: List of tool execution results.
        chat_history: Optional conversation history.

    Returns:
        Natural language explanation string.
    """
    # Minify JSON and truncate to save TPM
    results_text = json.dumps(tool_results, default=str)[:1500]
    
    system_content = (
        "You are a data analyst. Output format MUST be followed EXACTLY.\n"
        "Example:\n"
        "Summary: The dataset consists of 891 entries. Analysis shows high variance in fares.\n\n"
        "Insights:\n"
        "- Average age is 29.7 years.\n"
        "- 38% of passengers survived.\n\n"
        "Constraint: Never use markdown bold (**) for Summary or Insights labels."
    )

    messages = [{"role": "system", "content": system_content}]
    
    # Very limited history for explanation phase
    if chat_history:
        messages.extend(chat_history[-2:])  # Last 1 turn
        
    messages.append({
        "role": "user",
        "content": f"Data: {dataset_info[:500]}\nQuery: {user_query}\nResults: {results_text}",
    })

    response = call_llm_with_tools(messages, tools=None)
    return response.content or "Analysis completed but no explanation was generated."
