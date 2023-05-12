from typing import Any
import Modules.Parser.Container as Container
import Modules.Parser.Expression as Expression
import Modules.Parser.Checker as Checker


class Object:
    @staticmethod
    def getVar(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
        if codes[idx][0] != "IDENTIFIER":
            raise SyntaxError()
        tree: dict[str, Any] = {}
        tree["Category"] = "Object"
        tree["ObjectType"] = "Var"
        tree["Name"] = codes[idx][1]
        return (tree, idx + 1)

    @staticmethod
    def getLiteral(
        codes: list[tuple[str, str]], idx: int
    ) -> tuple[dict[str, Any], int]:
        if codes[idx][0] not in ["NUMBER", "STRING", "BOOL"]:
            raise SyntaxError()
        tree: dict[str, Any] = {}
        tree["Category"] = "Object"
        tree["ObjectType"] = codes[idx][0]
        tree["Value"] = codes[idx][1]

        return (tree, idx + 1)

    @staticmethod
    def getKeyAndValue(
        codes: list[tuple[str, str]], idx: int
    ) -> tuple[dict[str, Any], int]:
        tree: dict[str, Any] = {}
        tree["Category"] = "Object"
        tree["ObjectType"] = "KeyAndValue"
        expr, idx = Checker.Checker.codeMatch(
            codes=codes,
            idx=idx,
            match_list=[
                Container.Container.getDict,
                Container.Container.getList,
                Container.Container.getTuple,
                Container.Container.getSet,
                Object.getLiteral,
                Object.getVar,
            ],
        )
        tree["Key"] = expr
        while codes[idx][0] != "COLON":
            if codes[idx][0] != "INDENT" or codes[idx][0] != "EOL":
                raise SyntaxError()
            idx += 1
        idx += 1
        while codes[idx][0] == "INDENT" or codes[idx][0] == "EOL":
            idx += 1
        expr, idx = Checker.Checker.codeMatch(
            codes=codes,
            idx=idx,
            match_list=[
                Container.Container.getDict,
                Container.Container.getList,
                Container.Container.getTuple,
                Container.Container.getSet,
                Object.getLiteral,
                Object.getVar,
                Expression.Expression.getExpr,
            ],
        )
        tree["Value"] = expr
        return (tree, idx)
