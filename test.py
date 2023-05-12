from Modules.Parser import Parser
from Modules.Lexer import Lexer
from Modules.Parser import Parser
from Modules.Parser import Container
from Modules.Parser import Object
from Modules.Parser.Expression import priority

input_txt: str = '123           :           "asd"'

print(
    Parser.cleanup(Lexer.tokenize(input_text=input_txt)),
    end="\n\n",
)

print(
    Object.getKeyAndValue(
        Parser.cleanup(Lexer.tokenize(input_text=input_txt)),
        0,
    ),
    end="\n\n",
)


print(priority)
