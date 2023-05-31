from typing import Any
import Modules.Parser.Checker as Checker
import Modules.Parser.Container as Container
import Modules.Parser.Object as Object


def getGenerator(
    codes: list[tuple[str, str]],
    idx: int,
) -> tuple[dict[str, Any], int]:
    expr, idx = Checker.code_match(
        codes=codes,
        idx=idx,
        obj_list=[
            Object.getLiteral,
            Object.getVar,
            Container.getDict,
            Container.getList,
            Container.getSet,
            Container.getTuple,
        ],
    )

    tree: dict[str, Any] = {}
    tree["Output"] = expr
    assert codes[idx][0] == "FOR", ""
    idx += 1
    tree["Variables"], idx = Checker.code_match(
        codes=codes,
        idx=idx,
        obj_list=[
            Object.getLiteral,
            Object.getVar,
            Container.getList,
            Container.getTuple,
        ],
    )
    if tree["Variables"]["ObjectType"] != "Var":
        assert Checker.typeCheck(
            obj_types=[obj["ObjectType"] for obj in tree["Variables"]["Elements"]],
            type_list=["Var"],
        ), ""
        tree["Variables"] = tree["Variables"]["Elements"]
    else:
        tree["Variables"] = [tree["Variables"]]
    assert codes[idx][0] == "IN", ""
    idx += 1
    expr, idx = Checker.code_match(
        codes=codes,
        idx=idx,
        obj_list=Object.default_obj + Container.default_container,
    )
    tree["Row"] = expr
    if codes[idx][0] != "IF":
        return (tree, idx)
    idx += 1
    expr, idx = Checker.code_match(
        codes=codes,
        idx=idx,
        obj_list=Object.default_obj + Container.default_container,
    )
    tree["Condition"] = expr
    return (tree, idx)


def initialization(
    codes: list[tuple[str, str]], idx: int
) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    return (tree, idx)
