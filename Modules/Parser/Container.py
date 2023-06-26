from typing import Any, Callable
import Modules.Parser.Checker as Checker
import Modules.Parser.Object as Object
import Modules.Parser.Expression as Expression


def getTuple(
    tokens: list[tuple[str, str]],
    idx: int,
) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    if tokens[idx][0] != "LPAREN":  # '(' 검사
        raise SyntaxError()
    idx += 1
    tree["Category"] = "Object"
    tree["ObjectType"] = "Tuple"
    tree["Elements"] = []
    count: int = 0  # 구분자와 표현식 순서를 파악하는데 사용할 변수
    while tokens[idx][0] != "RPAREN":  # ')'가 온다면
        if not count % 2:  # 표현식 검사
            element, idx = Checker.code_match(
                tokens=tokens,
                idx=idx,
                obj_list=Object.default_obj
                + default_container
                + Expression.default_expression,
            )
            tree["Elements"].append(element)  # type: ignore
            count += 1

        elif count % 2 and tokens[idx][0] != "COMMA":  # 구분자 검사
            raise SyntaxError()

        else:  # 구분자가 올바르다면
            idx += 1
            count += 1

    return (tree, idx + 1)


def getSet(
    tokens: list[tuple[str, str]],
    idx: int,
) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    if tokens[idx][0] != "LBRACE":
        raise SyntaxError()
    idx += 1
    tree["Category"] = "Object"
    tree["ObjectType"] = "Set"
    tree["Elements"] = []
    count: int = 0
    while tokens[idx][0] != "RBRACE":
        if not count % 2:
            element, idx = Checker.code_match(
                tokens=tokens,
                idx=idx,
                obj_list=Object.default_obj
                + default_container
                + Expression.default_expression,
            )
            tree["Elements"].append(element)  # type: ignore
            count += 1

        elif count % 2 and tokens[idx][0] != "COMMA":
            raise SyntaxError()

        else:
            idx += 1
            count += 1

    return (tree, idx + 1)


def getList(
    tokens: list[tuple[str, str]],
    idx: int,
) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    if tokens[idx][0] != "LSQB":
        raise SyntaxError()
    idx += 1
    tree["Category"] = "Object"
    tree["ObjectType"] = "List"
    tree["Elements"] = []
    count: int = 0
    while tokens[idx][0] != "RSQB":
        if not count % 2:
            element, idx = Checker.code_match(
                tokens=tokens,
                idx=idx,
                obj_list=Object.default_obj
                + default_container
                + Expression.default_expression,
            )
            tree["Elements"].append(element)  # type: ignore
            count += 1

        elif count % 2 and tokens[idx][0] != "COMMA":
            raise SyntaxError()

        else:
            idx += 1
            count += 1

    return (tree, idx + 1)


def getDict(
    tokens: list[tuple[str, str]],
    idx: int,
) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    if tokens[idx][0] != "LBRACE":
        raise SyntaxError()
    idx += 1
    tree["Category"] = "Object"
    tree["ObjectType"] = "Dict"
    tree["Elements"] = []
    count: int = 0

    def getKeyAndValue(
        tokens: list[tuple[str, str]],
        idx: int,
    ) -> tuple[dict[str, Any], int]:
        tree: dict[str, Any] = {}
        tree["Category"] = "Object"
        tree["ObjectType"] = "KeyAndValue"
        expr, idx = Checker.code_match(
            tokens=tokens,
            idx=idx,
            obj_list=Object.default_obj
            + default_container
            + Expression.default_expression,
        )
        tree["Key"] = expr
        assert tokens[idx][0] == "COLON", ""
        idx += 1
        expr, idx = Checker.code_match(
            tokens=tokens,
            idx=idx,
            obj_list=Object.default_obj
            + default_container
            + Expression.default_expression,
        )
        tree["Value"] = expr
        return (tree, idx)

    while tokens[idx][0] != "RBRACE":
        if not count % 2:
            element, idx = getKeyAndValue(tokens=tokens, idx=idx)
            tree["Elements"].append(element)  # type: ignore
            count += 1

        elif count % 2 and tokens[idx][0] != "COMMA":
            raise SyntaxError()

        else:
            idx += 1
            count += 1

    return (tree, idx + 1)


def getEnum(
    tokens: list[tuple[str, str]],
    idx: int,
    obj_list: list[
        Callable[
            [
                list[tuple[str, str]],
                int,
            ],
            tuple[dict[str, Any], int],
        ]
    ],
) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    tree["Category"] = "Object"
    tree["ObjectType"] = "Enum"
    tree["Elements"] = []
    count: int = 0
    error_idx: int = idx
    while True:
        if tokens[idx][0] == "INDENT":
            idx += 1

        elif not count % 2:
            try:
                element, idx = Checker.code_match(
                    tokens=tokens, idx=idx, obj_list=obj_list
                )
                tree["Elements"].append(element)  # type: ignore
                count += 1
            except:
                break

        elif count % 2 and tokens[idx][0] != "COMMA":
            break

        else:
            idx += 1
            count += 1
    if error_idx == idx:
        raise SyntaxError()
    return (tree, idx)


default_container: list[
    Callable[
        [
            list[tuple[str, str]],
            int,
        ],
        tuple[dict[str, Any], int],
    ]
] = [getTuple, getDict, getList, getSet]
