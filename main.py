from parser import Lexer, Parser
from scanner import Scanner

if __name__ == '__main__':
    file_path = input("Please enter the file path\n")

    tokens = []

    sc = Scanner(file_path)
    tok = sc.get_token()

    while tok.get_symbol() != -1:
        tokens.append(tok)
        tok = sc.get_token()
        # Lexer.get_next_token(tok)

    lexer = Lexer(tokens)
    parser = Parser(lexer)
    parsed_code = parser.parse()
    print(parsed_code)

    # for tok in tokens:
    #     print(tok)
