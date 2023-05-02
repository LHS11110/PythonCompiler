from typing import Callable, Any


class Expression:
    def __init__(self) -> None:
        self.check_list: list[
            Callable[[list[tuple[str, str]], int], tuple[dict[str, Any], int]]
        ] = [Expression.isCall, Expression.isTuple]

    @staticmethod
    def isCall(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        tree: dict[str, Any] = {}
        if codes[idx][0] != "IDENTIFIER":
            raise SyntaxError()
        tree["Type"] = "Call"
        tree["Name"] = codes[idx][1]
        idx += 1
        tree["arguments"], idx = Expression.isTuple(codes=codes, idx=idx)
        tree["arguments"] = tree["arguments"]["elements"]

        return (tree, idx)

    @staticmethod
    def isTuple(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        tree: dict[str, Any] = {}
        if codes[idx][0] != "LPAREN":
            raise SyntaxError()
        idx += 1
        tree["Type"] = "Tuple"
        tree["elements"] = []
        count: int = 0  # 구분자와 전달인자의 순서를 파악하는데 사용할 변수
        while codes[idx][0] != "RPAREN":
            if codes[idx][0] == "EOL" or codes[idx][0] == "INDENT":  # EOL과 INDENT는 무시
                idx += 1

            elif not count % 2:  # 전달인자 검사
                expr_tuple: tuple[dict[str, Any], int] = ({}, -1)
                for method in Expression().check_list:
                    try:
                        expr, _idx = method(codes, idx)
                        if _idx > expr_tuple[1]:
                            expr_tuple = (expr, _idx)
                        idx = _idx
                        break
                    except:
                        pass
                if expr_tuple[1] == -1:
                    raise SyntaxError()
                tree["elements"].append(expr_tuple[0])  # type: ignore
                count += 1

            elif count % 2 and codes[idx][0] != "COMMA":  # 구분자 검사
                raise SyntaxError()

            else:  # 구분자가 올바르다면
                idx += 1
                count += 1

        return (tree, idx + 1)
