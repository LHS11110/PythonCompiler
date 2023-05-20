from Modules.Parser import Parser
from Modules.Lexer import Lexer
from Modules.Parser import Parser
from Modules.Parser import Container
from Modules.Parser import Object
from Modules.Parser import Expression
from Modules.Parser.Expression import priority

input_txt: str = "i for i in [1, 2, 3]\n"
print(input_txt)
print(
    Parser.cleanup(Lexer.tokenize(input_text=input_txt)),
    end="\n\n",
)

print(
    Object.getGenerator(
        Parser.cleanup(Lexer.tokenize(input_text=input_txt)),
        0,
    ),
    end="\n\n",
)

print(
    Parser.cleanup(Lexer.tokenize(input_text=input_txt))[
        Object.getGenerator(
            Parser.cleanup(Lexer.tokenize(input_text=input_txt)),
            0,
        )[1] :
    ],
    end="\n\n",
)
