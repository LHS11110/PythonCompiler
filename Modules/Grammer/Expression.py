from typing import Callable, Any


class Expression:
    class_names: list[str] = []
    container_names: list[str] = []

    def __init__(self) -> None:
        pass

    @staticmethod
    def checkElement(
        codes: list[tuple[str, str]],
        idx: int,
        check_list: list[
            Callable[[list[tuple[str, str]], int], tuple[dict[str, Any], int]]
        ],
    ) -> tuple[dict[str, Any], int]:
        """
        Returns
        -------
        Dict[str, Any]: Matched Expression
        int: End Index
        """
        expr_tuple: tuple[dict[str, Any], int] = ({}, -1)  # 표현식과 인덱스를 담을 튜플

        for method in check_list:
            try:
                expr, _idx = method(codes, idx)
                if _idx > expr_tuple[1]:  # 표현식이 더 많이 매칭된 경우
                    expr_tuple = (expr, _idx)
            except:  # 매칭될 수 없는 경우
                pass
        if expr_tuple[1] == -1:  # 매칭될 수 없는 경우
            raise SyntaxError()

        return expr_tuple

    @staticmethod
    def checkType(obj_type: str, check_list: list[str]) -> bool:
        return True if obj_type in check_list else False

    @staticmethod
    def getCall(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        """
        Returns
        -------
        Dict[str, Any]: Type=Call, Name=Function Name, Arguments=Elements
        int: End Index
        """
        tree: dict[str, Any] = {}
        if codes[idx][0] != "IDENTIFIER":
            raise SyntaxError()
        tree["Type"] = "Call"
        tree["Name"] = codes[idx][1]
        idx += 1
        tree["Arguments"], idx = Expression.getTuple(codes=codes, idx=idx)
        tree["Arguments"] = tree["Arguments"]["Elements"]
        if codes[idx][0] == "RARROW":
            pass
        return (tree, idx)

    @staticmethod
    def getTuple(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        """
        Returns
        -------
        Dict[str, Any]: Type=Tuple, Elements=Objects
        int: End Index
        """
        tree: dict[str, Any] = {}
        if codes[idx][0] != "LPAREN":
            raise SyntaxError()
        idx += 1
        tree["Type"] = "Tuple"
        tree["Elements"] = []
        count: int = 0  # 구분자와 표현식의 순서를 파악하는데 사용할 변수
        while codes[idx][0] != "RPAREN":
            if codes[idx][0] == "EOL" or codes[idx][0] == "INDENT":  # EOL과 INDENT는 무시
                idx += 1

            elif not count % 2:  # 표현식 검사
                element, idx = Expression.checkElement(
                    codes=codes,
                    idx=idx,
                    check_list=[
                        Expression.getCall,
                        Expression.getTuple,
                        Expression.getVar,
                        Expression.getSet,
                        Expression.getList,
                        Expression.getLiteral,
                        Expression.getTernaryOper,
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
        """
        Returns
        -------
        Dict[str, Any]: Type=Set, Elements=Objects
        int: End Index
        """
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
                element, idx = Expression.checkElement(
                    codes=codes,
                    idx=idx,
                    check_list=[
                        Expression.getCall,
                        Expression.getTuple,
                        Expression.getVar,
                        Expression.getSet,
                        Expression.getList,
                        Expression.getLiteral,
                        Expression.getTernaryOper,
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
        """
        Returns
        -------
        Dict[str, Any]: Type=List, Elements=Objects
        int: End Index
        """
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
                element, idx = Expression.checkElement(
                    codes=codes,
                    idx=idx,
                    check_list=[
                        Expression.getCall,
                        Expression.getTuple,
                        Expression.getVar,
                        Expression.getSet,
                        Expression.getList,
                        Expression.getLiteral,
                        Expression.getTernaryOper,
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
        """
        Returns
        -------
        Dict[str, Any]: Type=Enum, Elements=Objects
        int: End Index
        """
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
                    element, idx = Expression.checkElement(
                        codes=codes,
                        idx=idx,
                        check_list=[
                            Expression.getCall,
                            Expression.getTuple,
                            Expression.getVar,
                            Expression.getSet,
                            Expression.getList,
                            Expression.getLiteral,
                            Expression.getTernaryOper,
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
        """
        Returns
        -------
        Dict[str, Any]: Type=Var, Name=Variable Name
        int: End Index
        """
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
        """
        Returns
        -------
        Dict[str, Any]: Type=Literal, Value=Literal Value
        int: End Index
        """
        if codes[idx][0] not in ["NUMBER", "STRING", "BOOL"]:
            raise SyntaxError()
        tree: dict[str, Any] = {}
        tree["Type"] = "Literal"
        tree["Value"] = codes[idx][1]

        return (tree, idx + 1)

    @staticmethod
    def getTernaryOper(
        codes: list[tuple[str, str]], idx: int
    ) -> tuple[dict[str, Any], int]:
        """
        Returns
        -------
        Dict[str, Any]: Type=Ternary Operator, isTrue, isFalse, ConditionalExpr
        int: End Index
        """
        tree: dict[str, Any] = {}
        tree["Type"] = "TernaryOperator"
        tree["isTrue"], idx = Expression.checkElement(
            codes=codes,
            idx=idx,
            check_list=[
                Expression.getCall,
                Expression.getList,
                Expression.getLiteral,
                Expression.getSet,
                Expression.getTuple,
                Expression.getVar,
            ],
        )
        if codes[idx][0] != "IF":
            raise SyntaxError()
        idx += 1
        tree["ConditionalExpr"], idx = Expression.checkElement(
            codes=codes,
            idx=idx,
            check_list=[
                Expression.getCall,
                Expression.getList,
                Expression.getLiteral,
                Expression.getSet,
                Expression.getTuple,
                Expression.getVar,
            ],
        )
        if codes[idx][0] != "ELSE":
            raise SyntaxError()
        idx += 1
        tree["isFalse"], idx = Expression.checkElement(
            codes=codes,
            idx=idx,
            check_list=[
                Expression.getCall,
                Expression.getList,
                Expression.getLiteral,
                Expression.getSet,
                Expression.getTuple,
                Expression.getVar,
            ],
        )
        return (tree, idx)

    @staticmethod
    def getExpr(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        literal: Callable[
            [], tuple[dict[str, Any], int]
        ] = lambda: Expression.getLiteral(codes=codes, idx=idx)
