def Enumerater(*str_list: str) -> dict[str, int]:
    return {str_list[idx]: idx for idx in range(len(str_list))}


token: dict[str, int] = Enumerater(
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
    "Unknown",
    "pass",
)
