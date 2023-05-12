from Modules.Parser import Parser
from Modules.Lexer import Lexer
from Modules.Parser.Expression import Expression, priority
from Modules.Parser.Container import Container
from Modules.Parser.Object import Object

input_txt: str = "+"

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
