def Enumerater(*str_list: str) -> dict[str, int]:
    return {str_list[idx]: idx for idx in range(len(str_list))}


token: dict[str, int] = Enumerater(
    # Spesial Form
    "PLUS",         # +
    "MINUS",        # -
    "MULTIPLY",     # *
    "DIVIDE",       # /
    "NOT",          # not
    "EQUAL",        # =
    "MODULO",       # %
    "DMULTIPLY",    # **
    "DEQUAL",       # ==
    "NEQUAL",       # !=
    "LESS",         # <
    "GREATER",      # >
    "LEQUAL",       # <=
    "GEQUAL",       # >=
    "AND",          # and
    "OR",           # or
    "PEQUAL",       # +=
    "MEQUAL",       # -=
    "MULEQUAL",     # *=
    "DIVEQUAL",     # /=
    "MODULEQUAL",   # %=
    "DOT",          # .
    "LSQB",         # [
    "RSQB",         # ]
    "LBRACE",       # {
    "RBRACE"        # }
    "LPAREN",       # (
    "RPAREN",       # )
    "SPACE",        # space
    "EOL",          # \n
    "BSLASH",       # \
    'QMARK',        # "
    "APOSTROPHE",   # '
    "IF",           # if
    "ELIF",         # elif
    "ELSE",         # else
    "FOR",          # for
    "IN",           # in
    "WHILE",        # while
    "RETURN",       # return
    "YEILD",        # yeild
    "DEF",          # def
    "UNKNOWN",      #
    "PASS",         # pass, ...
    "COLON",        # :
    # General Form
    "DECIMAL",      # 0-9
    "NUMBER",       # 0-9
    "STRING",       # a-z, A-Z
    "IDENTIFIER",   #
    "INDENT",       # tap
)
