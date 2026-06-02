import ast
import json
import os


class VulnerableFunctionFinder(ast.NodeVisitor):
    """
    Localiza la función que contiene la línea vulnerable
    reportada por Bandit.
    """

    def __init__(self, target_line):
        self.target_line = target_line
        self.target_node = None

    def visit_FunctionDef(self, node):

        if (
            hasattr(node, "lineno")
            and hasattr(node, "end_lineno")
        ):
            if node.lineno <= self.target_line <= node.end_lineno:
                self.target_node = node

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):

        if (
            hasattr(node, "lineno")
            and hasattr(node, "end_lineno")
        ):
            if node.lineno <= self.target_line <= node.end_lineno:
                self.target_node = node

        self.generic_visit(node)


def prune_vulnerable_context(report_path):

    if not os.path.exists(report_path):
        return None, None, 0

    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    if not report["results"]:
        return None, None, 0

    issue = report["results"][0]

    file_path = issue["filename"]
    target_line = issue["line_number"]

    # Resolver ruta absoluta
    base_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(report_path),
            "..",
            ".."
        )
    )

    full_path = (
        os.path.join(base_dir, file_path)
        if not os.path.isabs(file_path)
        else file_path
    )

    with open(full_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    # Parseo AST
    tree = ast.parse(source_code)

    finder = VulnerableFunctionFinder(target_line)
    finder.visit(tree)

    if finder.target_node is None:

        # Fallback por líneas
        lines = source_code.splitlines()

        start = max(0, target_line - 5)
        end = min(len(lines), target_line + 5)

        context = "\n".join(lines[start:end])

    else:

        lines = source_code.splitlines()

        start = finder.target_node.lineno - 1
        end = finder.target_node.end_lineno

        context = "\n".join(lines[start:end])

    size_original = len(source_code)
    size_contexto = len(context)

    ahorro = round(
        (1 - (size_contexto / size_original)) * 100,
        1
    ) if size_original > 0 else 0

    return context, issue, ahorro
