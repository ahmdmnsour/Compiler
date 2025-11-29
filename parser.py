"""Parser for the compiler - builds parse tree from tokens."""

from typing import List, Tuple, Optional
from tokens import TokenType
from errors import SyntaxError as ParserSyntaxError


class Parser:
    """Parses tokens according to the grammar rules."""

    def __init__(self, tokens: List[Tuple[str, str]]):
        """
        Initialize the parser with a list of tokens.
        
        Args:
            tokens: List of (token_type, token_value) tuples
        """
        self.tokens: List[Tuple[str, str]] = tokens
        self.current_index: int = 0

    def parse(self) -> None:
        """
        Parse the tokens according to the grammar.
        
        Raises:
            SyntaxError: If a syntax error is encountered
        """
        try:
            while self.current_index < len(self.tokens):
                self.parse_function()
            print("Code is syntactically correct.")
        except ParserSyntaxError as e:
            print(f"SyntaxError: {e}")
            raise

    def match(self, expected_type: str) -> bool:
        """
        Check if current token matches expected type and advance if it does.
        
        Args:
            expected_type: The expected token type
            
        Returns:
            True if match, False otherwise
        """
        if (self.current_index < len(self.tokens) and
                self.tokens[self.current_index][0] == expected_type):
            print(self.tokens[self.current_index][1])
            self.current_index += 1
            return True
        return False

    def error(self, expected_type: str) -> None:
        """
        Raise a syntax error with context information.
        
        Args:
            expected_type: The expected token type
            
        Raises:
            SyntaxError: Always raises this exception
        """
        if self.current_index < len(self.tokens):
            got = self.tokens[self.current_index][1]
            raise ParserSyntaxError(f"Expected {expected_type}, got '{got}'")
        else:
            raise ParserSyntaxError(f"Expected {expected_type}, but reached end of file")

    def parse_function(self) -> None:
        """
        Parse a function declaration.
        Grammar: DataType ID ( ) Block
        """
        if not self.match(TokenType.KEYWORD):
            self.error("Data Type of Function")
        if not self.match(TokenType.ID):
            self.error("Name of Function")
        if not self.match(TokenType.LPAREN):
            self.error("(")
        if not self.match(TokenType.RPAREN):
            self.error(")")

        self.parse_block()

    def parse_block(self) -> None:
        """
        Parse a block of statements.
        Grammar: { Statement* ReturnStatement? }
        """
        if not self.match(TokenType.LBRACE):
            self.error("{")

        # Parse statements while we have if, for, declarations, or assignments
        while (self.current_index < len(self.tokens) and
               (self._is_token("if") or
                self._is_token("for") or
                (self.tokens[self.current_index][0] == TokenType.KEYWORD and
                 not self._is_token("return")) or
                self.tokens[self.current_index][0] == TokenType.ID)):
            self.parse_statement()

        # Parse return statement if present
        if (self.current_index < len(self.tokens) and
                self._is_token("return")):
            self.match(TokenType.KEYWORD)
            if not self.match(TokenType.NUMBER):
                self.error("Number")
            if not self.match(TokenType.SEMICOLON):
                self.error("Semicolon")

        if not self.match(TokenType.RBRACE):
            self.error("}")

    def parse_statement(self) -> None:
        """Parse a statement (if, for, declaration, or assignment)."""
        if self.current_index >= len(self.tokens):
            return
        
        if self._is_token("if"):
            self.parse_if_statement()
        elif self._is_token("for"):
            self.parse_for_loop()
        elif (self.tokens[self.current_index][0] == TokenType.KEYWORD and
              self._is_token("int")):
            self.parse_declaration()
        elif self.tokens[self.current_index][0] == TokenType.ID:
            self.parse_assignment()

    def parse_if_statement(self) -> None:
        """
        Parse an if statement.
        Grammar: if ( Expression ) Block [else Block]
        """
        self.match(TokenType.KEYWORD)
        self.match(TokenType.LPAREN)
        self.parse_expression()
        self.match(TokenType.RPAREN)
        self.parse_block()
        
        # Optional else clause
        if (self.current_index < len(self.tokens) and
                self._is_token("else")):
            self.match(TokenType.KEYWORD)
            self.parse_block()

    def parse_for_loop(self) -> None:
        """
        Parse a for loop.
        Grammar: for ( Declaration Expression ; Assignment ) Block
        """
        self.match(TokenType.KEYWORD)
        self.match(TokenType.LPAREN)
        self.parse_declaration()
        self.parse_expression()
        self.match(TokenType.SEMICOLON)
        self.parse_assignment()
        self.match(TokenType.RPAREN)
        self.parse_block()

    def parse_declaration(self) -> None:
        """
        Parse a variable declaration.
        Grammar: int ID [= Expression] ;
        """
        if not self.match(TokenType.KEYWORD):
            self.error("Data Type")
        if not self.match(TokenType.ID):
            self.error("ID")
        
        # Optional assignment
        if (self.current_index < len(self.tokens) and
                self._is_assign_operator()):
            if not (self.match(TokenType.ASSIGN) or
                    self.match(TokenType.ADD_ASSIGN) or
                    self.match(TokenType.SUB_ASSIGN) or
                    self.match(TokenType.MUL_ASSIGN) or
                    self.match(TokenType.DIV_ASSIGN)):
                self.error("Assignment operator")
            
            if not (self.match(TokenType.ID) or self.match(TokenType.NUMBER)):
                self.error("ID or Number")
            
            # Parse additional expression terms
            while (self.current_index < len(self.tokens) and
                   self.tokens[self.current_index][0] != TokenType.SEMICOLON):
                if not (self.match("Plus") or
                        self.match("Mul") or
                        self.match("Minus") or
                        self.match("Div")):
                    self.error("Operator")

                if not (self.match(TokenType.ID) or self.match(TokenType.NUMBER)):
                    self.error("ID or Number")

        if not self.match(TokenType.SEMICOLON):
            self.error("Semicolon")

    def parse_assignment(self) -> None:
        """
        Parse an assignment statement.
        Grammar: ID [++|--] | ID [= | += | -= | *= | /=] Expression ;
        """
        if not self.match(TokenType.ID):
            self.error("ID")

        if self.current_index >= len(self.tokens):
            self.error("Semicolon or operator")

        # Handle increment/decrement operators (x++ or x--)
        if self._is_token("++") or self._is_token("--"):
            if not (self.match(TokenType.INCREASE) or self.match(TokenType.DECREASE)):
                self.error("Increment or decrement operator")
            
            # Check if we're in a for loop (next token might be )
            if (self.current_index < len(self.tokens) and
                    self._is_token(")")):
                return
            
            if not self.match(TokenType.SEMICOLON):
                self.error("Semicolon")
            return

        # Handle assignment operators (=, +=, -=, *=, /=)
        if self._is_assign_operator():
            if not (self.match(TokenType.ASSIGN) or
                    self.match(TokenType.ADD_ASSIGN) or
                    self.match(TokenType.SUB_ASSIGN) or
                    self.match(TokenType.MUL_ASSIGN) or
                    self.match(TokenType.DIV_ASSIGN)):
                self.error("Assignment operator")
            
            if not (self.match(TokenType.ID) or self.match(TokenType.NUMBER)):
                self.error("ID or Number")

            # Parse additional expression terms
            while (self.current_index < len(self.tokens) and
                   self.tokens[self.current_index][0] != TokenType.SEMICOLON):
                if not (self.match(TokenType.PLUS) or
                        self.match(TokenType.MUL) or
                        self.match(TokenType.MINUS) or
                        self.match(TokenType.DIV)):
                    self.error("Operator")

                if not (self.match(TokenType.ID) or self.match(TokenType.NUMBER)):
                    self.error("ID or Number")

            if not self.match(TokenType.SEMICOLON):
                self.error("Semicolon")

    def parse_expression(self) -> None:
        """
        Parse a comparison expression.
        Grammar: (ID | Number) ComparisonOperator (ID | Number)
        """
        if not (self.match(TokenType.ID) or self.match(TokenType.NUMBER)):
            self.error("ID or Number")

        if not (self.match(TokenType.LESS) or
                self.match(TokenType.LESSER) or
                self.match(TokenType.EQUAL) or
                self.match(TokenType.GREAT) or
                self.match(TokenType.GREATER) or
                self.match(TokenType.NOT_EQU)):
            self.error("Comparison operator")

        if not (self.match(TokenType.ID) or self.match(TokenType.NUMBER)):
            self.error("ID or Number")

    def _is_token(self, value: str) -> bool:
        """Check if current token has the given value."""
        return (self.current_index < len(self.tokens) and
                self.tokens[self.current_index][1] == value)

    def _is_assign_operator(self) -> bool:
        """Check if current token is an assignment operator."""
        if self.current_index >= len(self.tokens):
            return False
        token_value = self.tokens[self.current_index][1]
        return token_value in ["=", "+=", "-=", "*=", "/=", "%="]

