# Compiler Project

A simple compiler implementation in Python that performs lexical analysis (scanning) and syntax analysis (parsing) for a C-like programming language.

## Features

- **Lexical Analysis (Scanner)**: Tokenizes source code into keywords, identifiers, numbers, operators, and special characters
- **Syntax Analysis (Parser)**: Validates the token stream against grammar rules
- **Error Handling**: Comprehensive error reporting with line and column information
- **Comment Support**: Handles both single-line (`//`) and multi-line (`/* */`) comments

## Project Structure

```
Compiler/
├── main.py          # Main entry point
├── scanner.py       # Lexical analyzer
├── parser.py        # Syntax analyzer
├── tokens.py        # Token type definitions and constants
├── errors.py        # Custom exception classes
├── input.txt        # Sample input file
└── README.md        # This file
```

## Language Grammar

The compiler supports the following language features:

### Data Types
- `int` - Integer type

### Keywords
- `const`, `else`, `if`, `int`, `return`, `void`, `while`, `true`, `false`, `for`

### Operators
- Arithmetic: `+`, `-`, `*`, `/`, `%`, `++`, `--`
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`
- Comparison: `==`, `!=`, `<`, `<=`, `>`, `>=`
- Logical: `&&`, `||`, `!`

### Special Characters
- Parentheses: `(`, `)`
- Braces: `{`, `}`
- Brackets: `[`, `]`
- Semicolon: `;`
- Comma: `,`

### Statements
- Function declarations
- Variable declarations
- Assignment statements
- If-else statements
- For loops
- Return statements

## Usage

### Basic Usage

```bash
python main.py
```

The program will read from `input.txt` by default. To use a different file, modify the `file_path` variable in `main.py`.

### Example Input

```c
int main() {
    int x = 10;
    if(x == 3) {
        x = 1;
    }
    else {
        x = 0;
    }
    
    for(int i = 0; i < 10; i++) {
        x++;
    }
    
    return 0;
}
```

### Output

The compiler will output:
1. **Tokens**: List of all tokens found during lexical analysis
2. **Atoms**: Parsed tokens showing the structure of the code
3. **Status**: Whether the code is syntactically correct or any errors encountered

## Error Handling

The compiler provides detailed error messages:

- **FileError**: When a file cannot be opened or read
- **LexicalError**: When an invalid character is encountered during scanning
- **SyntaxError**: When the code doesn't match the expected grammar

All errors include line and column information when available.

## Implementation Details

### Scanner (`scanner.py`)
- Reads source code character by character
- Identifies tokens based on language rules
- Handles whitespace and comments
- Tracks line and column numbers for error reporting

### Parser (`parser.py`)
- Uses recursive descent parsing
- Validates token sequences against grammar rules
- Reports syntax errors with context

### Token Definitions (`tokens.py`)
- Centralized token type constants
- Keyword, operator, and special character mappings
- Helper functions for token identification

### Error Classes (`errors.py`)
- Custom exception hierarchy
- Error messages with location information
- Base class for all compiler errors

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Future Enhancements

Potential improvements for the compiler:

- [ ] Abstract Syntax Tree (AST) generation
- [ ] Semantic analysis (type checking, symbol tables)
- [ ] Code generation (targeting assembly or bytecode)
- [ ] Support for more data types (float, char, string)
- [ ] Function parameters and return types
- [ ] Array support
- [ ] While loops
- [ ] Unit tests
- [ ] Command-line argument parsing
- [ ] Multiple output formats

## License

This is an educational project for learning compiler construction principles.

