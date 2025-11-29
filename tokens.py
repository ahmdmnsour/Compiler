"""Token type definitions and constants for the compiler."""

from typing import Dict, Optional


# Token type constants
class TokenType:
    """Token type constants."""
    KEYWORD = "Keyword"
    ID = "ID"
    NUMBER = "Number"
    LPAREN = "LParen"
    RPAREN = "RParen"
    LBRACKET = "LBracket"
    RBRACKET = "RBracket"
    SEMICOLON = "Semicolon"
    COMMA = "Comma"
    LBRACE = "LBrace"
    RBRACE = "RBrace"
    DOUBLE_QUOTES = "DoubleQuotes"
    # Operator token types
    ASSIGN = "Assign"
    ADD_ASSIGN = "AddAssign"
    SUB_ASSIGN = "SubAssign"
    MUL_ASSIGN = "MulAssign"
    DIV_ASSIGN = "DivAssign"
    MOD_ASSIGN = "ModAssign"
    PLUS = "Plus"
    MINUS = "Minus"
    MUL = "Mul"
    DIV = "Div"
    MOD = "Mod"
    INCREASE = "Increase"
    DECREASE = "Decrease"
    LESS = "Less"
    LESSER = "Lesser"
    GREAT = "Great"
    GREATER = "Greater"
    EQUAL = "Equal"
    NOT_EQU = "NotEqu"
    NOT = "Not"
    AND = "And"
    OR = "Or"


# Keyword definitions
KEYWORDS: Dict[str, str] = {
    "const": "Const",
    "else": "Else",
    "if": "If",
    "int": "Int",
    "return": "Return",
    "void": "Void",
    "while": "While",
    "true": "True",
    "false": "False",
    "for": "For"
}


# Special character definitions
SPECIAL_CHARACTERS: Dict[str, str] = {
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,
    ";": TokenType.SEMICOLON,
    ",": TokenType.COMMA,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "\"": TokenType.DOUBLE_QUOTES
}


# Operator definitions
OPERATORS: Dict[str, str] = {
    "!": "Not",
    "!=": "NotEqu",
    "%": "Mod",
    "%=": "ModAssign",
    "&&": "And",
    "||": "Or",
    "*": "Mul",
    "*=": "MulAssign",
    "+": "Plus",
    "++": "Increase",
    "+=": "AddAssign",
    "-": "Minus",
    "--": "Decrease",
    "-=": "SubAssign",
    "/": "Div",
    "/=": "DivAssign",
    "<": "Less",
    "<=": "Lesser",
    "=": "Assign",
    "==": "Equal",
    ">": "Great",
    ">=": "Greater"
}


def is_keyword(token_string: str) -> bool:
    """Check if a string is a keyword."""
    return token_string in KEYWORDS


def get_special_character(token_string: str) -> Optional[str]:
    """Get the token type for a special character, or None if not found."""
    return SPECIAL_CHARACTERS.get(token_string)


def get_operator(token_string: str) -> Optional[str]:
    """Get the token type for an operator, or None if not found."""
    return OPERATORS.get(token_string)

