"""Custom exception classes for the compiler."""


class CompilerError(Exception):
    """Base exception for all compiler errors."""
    
    def __init__(self, message: str, line: int = None, column: int = None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.line is not None and self.column is not None:
            return f"Line {self.line}, Column {self.column}: {self.message}"
        elif self.line is not None:
            return f"Line {self.line}: {self.message}"
        return self.message


class LexicalError(CompilerError):
    """Raised when a lexical error is encountered during scanning."""
    pass


class SyntaxError(CompilerError):
    """Raised when a syntax error is encountered during parsing."""
    pass


class FileError(CompilerError):
    """Raised when there's an error reading or opening a file."""
    pass

