def Enumerater(*str_list: tuple[str]) -> dict[str, int]:
    return {str_list[idx]: idx for idx in range(len(str_list))}


Token: dict[str, int] = Enumerater(
    # Operator Tokens
    "+",
    "-",
    "*",
    "/",
    "not",
    "=",
    "%",
    "==",
    "!=",
    ">",
    "<",
    ">=",
    "<=",
    "and",
    "or",
    "+=",
    "-=",
    "*=",
    "/=",
    "%=",
    ".",
    "[",
    "]",
    "{",
    "}",
    "(",
    ")",
    # Control Flow Statements Tokens
    "if",
    "elif",
    "else",
    "for",
    "while",
    # Keyword Tokens
    "return",
    "yeild",
    "def",
)
