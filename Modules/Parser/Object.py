from typing import Any
import Modules.Parser.Container as Container
import Modules.Parser.Expression as Expression
import Modules.Parser.Checker as Checker


def getVar(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    if codes[idx][0] != "IDENTIFIER":
        raise SyntaxError()
    tree: dict[str, Any] = {}
    tree["Category"] = "Object"
    tree["ObjectType"] = "Var"
    tree["Name"] = codes[idx][1]
    return (tree, idx + 1)


def getLiteral(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    if codes[idx][0] not in ["NUMBER", "STRING", "BOOL"]:
        raise SyntaxError()
    tree: dict[str, Any] = {}
    tree["Category"] = "Object"
    tree["ObjectType"] = codes[idx][0]
    tree["Value"] = codes[idx][1]

    return (tree, idx + 1)


def getKeyAndValue(
    codes: list[tuple[str, str]], idx: int
) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    tree["Category"] = "Object"
    tree["ObjectType"] = "KeyAndValue"
    expr, idx = Checker.codeMatch(
        codes=codes,
        idx=idx,
        match_list=[
            Container.getDict,
            Container.getList,
            Container.getTuple,
            Container.getSet,
            getLiteral,
            getVar,
        ],
    )
    tree["Key"] = expr
    if codes[idx][0] != "COLON":
        raise SyntaxError()
    idx += 1
    expr, idx = Checker.codeMatch(
        codes=codes,
        idx=idx,
        match_list=[
            Container.getDict,
            Container.getList,
            Container.getTuple,
            Container.getSet,
            getLiteral,
            getVar,
            Expression.getExpr,
        ],
    )
    tree["Value"] = expr
    return (tree, idx)
