from Modules import Parser, Lexer
from Modules.Grammer import Expression

input_txt = """
print(), (), ()
"""

print(
    Parser.Parser().cleanup(Lexer.Lexer().tokenize(input_text=input_txt))[
        Expression.Expression().isEnum(
            Parser.Parser().cleanup(Lexer.Lexer().tokenize(input_text=input_txt)),
            1,
        )[1] :
    ],
    end="\n\n",
)

print(
    Expression.Expression().isEnum(
        Parser.Parser().cleanup(Lexer.Lexer().tokenize(input_text=input_txt)),
        1,
    )
)
