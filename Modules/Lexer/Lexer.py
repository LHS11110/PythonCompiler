from collections.abc import Iterator
from typing import Any, Optional
import re
from re import Match


class Token:
    def __init__(self) -> None:
        self.idx: int = 0
        self.tokens: list[tuple[str, str]] = []
        with open("Grammer/tokens.txt", "r") as file:
            tokens: list[list[str]] = [line.split() for line in file.read().split("\n")]
        for token in tokens:
            self.tokens.append((" ".join(token[1:]), token[0]))

    def __iter__(self) -> Iterator[tuple[str, str]]:
        return self.tokens.__iter__()


def lexical_analyze(input_text: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] = []
    pos: int = 0
    length: int = len(input_text)
    while pos < length:
        match_list: list[tuple[str, str]] = []
        for token, token_type in Token():
            match: Optional[Match[Any]] = re.match(token, input_text[pos:])
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
    print(lexical_analyze(input_text=input_text))
