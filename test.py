from Modules.Parser import Parser
from Modules.Lexer import Lexer
from Modules.Parser import Parser
from Modules.Parser import Container
from Modules.Parser import Object
from Modules.Parser import Expression
from Modules.Parser.Expression import priority

input_txt: str = "- not - - 123 - - not 321\n"

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
