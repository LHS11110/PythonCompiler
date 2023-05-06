from typing import Any


class Object:
    @staticmethod
    def getVar(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        if codes[idx][0] != "IDENTIFIER":
            raise SyntaxError()
        tree: dict[str, Any] = {}
        tree["Type"] = "Object"
        tree["ObjectType"] = "Var"
        tree["Name"] = codes[idx][1]
        return (tree, idx + 1)

    @staticmethod
    def getLiteral(
        codes: list[tuple[str, str]], idx: int
    ) -> tuple[dict[str, Any], int]:
        if codes[idx][0] not in ["NUMBER", "STRING", "BOOL"]:
            raise SyntaxError()
        tree: dict[str, Any] = {}
        tree["Type"] = "Object"
        tree["ObjectType"] = codes[idx][0]
        tree["Value"] = codes[idx][1]

        return (tree, idx + 1)
