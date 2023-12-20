from scanner import Scanner

if __name__ == '__main__':
    file_path = input("Please enter the file path\n")

    sc = Scanner(file_path)
    tokens = sc.scan()

    print(tokens)
