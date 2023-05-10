from typing import Any
from Modules.Grammer.Checker import Checker
from Modules.Grammer.Object import Object
from Modules.Grammer.Container import Container


# 연산자 우선순위
priority: dict[str, int] = {}
with open("Modules/Grammer/priority.txt", "r") as file:
    for key, value in [
        line.split() for line in [line for line in file.read().split("\n")]
    ]:
        priority[key] = int(value)


class Expression:
    class_names: list[str] = [
        "int",
        "float",
        "str",
        "list",
        "tuple",
        "dict",
        "set",
    ]  # 컨테이너 클래스도 포함

    def __init__(self) -> None:
        pass

    @staticmethod
    def getIndexing(
        codes: list[tuple[str, str]], idx: int
    ) -> tuple[dict[str, Any], int]:
        if codes[idx][0] != "LSQB":
            raise SyntaxError()
        idx += 1
        tree: dict[str, Any] = {}
        tree["Type"] = "Expression"
        tree["ObjectType"] = "Indexing"
        tree["Elements"] = []
        count: int = 0
        while codes[idx][0] != "RSQB":
            if codes[idx][0] == "EOL" or codes[idx][0] == "INDENT":
                idx += 1

            elif not count % 2:
                if codes[idx][0] == "COLON":  # 슬라이싱에서 객체가 생략됬다면
                    tree["Elements"].append({"Type": "Empty"})
                else:
                    element, idx = Checker.codeMatch(
                        codes=codes,
                        idx=idx,
                        match_list=[
                            Object.getVar,
                            Object.getLiteral,
                            Expression.getExpr,
                            Container.getTuple,
                            Container.getSet,
                            Container.getList,
                            Container.getDict,
                        ],
                    )
                    tree["Elements"].append(element)
                count += 1

            elif count % 2 and codes[idx][0] != "COLON":
                raise SyntaxError()

            else:
                idx += 1
                count += 1
        if not count % 2:  # 마지막 객체가 생략됬다면
            tree["Elements"].append({"Type": "Empty"})
        if len(tree["Elements"]) == 0 or len(tree["Elements"]) > 3:
            raise SyntaxError()
        if len(tree["Elements"]) > 1:
            tree["Type"] = "Slicing"
        return (tree, idx + 1)

    @staticmethod
    def getMemberAccess(
        codes: list[tuple[str, str]], idx: int
    ) -> tuple[dict[str, Any], int]:
        if codes[idx][0] != "DOT":
            raise SyntaxError()
        idx += 1
        tree: dict[str, Any] = {}
        tree["Type"] = "Expression"
        tree["ObjectType"] = "MemberAccess"
        tree["Member"], idx = Checker.codeMatch(
            codes=codes, idx=idx, match_list=[Object.getVar]
        )

        return (tree, idx)

    @staticmethod
    def getCall(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        tree: dict[str, Any] = {}
        expr, idx = Checker.codeMatch(
            codes=codes, idx=idx, match_list=[Container.getTuple]
        )
        tree["Type"] = "Expression"
        tree["ObjectType"] = "Call"
        tree["Arguments"] = expr["Elements"]
        return (tree, idx)

    @staticmethod
    def getUnaryOp(
        codes: list[tuple[str, str]], idx: int
    ) -> tuple[dict[str, Any], int]:
        if codes[idx][0] not in ["MINUS", "PLUS", "NOT"]:
            raise SyntaxError()
        tree: dict[str, Any] = {}
        tree["Type"] = "Expression"
        tree["ObjectType"] = (
            "NOT" if codes[idx][0] == "NOT" else "UNARY_" + codes[idx][0]
        )
        return (tree, idx + 1)

    @staticmethod
    def getBinaryOp(
        codes: list[tuple[str, str]], idx: int
    ) -> tuple[dict[str, Any], int]:
        if codes[idx][0] not in [
            "DMULTIPLY",
            "MULTIPLY",
            "DIVIDE",
            "FLOORDIV",
            "MODULO",
            "PLUS",
            "MINUS",
            "RBITSHIFT",
            "LBITSHIFT",
            "AND",
            "OR",
            "BITAND",
            "BITOR",
            "BITXOR",
            "IN",
            "NOTIN",
            "IS",
            "ISNOT",
            "LESS",
            "GREATER",
            "LEQUAL",
            "GEQUAL",
            "NEQUAL",
            "DEQUAL",
        ]:
            raise SyntaxError()
        tree: dict[str, Any] = {}
        tree["Type"] = "Expression"
        tree["ObjectType"] = codes[idx][0]
        return (tree, idx + 1)

    @staticmethod
    def getTernaryOp(
        codes: list[tuple[str, str]], idx: int
    ) -> tuple[dict[str, Any], int]:
        if codes[idx][0] != "IF":
            raise SyntaxError()
        idx += 1
        tree: dict[str, Any] = {}
        tree["Type"] = "Expression"
        tree["ObjectType"] = "TERNARY_OP"
        tree["Mid"], idx = Checker.codeMatch(
            codes=codes,
            idx=idx,
            match_list=[
                Object.getLiteral,
                Object.getVar,
                Expression.getExpr,
                Container.getDict,
                Container.getList,
                Container.getSet,
                Container.getTuple,
            ],
        )
        if codes[idx][0] != "ELSE":
            raise SyntaxError()
        return (tree, idx + 1)

    @staticmethod
    def getAnotherOp(
        codes: list[tuple[str, str]], idx: int
    ) -> tuple[dict[str, Any], int]:
        tree, idx = Checker.codeMatch(
            codes=codes,
            idx=idx,
            match_list=[
                Expression.getCall,
                Expression.getIndexing,
                Expression.getMemberAccess,
            ],
        )
        return (tree, idx)

    @staticmethod
    def getExpr(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        stack: list[dict[str, Any]] = []
        tree: dict[str, Any] = {}

        return (tree, idx)
