import ast
import operator as op
from langchain_core.tools import tool

_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}

def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_eval(node.operand))
    raise ValueError("Chỉ hỗ trợ số và toán tử + - * / % **")

@tool
def calculator(expression: str) -> str:
    """Tính toán biểu thức số học an toàn, dùng cho điểm xét tuyển, tổng điểm, học phí."""
    try:
        tree = ast.parse(expression, mode="eval")
        value = _eval(tree.body)
        return f"Kết quả tính toán: {value}"
    except Exception as exc:
        return f"Không tính được: {exc}"
