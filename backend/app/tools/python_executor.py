"""Python Execution Tool — sandboxed pandas/numpy/matplotlib execution."""

import io
import sys
import traceback
from contextlib import redirect_stdout, redirect_stderr

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from app.core.logging_config import get_logger

logger = get_logger(__name__)

# Restricted builtins allowed in sandboxed execution
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "format": format,
    "frozenset": frozenset,
    "int": int,
    "isinstance": isinstance,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "print": print,
    "range": range,
    "reversed": reversed,
    "round": round,
    "set": set,
    "slice": slice,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "type": type,
    "zip": zip,
}


def execute_python_code(
    code: str,
    df: pd.DataFrame,
    chart_save_path: str | None = None,
) -> dict:
    """Execute Python code in a restricted sandbox with access to the dataset.

    The code has access to:
      - ``df``: the uploaded DataFrame
      - ``pd``, ``np``, ``plt``, ``sns``
      - A safe subset of builtins

    The code can store its result in a variable named ``result``.

    Args:
        code: Python code string to execute.
        df: The dataset as a pandas DataFrame.
        chart_save_path: Optional path to save generated charts.

    Returns:
        Dictionary with stdout, stderr, result, and chart_saved flag.
    """
    import seaborn as sns

    logger.info(f"Executing Python code ({len(code)} chars)")

    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    # Build restricted global namespace
    sandbox_globals = {
        "__builtins__": SAFE_BUILTINS,
        "df": df.copy(),
        "pd": pd,
        "np": np,
        "plt": plt,
        "sns": sns,
        "result": None,
    }

    execution_result = {
        "stdout": "",
        "stderr": "",
        "result": None,
        "chart_saved": False,
        "success": False,
    }

    try:
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(code, sandbox_globals)  # noqa: S102

        execution_result["stdout"] = stdout_capture.getvalue()
        execution_result["stderr"] = stderr_capture.getvalue()
        execution_result["success"] = True

        # Capture the result variable
        raw_result = sandbox_globals.get("result")
        if raw_result is not None:
            if isinstance(raw_result, pd.DataFrame):
                execution_result["result"] = raw_result.head(50).to_dict(orient="records")
            elif isinstance(raw_result, pd.Series):
                execution_result["result"] = raw_result.head(50).to_dict()
            elif isinstance(raw_result, (dict, list, int, float, str, bool)):
                execution_result["result"] = raw_result
            else:
                execution_result["result"] = str(raw_result)

        # Save chart if matplotlib figure was created
        if chart_save_path and plt.get_fignums():
            plt.savefig(chart_save_path, bbox_inches="tight", dpi=100)
            execution_result["chart_saved"] = True
            logger.info(f"Chart saved to {chart_save_path}")

    except Exception as e:
        execution_result["stderr"] = f"{type(e).__name__}: {str(e)}"
        execution_result["success"] = False
        logger.warning(f"Code execution failed: {e}")

    finally:
        plt.close("all")
        stdout_capture.close()
        stderr_capture.close()

    return execution_result
