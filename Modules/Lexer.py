from collections.abc import Iterator
from typing import Any, Optional
from Grammer import Token
import re
from re import Match


class Lexer:
    class Pattern:
        def __init__(self) -> None:
            self.idx: int = 0
            self.patterns: list[tuple[str, str]] = [
                (p, n)
                for n, p in [
                    line.split()
                    for line in open("Modules/Grammer/tokens.txt", "r")
                    .read()
                    .split("\n")
                ]
            ]

            identifier_pattern: str = ""
            for p, _ in self.patterns:
                for _p in p.split("|"):
                    match: Optional[Match[Any]] = re.match(r"[a-zA-Z]+", _p)
                    if match:
                        identifier_pattern += f"^{match.group()}+\\w+|"
            identifier_pattern = identifier_pattern[:-1]
            self.patterns.insert(0, (identifier_pattern, "IDENTIFIER"))
            self.patterns.append((r"\w+", "IDENTIFIER"))

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
            for pattern, token_type in Lexer.Pattern():
                match: Optional[Match[Any]] = re.match(pattern, input_text[pos:])
                if match:
                    tokens.append((token_type, match.group()))
                    pos += len(match.group())
                    break
            else:
                raise ValueError(f"Unexpected character at position {pos}")
        return tokens


if __name__ == "__main__":
    print(Lexer().tokenize("False True Falseasdf Trueasdf"))
