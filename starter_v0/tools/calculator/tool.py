from __future__ import annotations

import ast
import operator
from typing import Any

# Allowed operators for safe mathematical evaluation
SAFE_OPERATORS: dict[type[ast.AST], Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node: ast.AST) -> float | int:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
            raise ZeroDivisionError("Division by zero")
        return SAFE_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        operand = _eval_node(node.operand)
        return SAFE_OPERATORS[op_type](operand)
    raise ValueError(f"Unsupported syntax in math expression: {type(node).__name__}")


def calculate(expression: str = "") -> dict[str, Any]:
    """Safely evaluates a basic mathematical expression."""
    if not expression or not expression.strip():
        return {
            "tool": "calculator",
            "expression": "",
            "result": None,
            "error": "expression is required",
        }

    clean_expr = expression.strip().replace(",", "")

    try:
        parsed = ast.parse(clean_expr, mode="eval")
        result = _eval_node(parsed.body)

        # Format float nicely if it is an integer value (e.g. 5.0 -> 5)
        if isinstance(result, float) and result.is_integer():
            formatted = str(int(result))
        elif isinstance(result, float):
            formatted = f"{result:.4f}".rstrip("0").rstrip(".")
        else:
            formatted = str(result)

        return {
            "tool": "calculator",
            "expression": clean_expr,
            "result": result,
            "formatted": formatted,
        }
    except Exception as exc:
        return {
            "tool": "calculator",
            "expression": clean_expr,
            "result": None,
            "error": str(exc),
        }
