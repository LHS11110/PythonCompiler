from Modules import Parser, Lexer
from Modules.Grammer.Expression import Expression, priority
from Modules.Grammer.Container import Container
from Modules.Grammer.Object import Object

input_txt: str = "not"

print(
    Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt)),
    end="\n\n",
)

print(
    Expression.getPreUnaryOp(
        Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt)),
        0,
    ),
    end="\n\n",
)


print(priority)
