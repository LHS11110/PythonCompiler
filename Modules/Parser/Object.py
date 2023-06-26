from typing import Any, Callable


def getVar(tokens: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    assert tokens[idx][0] == "IDENTIFIER", ""
    tree: dict[str, Any] = {}
    tree["Category"] = "Object"
    tree["ObjectType"] = "Var"
    tree["Name"] = tokens[idx][1]
    return (tree, idx + 1)


def getLiteral(tokens: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    assert tokens[idx][0] in ["NUMBER", "STRING", "BOOL"], ""
    tree: dict[str, Any] = {}
    tree["Category"] = "Object"
    tree["ObjectType"] = tokens[idx][0]
    tree["Value"] = tokens[idx][1]
    return (tree, idx + 1)


default_obj: list[
    Callable[[list[tuple[str, str]], int], tuple[dict[str, Any], int]]
] = [
    getLiteral,
    getVar,
]
