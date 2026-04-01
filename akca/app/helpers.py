class FormattingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

def format_table(headers: list, rows: list[tuple]) -> str:
    pass