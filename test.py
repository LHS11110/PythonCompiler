from Modules import Parser, Lexer
from Modules.Grammer import Expression

input_txt = """for ((123, "Hello, World!"), ()), (add(), print), ({ar}), [hi()] in
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
