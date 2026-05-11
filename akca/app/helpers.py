import os
from collections import deque

class FormattingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def format_table(headers: list, rows: list[tuple | list]) -> str:
    front_padding = 1
    end_padding = 1

    #Find the longest element in each column and adjust width to it
    widths = [len(str(header))+front_padding+end_padding for header in headers]
    for row in rows:
        if len(row) != len(headers):
            raise FormattingError("Wrong number of columns")
        widths = [max(widths[i], len(str(row[i]))+front_padding+end_padding) for i in range(len(row))]

    #Make sure we are still in bounds of the terminal
    size = os.get_terminal_size()
    column_separators_cnt = len(headers)-1
    max_section_width = (size.columns - column_separators_cnt - 2) // len(headers)

    widths = [min(max_section_width, width) for width in widths]

    table_width = column_separators_cnt + sum(widths)
    res = "+" + ("-"*table_width) + "+"

    rows = [headers] + rows

    for i, row in enumerate(rows):
        if i == 1:
            res = "\n".join([res, "+" + ("-"*table_width) + "+"])
        row_str = "|"
        for j in range(len(row)):
            cell = str(row[j])
            if len(cell)+end_padding+front_padding > widths[j]:
                cell = cell[:(widths[j])-5]+"..."
            row_str += front_padding*" " + f"{cell:{widths[j]-1}}|"
        res = "\n".join([res, row_str])

    return "\n".join([res, "+" + ("-"*table_width) + "+"])

def format_tree(nodes: list[dict]) -> str:
    if not nodes:
        return "Nothing to display"

    children: dict[int | None, list[dict]] = {}
    for node in nodes:
        children.setdefault(node["parent_id"], []).append(node)

    lines: list[str] = []

    def render(node: dict, prefix: str, is_last: bool) -> None:
        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + node["name"])
        extension = "    " if is_last else "│   "
        kids = children.get(node["id"], [])
        for i, child in enumerate(kids):
            render(child, prefix + extension, i == len(kids) - 1)

    lines.append(".")
    roots = children.get(None, [])
    for i, root in enumerate(roots):
        render(root, "", i == len(roots) - 1)

    return "\n".join(lines)
