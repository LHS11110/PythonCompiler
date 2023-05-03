from typing import Callable, Any, Optional


class Expression:
    def __init__(self) -> None:
        pass

    @staticmethod
    def getElement(
        codes: list[tuple[str, str]],
        idx: int,
        check_list: list[
            Callable[[list[tuple[str, str]], int], tuple[dict[str, Any], int]]
        ],
    ) -> tuple[dict[str, Any], int]:
        expr_tuple: tuple[dict[str, Any], int] = ({}, 0)  # 표현식과 인덱스를 담을 튜플
        for method in check_list:
            try:
                expr, _idx = method(codes, idx)
                if _idx > expr_tuple[1]:  # 표현식이 더 많이 매칭된 경우
                    expr_tuple = (expr, _idx)
                idx = _idx
            except:
                pass
        if expr_tuple[1] == 0:  # 매칭될 수 없는 경우
            raise SyntaxError()

        return expr_tuple

    @staticmethod
    def getCall(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        tree: dict[str, Any] = {}
        if codes[idx][0] != "IDENTIFIER":
            raise SyntaxError()
        tree["Type"] = "Call"
        tree["Name"] = codes[idx][1]
        idx += 1
        tree["Arguments"], idx = Expression.getTuple(codes=codes, idx=idx)
        tree["Arguments"] = tree["Arguments"]["Elements"]

        return (tree, idx)

    @staticmethod
    def getTuple(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        tree: dict[str, Any] = {}
        if codes[idx][0] != "LPAREN":
            raise SyntaxError()
        idx += 1
        tree["Type"] = "Tuple"
        tree["Elements"] = []
        count: int = 0  # 구분자와 전달인자의 순서를 파악하는데 사용할 변수
        while codes[idx][0] != "RPAREN":
            if codes[idx][0] == "EOL" or codes[idx][0] == "INDENT":  # EOL과 INDENT는 무시
                idx += 1

            elif not count % 2:  # 전달인자 검사
                element, idx = Expression.getElement(
                    codes=codes,
                    idx=idx,
                    check_list=[
                        Expression.getCall,
                        Expression.getTuple,
                        Expression.getVar,
                        Expression.getSet,
                        Expression.getList,
                        Expression.getLiteral,
                    ],
                )
                tree["Elements"].append(element)  # type: ignore
                count += 1

            elif count % 2 and codes[idx][0] != "COMMA":  # 구분자 검사
                raise SyntaxError()

            else:  # 구분자가 올바르다면
                idx += 1
                count += 1

        return (tree, idx + 1)

    @staticmethod
    def getSet(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        tree: dict[str, Any] = {}
        if codes[idx][0] != "LBRACE":
            raise SyntaxError()
        idx += 1
        tree["Type"] = "Set"
        tree["Elements"] = []
        count: int = 0
        while codes[idx][0] != "RBRACE":
            if codes[idx][0] == "EOL" or codes[idx][0] == "INDENT":
                idx += 1

            elif not count % 2:
                element, idx = Expression.getElement(
                    codes=codes,
                    idx=idx,
                    check_list=[
                        Expression.getCall,
                        Expression.getTuple,
                        Expression.getVar,
                        Expression.getSet,
                        Expression.getList,
                        Expression.getLiteral,
                    ],
                )
                tree["Elements"].append(element)  # type: ignore
                count += 1

            elif count % 2 and codes[idx][0] != "COMMA":
                raise SyntaxError()

            else:
                idx += 1
                count += 1

        return (tree, idx + 1)

    @staticmethod
    def getList(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        tree: dict[str, Any] = {}
        if codes[idx][0] != "LSQB":
            raise SyntaxError()
        idx += 1
        tree["Type"] = "List"
        tree["Elements"] = []
        count: int = 0
        while codes[idx][0] != "RSQB":
            if codes[idx][0] == "EOL" or codes[idx][0] == "INDENT":
                idx += 1

            elif not count % 2:
                element, idx = Expression.getElement(
                    codes=codes,
                    idx=idx,
                    check_list=[
                        Expression.getCall,
                        Expression.getTuple,
                        Expression.getVar,
                        Expression.getSet,
                        Expression.getList,
                        Expression.getLiteral,
                    ],
                )
                tree["Elements"].append(element)  # type: ignore
                count += 1

            elif count % 2 and codes[idx][0] != "COMMA":
                raise SyntaxError()

            else:
                idx += 1
                count += 1

        return (tree, idx + 1)

    @staticmethod
    def getEnum(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        tree: dict[str, Any] = {}
        tree["Type"] = "Enum"
        tree["Elements"] = []
        count: int = 0
        error_idx: int = idx
        while True:
            if codes[idx][0] == "INDENT":
                idx += 1

            elif not count % 2:
                try:
                    element, idx = Expression.getElement(
                        codes=codes,
                        idx=idx,
                        check_list=[
                            Expression.getCall,
                            Expression.getTuple,
                            Expression.getVar,
                            Expression.getSet,
                            Expression.getList,
                            Expression.getLiteral,
                        ],
                    )
                    tree["Elements"].append(element)  # type: ignore
                    count += 1
                except:
                    break

            elif count % 2 and codes[idx][0] != "COMMA":
                break

            else:
                idx += 1
                count += 1
        if error_idx == idx:
            raise SyntaxError()
        return (tree, idx)

    @staticmethod
    def getVar(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        if codes[idx][0] != "IDENTIFIER":
            raise SyntaxError()
        tree: dict[str, Any] = {}
        tree["Type"] = "Var"
        tree["Name"] = codes[idx][1]
        return (tree, idx + 1)

    @staticmethod
    def getLiteral(
        codes: list[tuple[str, str]], idx: int
    ) -> tuple[dict[str, Any], int]:
        if codes[idx][0] not in ["NUMBER", "STRING"]:
            raise SyntaxError()
        tree: dict[str, Any] = {}
        tree["Type"] = "Literal"
        tree["Value"] = codes[idx][1]

        return (tree, idx + 1)
