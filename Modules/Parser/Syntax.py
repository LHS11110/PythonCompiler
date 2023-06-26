from typing import Any
import Modules.Parser.Checker as Checker
import Modules.Parser.Container as Container
import Modules.Parser.Object as Object
import Modules.Parser.Expression as Expression


def getGenerator(
    tokens: list[tuple[str, str]],
    idx: int,
) -> tuple[dict[str, Any], int]:
    expr, idx = Checker.code_match(
        tokens=tokens,
        idx=idx,
        obj_list=Object.default_obj
        + Container.default_container
        + Expression.default_expression,
    )

    tree: dict[str, Any] = {}
    tree["Output"] = expr
    assert tokens[idx][0] == "FOR", ""
    idx += 1
    try:
        tree["Variables"], idx = Checker.code_match(
            tokens=tokens, idx=idx, obj_list=[Container.getList, Container.getTuple]
        )
    except:
        tree["Variables"], idx = Container.getEnum(
            tokens=tokens, idx=idx, obj_list=[Object.getVar]
        )
    if tree["Variables"]["ObjectType"] != "Enum":
        print(tree["Variables"])
        assert Checker.typeCheck(
            obj_types=[v["ObjectType"] for v in tree["Variables"]["Elements"]], type_list=["Var"]  # type: ignore
        ), ""
    assert tokens[idx][0] == "IN", ""
    idx += 1
    expr, idx = Checker.code_match(
        tokens=tokens,
        idx=idx,
        obj_list=Object.default_obj
        + Container.default_container
        + Expression.default_expression,
    )
    tree["Row"] = expr
    if tokens[idx][0] != "IF":
        return (tree, idx)
    idx += 1
    expr, idx = Checker.code_match(
        tokens=tokens,
        idx=idx,
        obj_list=Object.default_obj
        + Container.default_container
        + Expression.default_expression,
    )
    tree["Condition"] = expr
    return (tree, idx)
