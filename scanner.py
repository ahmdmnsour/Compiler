from tokene import Token


class State:
    Initial, Dec, Oct, Hex, IDorKeyword, Operator, Zero, PreHex, SingleOperator = range(9)


class Scanner:
    EOF = '\255'
    SPECIAL_CHARS = "!=%&*+-/<>|"
    ID_LENGTH = 12

    def __init__(self, file_path):
        self.src = self.parse_file(file_path)
        self.idx = 0

    def parse_file(self, file_path):
        src = ""
        try:
            with open(file_path, 'r') as file_reader:
                for line in file_reader:
                    src += line + "\n"
                src += self.EOF
        except IOError:
            print("Cannot open file")
        return src

    def is_eof(self):
        return self.idx >= len(self.src)

    def is_special_char(self, c):
        return c in self.SPECIAL_CHARS

    def is_single_special_token(self, c):
        return c in '(){}[],;'

    def get_symbol_type(self, state):
        if state in [State.Dec, State.Oct, State.Hex, State.Zero]:
            return Token.SymbolType.NumericConstant
        elif state == State.IDorKeyword:
            return Token.SymbolType.IDorKeyword
        elif state in [State.Operator, State.SingleOperator]:
            return Token.SymbolType.Operator
        else:
            return Token.SymbolType.NULL

    def except_comment(self):
        while not self.is_eof() and self.src[self.idx].isspace():
            self.idx += 1

        if self.is_eof():
            return False

        if self.src[self.idx] == '/':
            if self.src[self.idx + 1] == '/':
                self.idx += 2
                while not self.is_eof() and self.src[self.idx] != '\n':
                    self.idx += 1
                if not self.is_eof():
                    self.idx += 1
            elif self.src[self.idx + 1] == '*':
                self.idx += 2
                while self.src[self.idx] != '*' and self.src[self.idx + 1] != '/':
                    if self.is_eof():
                        return True
                    self.idx += 1

                self.idx += 2

        return False

    def get_token(self):
        token = Token()
        sym_type = Token.SymbolType.NULL
        token_string = ""
        state = State.Initial

        if self.except_comment():
            print("Invalid Comment")
            return

        while not self.is_eof():
            c = self.src[self.idx]
            self.idx += 1

            if c.isspace():
                if state != State.Initial:
                    break
                else:
                    continue
            elif self.is_single_special_token(c):
                if state == State.Initial:
                    state = State.SingleOperator
                    token_string = c
                else:
                    self.idx -= 1
                break
            elif self.is_special_char(c):
                if state != State.Initial and state != State.Operator:
                    self.idx -= 1
                    break
                state = State.Operator
            elif state == State.Initial and c == '0':
                state = State.Zero
            elif c.isdigit():
                if state == State.Initial:
                    state = State.Dec
                elif state == State.Zero:
                    state = State.Oct
                elif state == State.PreHex:
                    state = State.Hex
                elif state == State.Operator:
                    self.idx -= 1
                    break
            elif state == State.Zero and c == 'x':
                state = State.PreHex
            elif c.isalpha() or c == '_':
                if state != State.Initial and state != State.IDorKeyword:
                    self.idx -= 1
                    break
                state = State.IDorKeyword

            token_string += c

        sym_type = self.get_symbol_type(state)


        token.set_symbol(token_string, sym_type)
        return token
