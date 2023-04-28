from Grammer import Token


def getToken(string: str) -> int:
    if string not in Token.token.keys():
        return Token.token["unknown"]
    return Token.token[string]


class Lexer:
    ...
