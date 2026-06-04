import ast
from typing import List

def process(data: str) -> List:
    try:
        return ast.literal_eval(data)
    except (ValueError, SyntaxError):
        return []