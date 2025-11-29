"""Lexical analyzer (scanner) for the compiler."""

from typing import List, Tuple, Optional
from tokens import TokenType, KEYWORDS, get_special_character, get_operator
from errors import LexicalError


class Scanner:
    """Scans source code and converts it into tokens."""

    def __init__(self, source_code: str):
        """
        Initialize the scanner with source code.
        
        Args:
            source_code: The source code string to scan
        """
        self.tokens: List[Tuple[str, str]] = []
        self.src: str = source_code
        self.pointer: int = 0
        self.line: int = 1
        self.column: int = 1

    def scan(self) -> List[Tuple[str, str]]:
        """
        Scan the source code and return a list of tokens.
        
        Returns:
            List of tuples containing (token_type, token_value)
            
        Raises:
            LexicalError: If an invalid character is encountered
        """
        while not self.is_eof():
            # Skip whitespace and handle comments
            if self.src[self.pointer].isspace():
                self._handle_whitespace()
                continue
            
            # Check for comments before processing
            if self._handle_comments():
                continue
            
            if self.is_eof():
                break
            
            c = self.src[self.pointer]
            self.pointer += 1
            self.column += 1

            if c.isalpha():
                token = self._scan_identifier_or_keyword(c)
                self.tokens.append(token)
            elif get_special_character(c):
                token_type = get_special_character(c)
                self.tokens.append((token_type, c))
            elif get_operator(c):
                token = self._scan_operator(c)
                self.tokens.append(token)
            elif c.isnumeric():
                token = self._scan_number(c)
                self.tokens.append(token)
            else:
                raise LexicalError(
                    f"Invalid character '{c}'",
                    self.line,
                    self.column - 1
                )

        return self.tokens

    def _scan_identifier_or_keyword(self, first_char: str) -> Tuple[str, str]:
        """Scan an identifier or keyword."""
        token_string = first_char
        
        while not self.is_eof() and (self.src[self.pointer].isalnum() or self.src[self.pointer] == '_'):
            token_string += self.src[self.pointer]
            self.pointer += 1
            self.column += 1
        
        if token_string in KEYWORDS:
            return (TokenType.KEYWORD, token_string)
        else:
            return (TokenType.ID, token_string)

    def _scan_operator(self, first_char: str) -> Tuple[str, str]:
        """Scan an operator (may be single or double character)."""
        if self.is_eof():
            operator_type = get_operator(first_char)
            if operator_type:
                return (operator_type, first_char)
            return (TokenType.ID, first_char)  # Fallback, though this shouldn't happen
        
        # Check for two-character operators
        two_char = first_char + self.src[self.pointer]
        if get_operator(two_char):
            self.pointer += 1
            self.column += 1
            return (get_operator(two_char), two_char)
        
        # Single character operator
        operator_type = get_operator(first_char)
        if operator_type:
            return (operator_type, first_char)
        
        # Should not reach here if called correctly
        return (TokenType.ID, first_char)

    def _scan_number(self, first_char: str) -> Tuple[str, str]:
        """Scan a numeric literal."""
        token_string = first_char
        
        while not self.is_eof() and self.src[self.pointer].isnumeric():
            token_string += self.src[self.pointer]
            self.pointer += 1
            self.column += 1
        
        return (TokenType.NUMBER, token_string)

    def _handle_whitespace(self) -> None:
        """Handle whitespace characters and update line/column tracking."""
        while not self.is_eof() and self.src[self.pointer].isspace():
            if self.src[self.pointer] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pointer += 1

    def _handle_comments(self) -> bool:
        """
        Handle single-line and multi-line comments.
        
        Returns:
            True if a comment was processed, False otherwise
        """
        if self.is_eof() or self.src[self.pointer] != '/':
            return False
        
        if not self._check_bounds(1):
            return False
        
        next_char = self.src[self.pointer + 1]
        
        # Check for single-line comment //
        if next_char == '/':
            # Skip // and rest of line
            self.pointer += 2
            self.column += 2
            while not self.is_eof() and self.src[self.pointer] != '\n':
                self.pointer += 1
                self.column += 1
            
            # Skip the newline
            if not self.is_eof():
                self.pointer += 1
                self.line += 1
                self.column = 1
            return True
        
        # Check for multi-line comment /*
        if next_char == '*':
            # Skip /*
            self.pointer += 2
            self.column += 2
            
            # Find closing */
            while not self.is_eof():
                if self.src[self.pointer] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                
                if (self.src[self.pointer] == '*' and 
                    self._check_bounds(1) and 
                    self.src[self.pointer + 1] == '/'):
                    self.pointer += 2
                    self.column += 2
                    return True
                
                self.pointer += 1
            
            # Reached EOF without closing comment
            raise LexicalError(
                "Unclosed multi-line comment",
                self.line,
                self.column
            )
        
        return False

    def _check_bounds(self, offset: int = 0) -> bool:
        """Check if pointer + offset is within bounds."""
        return (self.pointer + offset) < len(self.src)

    def is_eof(self) -> bool:
        """Check if we've reached the end of the source file."""
        return self.pointer >= len(self.src)
