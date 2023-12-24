from scanner import Scanner
from _parser import Parser

if __name__ == '__main__':
    
    #file_path = input("Please enter the file path\n")
    file_path="input.txt"

    sc = Scanner(file_path)
    tokens = sc.scan()
    print("---------------Tokens---------------")
    print(tokens)

    p=Parser(tokens)
    parsed_code = p.parse()
    print("---------------Atoms---------------")
    print(parsed_code)
