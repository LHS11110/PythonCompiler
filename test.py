from Modules import Parser, Lexer
from Modules.Grammer.Expression import Expression
from Modules.Grammer.Container import Container
from Modules.Grammer.Object import Object

input_txt: str = '{123: 123, "asd": 312} \n'

print(
    Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt))[
        Container.getDict(
            Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt)),
            0,
        )[1] :
    ],
    end="\n\n",
)

print(
    Container.getDict(
        Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt)),
        0,
    )
)
