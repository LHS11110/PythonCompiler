from Modules.Parser import Parser
from Modules.Lexer import Lexer
from Modules.Parser import Parser
from Modules.Parser import Container
from Modules.Parser import Object
from Modules.Parser import Expression
from Modules.Parser import Checker
from Modules.Parser.Expression import priority

input_txt: str = '{1: 2, "123": 123, {123}: [123]}\n'

print(input_txt)
print(
    Parser.cleanup(Lexer.tokenize(input_text=input_txt)),
    end="\n\n",
)

print(
    Container.getDict(
        Parser.cleanup(Lexer.tokenize(input_text=input_txt)),
        0,
        container_list=[Container.getList, Container.getSet],
        obj_list=[Object.getLiteral, Object.getVar],
    ),
    end="\n\n",
)

print(
    Parser.cleanup(Lexer.tokenize(input_text=input_txt))[
        Container.getDict(
            Parser.cleanup(Lexer.tokenize(input_text=input_txt)),
            0,
            container_list=[Container.getList, Container.getSet],
            obj_list=[Object.getLiteral, Object.getVar],
        )[1] :
    ],
    end="\n\n",
)
