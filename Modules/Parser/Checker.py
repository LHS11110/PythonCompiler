from typing import Callable, Any


def object_match(
    codes: list[tuple[str, str]],
    idx: int,
    obj_list: list[Callable[[list[tuple[str, str]], int], tuple[dict[str, Any], int]]],
) -> tuple[dict[str, Any], int]:
    expr_tuple: tuple[dict[str, Any], int] = (dict(), -1)  # 표현식과 인덱스를 담을 튜플

    for object in obj_list:
        try:
            expr, _idx = object(codes, idx)
            if _idx > expr_tuple[1]:  # 표현식이 더 많이 매칭된 경우
                expr_tuple = (expr, _idx)
        except:  # 매칭될 수 없는 경우
            pass
    if expr_tuple[1] == -1:  # 모두 매칭될 수 없는 경우
        raise SyntaxError()

    return expr_tuple


def container_match(
    codes: list[tuple[str, str]],
    idx: int,
    container_list: list[
        Callable[
            [
                list[tuple[str, str]],
                int,
            ],
            tuple[dict[str, Any], int],
        ]
    ],
) -> tuple[dict[str, Any], int]:
    expr_tuple: tuple[dict[str, Any], int] = (dict(), -1)  # 표현식과 인덱스를 담을 튜플
    for container in container_list:
        try:
            expr, _idx = container(codes, idx)
            if _idx > expr_tuple[1]:  # 표현식이 더 많이 매칭된 경우
                expr_tuple = (expr, _idx)
        except:  # 매칭될 수 없는 경우
            pass
    if expr_tuple[1] == -1:  # 모두 매칭될 수 없는 경우
        raise SyntaxError()

    return expr_tuple


def code_match(
    codes: list[tuple[str, str]],
    idx: int,
    container_list: list[
        Callable[
            [
                list[tuple[str, str]],
                int,
            ],
            tuple[dict[str, Any], int],
        ]
    ],
    obj_list: list[Callable[[list[tuple[str, str]], int], tuple[dict[str, Any], int]]],
) -> tuple[dict[str, Any], int]:
    assert obj_list or container_list, ""  #  두 컨테이너가 모두 비어있다면 에러처리
    tree: dict[str, Any] = {}
    if obj_list:  # obj 매치 리스트가 비어있지 않다면
        try:
            tree, idx = object_match(codes=codes, idx=idx, obj_list=obj_list)
        except:
            pass
    if container_list:  # container 매치 리스트가 비어있지 않다면
        try:
            tree, idx = container_match(
                codes=codes,
                idx=idx,
                container_list=container_list,
            )
        except:
            pass
    assert tree, ""  # 매칭된 경우가 없다면 에러처리
    return (tree, idx)


def typeCheck(obj_types: list[str], type_list: list[str]) -> bool:
    return False in [obj_type in type_list for obj_type in obj_types]
