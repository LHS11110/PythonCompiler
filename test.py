from Modules import Parser, Lexer
from Modules.Grammer.Expression import Expression, priority
from Modules.Grammer.Container import Container
from Modules.Grammer.Object import Object

input_txt: str = '{123: 123,\n\n                 "asd": 312} \n     asd     \n      '

print(
    Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt)),
    end="\n\n",
)

print(
    Container.getDict(
        Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt)),
        0,
    ),
    end="\n\n",
)
