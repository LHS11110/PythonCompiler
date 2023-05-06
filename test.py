from Modules import Parser, Lexer
from Modules.Grammer import Expression
from Modules.Grammer import Container

input_txt: str = "[:]\n"

print(
    Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt))[
        Expression.Expression.getIndexing(
            Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt)),
            0,
        )[1] :
    ],
    end="\n\n",
)

print(
    Expression.Expression.getIndexing(
        Parser.Parser.cleanup(Lexer.Lexer.tokenize(input_text=input_txt)),
        0,
    )
)
