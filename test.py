from Modules.Parser import Parser
from Modules.Lexer import Lexer
from Modules.Parser import Parser
from Modules.Parser import Container
from Modules.Parser import Object
from Modules.Parser import Expression
from Modules.Parser.Expression import priority

input_txt: str = "- not -asd.a[::]() ** (4 + 2) if True else 123\n"

print(
    Parser.cleanup(Lexer.tokenize(input_text=input_txt)),
    end="\n\n",
)

print(
    Expression.getExpr(
        Parser.cleanup(Lexer.tokenize(input_text=input_txt)),
        0,
    ),
    end="\n\n",
)

print(
    Parser.cleanup(Lexer.tokenize(input_text=input_txt))[
        Expression.getExpr(
            Parser.cleanup(Lexer.tokenize(input_text=input_txt)),
            0,
        )[1] :
    ],
    end="\n\n",
)
