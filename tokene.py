from enum import Enum


class Token:

    class SymbolType(Enum):
        Operator, IDorKeyword, NumericConstant, SpecialCharacter,  NULL = range(5)

    class TokenSymbol(Enum):
        NULL, Not, NotEqu, Mod, ModAssign, ID, Keyword, Number, And, LParen, RParen, Mul, MulAssign, Plus, Increase, AddAssign, Comma, Minus, Decrease, SubAssign, Div, DivAssign, Semicolon, Less, Lesser, Assign, Equal, Great, Greater, LBracket, RBracket, EOF, Const, Else, If, Int, Return, Void, While, LBrace, Or, RBrace, include = range(43)

    def __init__(self):
        self.symbol = self.TokenSymbol.NULL
        self.val = "0"
        self.token_string = "NULL"

    def get_id_or_keyword_symbol(self, token):
        keywords = {
            "const": self.TokenSymbol.Const,
            "else": self.TokenSymbol.Else,
            "if": self.TokenSymbol.If,
            "int": self.TokenSymbol.Int,
            "return": self.TokenSymbol.Return,
            "void": self.TokenSymbol.Void,
            "while": self.TokenSymbol.While,
            "#include": self.TokenSymbol.include
        }
        if token in keywords:
            return self.TokenSymbol.Keyword
        else: return self.TokenSymbol.ID

    def get_operator_symbol(self, token):
        operators = {
            "!": self.TokenSymbol.Not,
            "!=": self.TokenSymbol.NotEqu,
            "%": self.TokenSymbol.Mod,
            "%=": self.TokenSymbol.ModAssign,
            "&&": self.TokenSymbol.And,
            "(": self.TokenSymbol.LParen,
            ")": self.TokenSymbol.RParen,
            "*": self.TokenSymbol.Mul,
            "*=": self.TokenSymbol.MulAssign,
            "+": self.TokenSymbol.Plus,
            "++": self.TokenSymbol.Increase,
            "+=": self.TokenSymbol.AddAssign,
            ",": self.TokenSymbol.Comma,
            "-": self.TokenSymbol.Minus,
            "--": self.TokenSymbol.Decrease,
            "-=": self.TokenSymbol.SubAssign,
            "/": self.TokenSymbol.Div,
            "/=": self.TokenSymbol.DivAssign,
            ";": self.TokenSymbol.Semicolon,
            "<": self.TokenSymbol.Less,
            "<=": self.TokenSymbol.Lesser,
            "=": self.TokenSymbol.Assign,
            "==": self.TokenSymbol.Equal,
            ">": self.TokenSymbol.Great,
            ">=": self.TokenSymbol.Greater,
            "[": self.TokenSymbol.LBracket,
            "]": self.TokenSymbol.RBracket,
            "\255": self.TokenSymbol.EOF,
            "{": self.TokenSymbol.LBrace,
            "||": self.TokenSymbol.Or,
            "}": self.TokenSymbol.RBrace
        }
        return operators.get(token, self.TokenSymbol.NULL)

    def set_symbol(self, token, type):
        self.token_string = token
        if type == self.SymbolType.IDorKeyword:
            self.symbol = self.get_id_or_keyword_symbol(token)
            if self.symbol == self.TokenSymbol.ID or self.symbol == self.TokenSymbol.Keyword:
                self.val = token
        elif type == self.SymbolType.NumericConstant:
            self.symbol = self.TokenSymbol.Number
            self.val = str(self.parse_int(token))
        elif type == self.SymbolType.Operator:
            self.symbol = self.get_operator_symbol(token)

    def parse_int(self, s):
        radix = 10
        if s.startswith("0x"):
            radix = 16
            s = s[2:]
        elif s.startswith("0") and len(s) > 1:
            radix = 8
        return int(s, radix)

    def get_symbol(self):
        return self.symbol.value - 1

    def __str__(self):
        return f"{self.token_string}: {self.symbol.name}"


