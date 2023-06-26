from Modules.Parser.Expression import priority
from Modules.Parser import Parser
from Modules.Lexer import Lexer
from Modules.Parser import Container
from Modules.Parser import Object
from Modules.Parser import Expression
from Modules.Parser import Checker
from Modules.Parser import Syntax
from Modules.Parser.Expression import priority

input_txt: str = "a.a[1]() for i, j, asd123 in range(10)\n"

print(input_txt)
print(
    Parser.cleanup(Lexer.lexical_analyze(input_text=input_txt)),
    end="\n\n",
)

print(
    Syntax.getGenerator(Parser.cleanup(Lexer.lexical_analyze(input_text=input_txt)), 0),
    end="\n\n",
)

print(
    Parser.cleanup(Lexer.lexical_analyze(input_text=input_txt))[
        Syntax.getGenerator(
            Parser.cleanup(Lexer.lexical_analyze(input_text=input_txt)),
            0,
        )[1] :
    ],
    end="\n\n",
)
