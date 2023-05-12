from typing import Any
from Modules.Parser import Checker
from Modules.Parser import Object
from Modules.Parser import Container


# 연산자 우선순위
priority: dict[str, list[list[str]]] = {}
with open("Grammer/priority.txt", "r") as file:
    category: str = ""
    for line in file.read().split("\n"):
        line_list: list[str] = line.split()
        if len(line_list) == 1:
            category = line_list[0]
            priority[category] = []
        elif len(line_list) > 0:
            priority[category].append(list(value for value in line_list))


def getIndexing(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    if codes[idx][0] != "LSQB":
        raise SyntaxError()
    idx += 1
    tree: dict[str, Any] = {}
    tree["Category"] = "Expression"
    tree["ObjectType"] = "Indexing"
    tree["Elements"] = []
    count: int = 0
    while codes[idx][0] != "RSQB":
        if codes[idx][0] == "EOL" or codes[idx][0] == "INDENT":
            idx += 1

        elif not count % 2:
            if codes[idx][0] == "COLON":  # 슬라이싱에서 객체가 생략됬다면
                tree["Elements"].append({})  # type: ignore
            else:
                element, idx = Checker.codeMatch(
                    codes=codes,
                    idx=idx,
                    match_list=[
                        Object.getVar,
                        Object.getLiteral,
                        getExpr,
                        Container.getTuple,
                        Container.getSet,
                        Container.getList,
                        Container.getDict,
                    ],
                )
                tree["Elements"].append(element)  # type: ignore
            count += 1

        elif count % 2 and codes[idx][0] != "COLON":
            raise SyntaxError()

        else:
            idx += 1
            count += 1
    if not count % 2:  # 마지막 객체가 생략됬다면
        tree["Elements"].append({})  # type: ignore
    if len(tree["Elements"]) == 0 or len(tree["Elements"]) > 3:
        raise SyntaxError()
    if len(tree["Elements"]) > 1:
        if len(tree["Elements"]) == 2:
            tree["Elements"].append({})  # type: ignore
        tree["ObjectType"] = "Slicing"
    return (tree, idx + 1)


def getMemberAccess(
    codes: list[tuple[str, str]], idx: int
) -> tuple[dict[str, Any], int]:
    if codes[idx][0] != "DOT":
        raise SyntaxError()
    idx += 1
    tree: dict[str, Any] = {}
    tree["Category"] = "Expression"
    tree["ObjectType"] = "MemberAccess"
    tree["Member"], idx = Checker.codeMatch(
        codes=codes, idx=idx, match_list=[Object.getVar]
    )

    return (tree, idx)


def getCall(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    expr, idx = Checker.codeMatch(codes=codes, idx=idx, match_list=[Container.getTuple])
    tree["Category"] = "Expression"
    tree["ObjectType"] = "Call"
    tree["Elements"] = expr["Elements"]
    return (tree, idx)


def getTernaryOp(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    tree["Category"] = "Expression"
    tree["ObjectType"] = "TernaryOp"
    for op, next_syntax, _priority in priority["TernaryOperator"]:
        if codes[idx][0] == op:
            tree["Op"] = op
            tree["NextSyntax"] = [next_syntax]
            tree["Priority"] = int(_priority)
            break
    else:
        raise SyntaxError()

    return (tree, idx + 1)


def getBinaryOp(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    tree["Category"] = "Expression"
    tree["ObjectType"] = "BinaryOp"
    for op, _priority in priority["BinaryOperator"]:
        if codes[idx][0] == op:
            tree["Op"] = op
            tree["Priority"] = int(_priority)
            break
    else:
        raise SyntaxError()

    return (tree, idx + 1)


def getPostUnaryOp(
    codes: list[tuple[str, str]], idx: int
) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    tree["Category"] = "Expression"
    tree["ObjectType"] = "PostUnaryOp"
    expr, idx = Checker.codeMatch(
        codes=codes,
        idx=idx,
        match_list=[
            getCall,
            getIndexing,
            getMemberAccess,
        ],
    )

    for op, _priority in priority["PostUnaryOperator"]:
        if expr["ObjectType"] == op:
            tree["Op"] = op
            tree["Priority"] = int(_priority)
            tree["Elements"] = expr["Elements"]
            break
    else:
        raise SyntaxError()

    return (tree, idx + 1)


def getPreUnaryOp(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    tree["Category"] = "Expression"
    tree["ObjectType"] = "PreUnaryOp"
    for op, _priority in priority["PreUnaryOperator"]:
        if codes[idx][0] == op:
            tree["Op"] = op
            tree["Priority"] = int(_priority)
            break
    else:
        raise SyntaxError()

    return (tree, idx + 1)


def getExpr(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    stack: list[dict[str, Any]] = []
    tree: dict[str, Any] = {}
    syntax_stack: list[str] = []
    tree["Category"] = "Expression"
    tree["ObjectType"] = "Expression"

    return (tree, idx)