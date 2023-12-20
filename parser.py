from tokene import Token


class Lexer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_position = 0

    def get_next_token(self):
        tok = self.tokens[self.current_position]
        self.current_position += 1
        print(tok)
        return tok


class ParseTreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, expected_type):
        if self.current_token.symbol == expected_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError(f"Expected {expected_type}, found {self.current_token.symbol}")

    # ... Other methods ...

    def parse_factor(self):
        token = self.current_token
        if token.symbol == Token.TokenSymbol.Number:
            self.eat(Token.TokenSymbol.Number)
            return ParseTreeNode(token.val)
        elif token.symbol == Token.TokenSymbol.LParen:
            self.eat(Token.TokenSymbol.LParen)
            result = self.parse_expression()
            self.eat(Token.TokenSymbol.RParen)
            return ParseTreeNode("(", [result])
        else:
            raise SyntaxError("Unexpected token in factor")

    def parse_term(self):
        result = self.parse_factor()

        while self.current_token.symbol in [Token.TokenSymbol.Mul, Token.TokenSymbol.Div]:
            token = self.current_token
            if token.symbol == Token.TokenSymbol.Mul:
                self.eat(Token.TokenSymbol.Mul)
                result = ParseTreeNode("*", [result, self.parse_factor()])
            elif token.symbol == Token.TokenSymbol.Div:
                self.eat(Token.TokenSymbol.Div)
                divisor = self.parse_factor()
                if divisor == 0:
                    raise ValueError("Division by zero")
                result = ParseTreeNode("/", [result, divisor])

        return result

    def parse_expression(self):
        result = self.parse_term()

        while self.current_token.symbol in [Token.TokenSymbol.Plus, Token.TokenSymbol.Minus]:
            token = self.current_token
            if token.symbol == Token.TokenSymbol.Plus:
                self.eat(Token.TokenSymbol.Plus)
                result = ParseTreeNode("+", [result, self.parse_term()])
            elif token.symbol == Token.TokenSymbol.Minus:
                self.eat(Token.TokenSymbol.Minus)
                result = ParseTreeNode("-", [result, self.parse_term()])

        return result

    def parse_statement(self):
        if self.current_token.symbol == Token.TokenSymbol.ID:
            variable_name = self.current_token.val
            self.eat(Token.TokenSymbol.ID)
            self.eat(Token.TokenSymbol.Assign)
            expression_result = self.parse_expression()
            return ParseTreeNode("=", [ParseTreeNode(variable_name), expression_result])
        else:
            raise SyntaxError("Invalid statement")

    def parse(self):
        return self.parse_statement()
