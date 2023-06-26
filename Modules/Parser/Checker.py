from typing import Callable, Any


def code_match(
    tokens: list[tuple[str, str]],
    idx: int,
    obj_list: list[
        Callable[[list[tuple[str, str]], int], tuple[dict[str, Any], int]]
    ] = [],
) -> tuple[dict[str, Any], int]:
    expr_tuple: tuple[dict[str, Any], int] = (dict(), -1)  # 표현식과 인덱스를 담을 튜플

    for object in obj_list:
        try:
            expr, _idx = object(tokens, idx)
            if _idx > expr_tuple[1]:  # 표현식이 더 많이 매칭된 경우
                expr_tuple = (expr, _idx)
        except:  # 매칭될 수 없는 경우
            pass
    if expr_tuple[1] == -1:  # 모두 매칭될 수 없는 경우
        raise SyntaxError()

    return expr_tuple


def typeCheck(obj_types: list[str], type_list: list[str]) -> bool:
    return not (False in [obj_type in type_list for obj_type in obj_types])
