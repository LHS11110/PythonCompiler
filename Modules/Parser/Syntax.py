from typing import Any


def setCheck(tree: dict[str, Any]) -> bool:
    if tree["Category"] == "Object" and tree["ObjectType"] == "Var":
        return True
    elif tree["Category"] == "Expression":
        pass
    return False


def initialization(
    codes: list[tuple[str, str]], idx: int
) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    return (tree, idx)
