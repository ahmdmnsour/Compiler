"""Main entry point for the compiler."""

from scanner import Scanner
from parser import Parser
from errors import LexicalError, SyntaxError, FileError


def main():
    """Main function to run the compiler."""
    file_path = "input.txt"

    try:
        try:
            with open(file_path, 'r', encoding='utf-8') as file_reader:
                source_code = file_reader.read()
        except IOError as e:
            raise FileError(f"Cannot open file: {file_path}", 0, 0) from e
        
        sc = Scanner(source_code)
        tokens = sc.scan()
        p = Parser(tokens)
        parsed_code = p.parse()
        
    except FileError as e:
        print(f"File Error: {e}")
    except LexicalError as e:
        print(f"Lexical Error: {e}")
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()
