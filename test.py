from Modules import Parser, Lexer
from Modules.Grammer import Expression
from Modules.Grammer import Container
from Modules.Grammer import Object

input_txt: str = "[123::] \n"

print(
    Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt))[
        Expression.Expression.getAnotherOp(
            Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt)),
            0,
        )[1] :
    ],
    end="\n\n",
)

print(
    Expression.Expression.getAnotherOp(
        Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt)),
        0,
    )
)
