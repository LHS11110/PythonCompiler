from typing import Any, TYPE_CHECKING
from Modules.Grammer.Checker import Checker
from Modules.Grammer.Object import Object
from Modules.Grammer.Container import Container

priority: dict[str, int] = {}


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
        while count != 0 and count % 2 == 0 and codes[idx][0] != "RSQB":
            if codes[idx][0] == "EOL" or codes[idx][0] == "INDENT":
                idx += 1

            elif not count % 2:
                if not count % 2 and codes[idx][0] == "COLON":  # 슬라이싱에서 객체가 생략됬다면
                    tree["Elements"].append({"Type": "Empty"})
                else:
                    element, idx = Checker.codeMatch(
                        codes=codes,
                        idx=idx,
                        match_list=[
                            Expression.getExpr,  # Expression은 계산식과 객체, 함수 호출, 인덱싱, 리터럴을 모두 포함한다.
                            Container.getTuple,
                            Container.getSet,
                            Container.getList,
                        ],
                    )
                    tree["Elements"].append(element)
                count += 1

            elif count % 2 and codes[idx][0] != "COLON":
                raise SyntaxError()

            else:
                idx += 1
                count += 1
        if len(tree["Elements"]) == 0 or len(tree["Elements"]) > 3:
            raise SyntaxError()
        if len(tree["Elements"]) > 1:
            tree["Type"] = "Slicing"
        return (tree, idx + 1)

    @staticmethod
    def getExpr(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        stack: list[str] = []
        raise SyntaxError()
