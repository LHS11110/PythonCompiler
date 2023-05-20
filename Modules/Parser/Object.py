from typing import Any, Callable
import Modules.Parser.Container as Container
import Modules.Parser.Expression as Expression
import Modules.Parser.Checker as Checker


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
    assert codes[idx][0] == "COLON", ""
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


def getGenerator(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    expr, idx = Checker.codeMatch(
        codes=codes,
        idx=idx,
        match_list=[
            getLiteral,
            getVar,
            Container.getDict,
            Container.getList,
            Container.getSet,
            Container.getTuple,
            Expression.getExpr,
        ],
    )

    tree: dict[str, Any] = {}
    tree["Output"] = expr
    assert codes[idx][0] == "FOR", ""
    idx += 1
    tree["Variables"], idx = Checker.codeMatch(
        codes=codes,
        idx=idx,
        match_list=[getVar, Container.getTuple, Container.getEnum],
    )
    if tree["Variables"]["ObjectType"] != "Var":
        assert Checker.typeCheck(
            obj_types=[obj["ObjectType"] for obj in tree["Variables"]["Elements"]],
            type_list=["Var"],
        ), ""
        tree["Variables"] = tree["Variables"]["Elements"]
    else:
        tree["Variables"] = [tree["Variables"]]
    assert codes[idx][0] == "IN", ""
    idx += 1
    expr, idx = Checker.codeMatch(
        codes=codes,
        idx=idx,
        match_list=[
            Container.getDict,
            Container.getList,
            Container.getSet,
            Container.getTuple,
            Container.getEnum,
        ],
    )
    tree["Row"] = expr
    if codes[idx][0] != "IF":
        return (tree, idx)
    idx += 1
    expr, idx = Checker.codeMatch(
        codes=codes,
        idx=idx,
        match_list=[
            getLiteral,
            getVar,
            Container.getDict,
            Container.getList,
            Container.getSet,
            Container.getTuple,
            Expression.getExpr,
        ],
    )
    tree["Condition"] = expr
    return (tree, idx)


obj_list: list[Callable[[list[tuple[str, str]], int], tuple[dict[str, Any], int]]] = [
    getGenerator,
    getKeyAndValue,
    getLiteral,
    getVar,
]
