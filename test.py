from Modules import Parser, Lexer

with open("test.py", "r") as file:
    print(Parser.Parser().clean(Lexer.Lexer().tokenize(file.read())))
