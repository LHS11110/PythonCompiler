from Grammer import Token


def Token(string: str) -> int:
    if string not in Token.token.items():
        return Token.token["Unknown"]
    return Token.token[string]
