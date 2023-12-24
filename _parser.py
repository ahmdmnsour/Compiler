class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0

    def parse(self):
        try:
            self.parse_function()
            exit("Code is syntactically correct.")
        except SyntaxError as e:
            print(f"SyntaxError: {e}")

    # check if current_token match ecpected or not , and increment current_index
    def match(self, expected_type):
        if (
            self.current_index < len(self.tokens)
            and self.tokens[self.current_index][0] == expected_type
        ):
            print(self.tokens[self.current_index][1])
            self.current_index += 1
            return True
        else:
            return False

    # according to place of error this function is work, to show what is the error
    def error(self, expected_type):
        exit(f"Expected {expected_type}, got {self.tokens[self.current_index][1]}")

    # check function structure
    # DataType ID () Block
    def parse_function(self):
        if not self.match("Keyword"):
            self.error("Data Type of Function")
        if not self.match("ID"):
            self.error("Name of Function")
        if not self.match("LParen"):
            self.error("(")
        if not self.match("RParen"):
            self.error(")")

        self.parse_block()

    def parse_block(self):
        if not self.match("LBrace"):
            self.error("{")

        while (
            self.tokens[self.current_index][1] == "if"
            or self.tokens[self.current_index][1] == "for"
            or (
                self.tokens[self.current_index][0] == "Keyword"
                and not self.tokens[self.current_index][1] == "return"
            )
            or self.tokens[self.current_index][0] == "ID"
        ):
            self.parse_statement()

        # keyword is return ولا شي غيرها
        if self.tokens[self.current_index][1] == "return":
            self.match("Keyword")
            if not self.match("Number"):
                self.error("Number")
            if not self.match("Semicolon"):
                self.error("Semicolon")

        if not self.match("RBrace"):
            self.error("}")

    def parse_statement(self):
        if (
            self.tokens[self.current_index][0] == "Keyword"
            and self.tokens[self.current_index][1] == "if"
        ):
            self.parse_if_statement()
        elif (
            self.tokens[self.current_index][0] == "Keyword"
            and self.tokens[self.current_index][1] == "for"
        ):
            self.parse_for_loop()
        elif (
            self.tokens[self.current_index][0] == "Keyword"
            and self.tokens[self.current_index][1] == "int"
        ):
            self.parse_declaration()
        elif self.tokens[self.current_index][0] == "ID":
            self.parse_assignment()

    def parse_if_statement(self):
        self.match("Keyword")
        self.match("LParen")
        self.parse_expression()
        self.match("RParen")
        self.parse_block()
        if (
            self.tokens[self.current_index][0] == "Keyword"
            and self.tokens[self.current_index][1] == "else"
        ):
            self.match("Keyword")
            self.parse_block()

    def parse_for_loop(self):
        self.match("Keyword")
        self.match("LParen")
        self.parse_declaration()
        self.parse_expression()
        self.match("Semicolon")
        self.parse_assignment()
        self.match("RParen")
        self.parse_block()

    # function related to check declaration statements
    def parse_declaration(self):
        # int x = y
        if not self.match("Keyword"):
            self.error("Data Type")
        if not self.match("ID"):
            self.error("ID")
        if (
            not self.match("Assign")
            and not self.match("NotEqu")
            and not self.match("AddAssign")
            and not self.match("SubAssign")
            and not self.match("MulAssign")
        ):
            self.error("Assign")
        if not self.match("ID") and not self.match("Number"):
            self.error("ID or Number")

        if self.match("Semicolon"):
            return
        # *4+u;
        while self.tokens[self.current_index][0]!="Semicolon":
                if (
                    not self.match("Plus")
                    and not self.match("Mul")
                    and not self.match("Minus")
                    and not self.match("Div")
                ):
                    self.error("Operator")

                if not self.match("ID") and not self.match("Number"):
                    self.error("ID or Number")

        if not self.match("Semicolon"):
            self.error("Semicolon")

    # check x++ ,x-- ,x=9; , x=8+9;
    def parse_assignment(self):
        if not self.match("ID"):
            self.error("ID")

        if (
            self.tokens[self.current_index][1] == "++"
            or self.tokens[self.current_index][1] == "--"
        ):
            if not self.match("Increase") and not self.match("Decrease"):
                self.error("inc , dec")
            # next=(self.current_index + 1 )
            if self.tokens[self.current_index][1] == ")":
                return
            if not self.match("Semicolon"):
                self.error("Semicolon")
        if self.tokens[self.current_index][1] in ["=", "+=", "-=", "*=", "/="]:
            if (
                not self.match("Assign")
                and not self.match("NotEqu")
                and not self.match("AddAssign")
                and not self.match("SubAssign")
                and not self.match("MulAssign")
            ):
                self.error("Assign")
            if not self.match("ID") and not self.match("Number"):
                self.error("ID or Number")

            if self.match("Semicolon"):
                return
            # *4+u;
            while self.tokens[self.current_index][0]!="Semicolon":
                if (
                    not self.match("Plus")
                    and not self.match("Mul")
                    and not self.match("Minus")
                    and not self.match("Div")
                ):
                    self.error("Operator")

                if not self.match("ID") and not self.match("Number"):
                    self.error("ID or Number")

            if not self.match("Semicolon"):
                self.error("Semicolon")

    # check expression x == > < >= <= y,number
    def parse_expression(self):
        if not self.match("ID") and not self.match("Number"):
            self.error("ID or Number")

        if (
            not self.match("Less")
            and not self.match("Lesser")
            and not self.match("Equal")
            and not self.match("Great")
            and not self.match("Greater")
        ):
            self.error("Operator")

        if not self.match("ID") and not self.match("Number"):
            self.error("ID or Number")
