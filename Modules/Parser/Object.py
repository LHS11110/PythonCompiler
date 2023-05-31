from typing import Any, Callable


def getVar(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    assert codes[idx][0] == "IDENTIFIER", ""
    tree: dict[str, Any] = {}
    tree["Category"] = "Object"
    tree["ObjectType"] = "Var"
    tree["Name"] = codes[idx][1]
    return (tree, idx + 1)


def getLiteral(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    assert codes[idx][0] in ["NUMBER", "STRING", "BOOL"], ""
    tree: dict[str, Any] = {}
    tree["Category"] = "Object"
    tree["ObjectType"] = codes[idx][0]
    tree["Value"] = codes[idx][1]
    return (tree, idx + 1)


default_obj: list[
    Callable[[list[tuple[str, str]], int], tuple[dict[str, Any], int]]
] = [
    getLiteral,
    getVar,
]
