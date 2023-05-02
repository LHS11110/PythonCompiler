from Modules import Parser, Lexer
from Modules.Grammer import Expression

input_txt = """
print(
    print(),
    test()                      , add(),
        div(),
    mul(add(),
        add()), ()
)
"""

print(
    Parser.Parser().clean(Lexer.Lexer().tokenize(input_text=input_txt))[
        Expression.Expression().isCall(
            Parser.Parser().clean(Lexer.Lexer().tokenize(input_text=input_txt)),
            1,
        )[1] :
    ],
    end="\n\n",
)

print(
    Expression.Expression().isCall(
        Parser.Parser().clean(Lexer.Lexer().tokenize(input_text=input_txt)),
        1,
    )
)
