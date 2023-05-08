from typing import Any, TYPE_CHECKING
from Modules.Grammer.Checker import Checker
from Modules.Grammer.Object import Object
from Modules.Grammer.Container import Container


# 연산자 우선순위
priority: dict[str, int] = {
    "Object": 1,
    "Container": 1,
    "Indexing": 2,
    "Slicing": 2,
    "Call": 2,
    "MemberAccess": 2,
    "DMULTIPLY": 4,
    "UNARY_MINUS": 5,
    "UNARY_PLUS": 5,
    "UNARY_NOT": 5,
    "MULTIPLY": 6,
    "DIVIDE": 6,
    "FLOORDIV": 6,
    "MODULO": 6,
    "PLUS": 7,
    "MINUS": 7,
    "RBITSHIFT": 8,
    "LBITSHIFT": 8,
    "BITAND": 9,
    "BITXOR": 10,
    "BITOR": 11,
    "IN": 12,
    "NOTIN": 12,
    "IS": 12,
    "ISNOT": 12,
    "LESS": 12,
    "GREATER": 12,
    "LEQUAL": 12,
    "GEQUAL": 12,
    "NEQUAL": 12,
    "DEQUAL": 12,
    "NOT": 13,
    "AND": 14,
    "OR": 15,
    "TERNARY_OP": 16,
}


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
        tree["Type"] = "Indexing"
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
        tree["Type"] = "MemberAccess"
        tree["Member"], idx = Checker.codeMatch(
            codes=codes, idx=idx, match_list=[Object.getVar]
        )

        return (tree, idx)

    @staticmethod
    def getExpr(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        stack: list[str] = []
        tree: dict[str, Any] = {}

        return (tree, idx)
