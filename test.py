from Modules import Parser, Lexer
from Modules.Grammer import Expression

input_txt: str = """for (add(), print), ({ar}), [hi()], 123 if True else 321 in
"""

print(
    Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt))[
        Expression.Expression.getEnum(
            Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt)),
            1,
        )[1] :
    ],
    end="\n\n",
)

print(
    Expression.Expression.getEnum(
        Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt)),
        1,
    )
)

print(not True or True)
