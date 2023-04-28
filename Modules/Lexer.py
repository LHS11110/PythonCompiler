from Grammer import Token


class Lexer:
    @staticmethod
    def getToken(string: str) -> int:
        if string not in Token.token.keys():
            return Token.token["unknown"]
        return Token.token[string]
