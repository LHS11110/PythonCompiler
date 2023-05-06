from typing import Callable, Any


class Checker:
    @staticmethod
    def codeMatch(
        codes: list[tuple[str, str]],
        idx: int,
        match_list: list[
            Callable[[list[tuple[str, str]], int], tuple[dict[str, Any], int]]
        ],
    ) -> tuple[dict[str, Any], int]:
        expr_tuple: tuple[dict[str, Any], int] = ({}, -1)  # 표현식과 인덱스를 담을 튜플

        for method in match_list:
            try:
                expr, _idx = method(codes, idx)
                if _idx > expr_tuple[1]:  # 표현식이 더 많이 매칭된 경우
                    expr_tuple = (expr, _idx)
            except:  # 매칭될 수 없는 경우
                pass
        if expr_tuple[1] == -1:  # 모두 매칭될 수 없는 경우
            raise SyntaxError()

        return expr_tuple

    @staticmethod
    def typeCheck(obj_types: list[str], type_list: list[str]) -> bool:
        return not (
            False
            in [True if obj_type in type_list else False for obj_type in obj_types]
        )
