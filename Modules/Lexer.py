from collections.abc import Iterator
from typing import Any, Optional
from Modules.Grammer import Token
import re
from re import Match


class Lexer:
    class Pattern:
        def __init__(self) -> None:
            self.idx: int = 0
            self.patterns: list[tuple[str, str]] = []
            with open("Modules/Grammer/tokens.txt", "r") as file:
                patterns: list[list[str]] = [
                    line.split() for line in file.read().split("\n")
                ]
            for pattern in patterns:
                self.patterns.append((" ".join(pattern[1:]), pattern[0]))

        def __iter__(self) -> Iterator[tuple[str, str]]:
            return self.patterns.__iter__()

    @staticmethod
    def getTokenValue(string: str) -> int:
        if not Token.token:
            raise ValueError("Token.token is None")
        if string not in Token.token.keys():
            raise ValueError("string not in Token.token.keys")
        return Token.token[string]

    def __init__(self):
        pass

    def tokenize(self, input_text: str) -> list[tuple[str, str]]:
        tokens: list[tuple[str, str]] = []
        pos: int = 0
        length: int = len(input_text)
        while pos < length:
            match_list: list[tuple[str, str]] = []
            for pattern, token_type in Lexer.Pattern():
                match: Optional[Match[Any]] = re.match(pattern, input_text[pos:])
                if not match:
                    continue
                match_list.append((token_type, match.group()))
            if not match_list:
                raise ValueError(f"Unexpected character at position {pos}")
            token: tuple[str, str] = match_list[0]
            for another_token in match_list[1:]:
                if len(token[1]) < len(another_token[1]):
                    token = another_token
            pos += len(token[1])
            if token[0] != "SPACE":
                tokens.append(token)

        return tokens


if __name__ == "__main__":
    input_text: str = input("input code : ")

    for token_type, txt in Lexer().tokenize(input_text=input_text):
        print(token_type, txt, Lexer.getTokenValue(token_type))
