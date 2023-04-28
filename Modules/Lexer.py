from Grammer import Token
from typing import Optional
from enum import Enum
import re


class Lexer:
    class Pattern(Enum):
        NUMBER: tuple[str, str] = (r"\d+(\.\d*)?", "NUMBER")
        PLUS = (r"\+", "PLUS")
        MINUS = (r"\-", "MINUS")
        DMULTIPLY = (r"\*\*", "DMULTIPLY")
        MULTIPLY = (r"\*", "MULTIPLY")
        DIVIDE = (r"\/", "DIVIDE")
        LPAREN = (r"\(", "LPAREN")
        RPAREN = (r"\)", "RPAREN")
        LSQB = (r"\[", "LSQB")
        RSQB = (r"\]", "RSQB")
        SPACE = (r"\s+", "SPACE")
        DOT = (r"\.", "DOT")
        EQUAL = (r"\=", "EQUAL")

    @staticmethod
    def getTokenValue(string: str) -> int:
        if string not in Token.token.keys():
            return Token.token["unknown"]
        return Token.token[string]
    
    def __init__(self):
        pass

    def tokenize(self, input_text: str) -> list[tuple[str, str]]:
        tokens: list[tuple[str, str]] = []
        pos: int = 0
        length: int = len(input_text)
        while pos < length:
            for pattern, token_type in Lexer.Pattern:
                match: Optional[str] = re.match(pattern, input_text[pos:])
                if match:
                    tokens.append((token_type, match.group(0)))
                    pos += len(match.group(0))
                    break
            else:
                raise ValueError(f"Unexpected character at position {pos}")
        return tokens
    
input_text: str = "3.14 ** 512312321315241231233213123"
lexer: Lexer = Lexer()
print(lexer.tokenize(input_text=input_text))