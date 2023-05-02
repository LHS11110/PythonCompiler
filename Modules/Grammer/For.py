from typing import Any


class For:
    def __init__(self, codes: list[tuple[str, str]]) -> None:
        self.codes: list[tuple[str, str]] = codes

    def get(self, idx: int) -> dict[str, Any]:
        tree: dict[str, Any] = {}
        if self.codes[idx][0] != "FOR":
            raise SyntaxError()
        tree["FOR"] = {}
        idx += 1

        while self.codes[idx][0] == "INDENT":
            idx += 1

        operand1: tuple[str, str] = ("IDENTIFIER", "COMMA")
        oper1_list: list[str] = []
        count: int = 0
        while self.codes[idx][0] != "IN":
            if self.codes[idx][0] == "INDENT":
                idx += 1
                continue
            if self.codes[idx][0] != operand1[count % 2]:
                raise SyntaxError()
            if not count % 2:
                oper1_list.append(self.codes[idx][1])
            count += 1
            idx += 1
        idx += 1

        return tree
