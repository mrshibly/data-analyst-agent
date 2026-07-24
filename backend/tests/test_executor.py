"""Unit tests for python executor AST sandbox security."""

import pytest
import pandas as pd
from app.tools.python_executor import execute_python_code, validate_code_ast


def test_ast_sandbox_blocks_import():
    """Importing modules inside execution code should be blocked by AST validation."""
    code = "import os\nos.system('echo hacked')"
    with pytest.raises(PermissionError, match="Module imports are disabled"):
        validate_code_ast(code)


def test_ast_sandbox_blocks_dunder_reflection():
    """Reflection via __subclasses__ should be blocked by AST validation."""
    code = "[c for c in ().__class__.__base__.__subclasses__()]"
    with pytest.raises(PermissionError, match="restricted for security"):
        validate_code_ast(code)


def test_ast_sandbox_blocks_eval_exec():
    """Calling eval or exec dynamically should be blocked."""
    code = "eval('1 + 1')"
    with pytest.raises(PermissionError, match="prohibited in the sandbox"):
        validate_code_ast(code)


def test_valid_pandas_code_executes():
    """Safe pandas computations should execute cleanly."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
    code = "result = df['a'].sum()"
    res = execute_python_code(code, df)
    assert res["success"] is True
    assert int(res["result"]) == 6
