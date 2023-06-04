from typing import Any, Callable
import Modules.Parser.Checker as Checker
import Modules.Parser.Container as Container
import Modules.Parser.Object as Object

# 연산자 우선순위
priority: dict[str, list[list[str]]] = {}
with open("Grammer/priority.txt", "r") as file:
    category: str = ""
    for line in file.read().split("\n"):
        word_list: list[str] = line.split()
        if len(word_list) == 1:
            category = word_list[0]
            priority[category] = []
        elif len(word_list) > 1:
            priority[category].append(list(value for value in word_list))


def getIndexing(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    assert codes[idx][0] == "LSQB", ""
    idx += 1
    tree: dict[str, Any] = {}
    tree["Category"] = "Expression"
    tree["ObjectType"] = "Indexing"
    tree["Elements"] = []
    count: int = 0
    while codes[idx][0] != "RSQB":
        if not count % 2:
            if codes[idx][0] == "COLON":  # 슬라이싱에서 객체가 생략됬다면
                tree["Elements"].append({})  # type: ignore
            else:
                element, idx = Checker.code_match(
                    codes=codes,
                    idx=idx,
                    obj_list=Object.default_obj + Container.default_container,
                )
                tree["Elements"].append(element)  # type: ignore
            count += 1

        elif count % 2 and codes[idx][0] != "COLON":
            raise SyntaxError()

        else:
            idx += 1
            count += 1
    if not count % 2:  # 마지막 객체가 생략됬다면
        tree["Elements"].append({})  # type: ignore
    assert not (len(tree["Elements"]) == 0 or len(tree["Elements"]) > 3), ""
    if len(tree["Elements"]) > 1:
        if len(tree["Elements"]) == 2:
            tree["Elements"].append({})  # type: ignore
        tree["ObjectType"] = "Slicing"
    return (tree, idx + 1)


def getCall(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    expr, idx = Checker.code_match(
        codes=codes,
        idx=idx,
        obj_list=[
            Container.getTuple,
        ],
    )
    tree["Category"] = "Expression"
    tree["ObjectType"] = "Call"
    tree["Elements"] = expr["Elements"]
    return (tree, idx)


def getTernaryOp(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    tree["Category"] = "Expression"
    tree["ObjectType"] = "TernaryOp"
    for op, next_syntax, _priority in priority["TernaryOperator"]:
        if codes[idx][0] == op:
            tree["Op"] = op
            tree["NextSyntax"] = [next_syntax]
            tree["Priority"] = int(_priority)
            break
    else:
        raise SyntaxError()

    return (tree, idx + 1)


def getBinaryOp(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    tree["Category"] = "Expression"
    tree["ObjectType"] = "BinaryOp"
    for op, _priority in priority["BinaryOperator"]:
        if codes[idx][0] == op:
            tree["Op"] = op
            tree["Priority"] = int(_priority)
            break
    else:
        raise SyntaxError()

    return (tree, idx + 1)


def getPostUnaryOp(
    codes: list[tuple[str, str]], idx: int
) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    tree["Category"] = "Expression"
    tree["ObjectType"] = "PostUnaryOp"
    expr, idx = Checker.code_match(
        codes=codes,
        idx=idx,
        obj_list=[
            getCall,
            getIndexing,
        ],
    )

    for op, _priority in priority["PostUnaryOperator"]:
        if expr["ObjectType"] == op:
            tree["Op"] = op
            tree["Priority"] = int(_priority)
            tree["Elements"] = expr["Elements"]
            break
    else:
        raise SyntaxError()

    return (tree, idx)


def getPreUnaryOp(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    tree: dict[str, Any] = {}
    tree["Category"] = "Expression"
    tree["ObjectType"] = "PreUnaryOp"
    for op, _priority in priority["PreUnaryOperator"]:
        if codes[idx][0] == op:
            tree["Op"] = op
            tree["Priority"] = int(_priority)
            break
    else:
        raise SyntaxError()

    return (tree, idx + 1)


def getOperand(codes: list[tuple[str, str]], idx: int) -> tuple[dict[str, Any], int]:
    tree, idx = Checker.code_match(
        codes=codes,
        idx=idx,
        obj_list=Object.default_obj + Container.default_container,
    )

    return (tree, idx)


def getExpr(
    codes: list[tuple[str, str]],
    idx: int,
) -> tuple[dict[str, Any], int]:
    stack: list[dict[str, Any]] = []
    tree: dict[str, Any] = {}
    syntax_stack: list[tuple[str, str]] = []
    syntax_check_stack: list[str] = []
    tree["Category"] = "Expression"
    tree["ObjectType"] = "Expr"
    tree["ExprList"] = []
    state: int = 0

    def syntax_check(expr: dict[str, Any]) -> bool:
        if "NextSyntax" in expr:
            return expr["NextSyntax"] == syntax_check_stack[-len(expr["NextSyntax"]) :]
        return True

    def push(expr: dict[str, Any]) -> None:
        while True:
            if len(stack) == 0:  # 스택이 비었다면
                stack.append(expr)
                break
            elif stack[-1]["Op"] == "LPAREN":  # 이미 들어있는 연산자가 괄호라면
                stack.append(expr)
                break
            elif (
                stack[-1]["Priority"] <= expr["Priority"]
            ):  # 이미 들어있는 연산자의 우선순위가 더 높거나 같다면
                if syntax_check(stack[-1]):
                    tree["ExprList"].append(stack[-1])
                else:
                    raise SyntaxError()
                stack.pop()
            else:  # 현재 연산자의 우선순위가 더 높다면
                stack.append(expr)
                break

    while True:
        if state == 0:  # 전위 단항 또는 피연산자
            if codes[idx][0] == "LPAREN":
                stack.append({"Op": "LPAREN"})
                idx += 1
                continue
            try:
                expr, idx = getPreUnaryOp(codes=codes, idx=idx)
                stack.append(expr)
                state = 0
            except:
                expr, idx = getOperand(codes=codes, idx=idx)
                tree["ExprList"].append(expr)  # type: ignore
                state = 1
        elif state == 1:  # 후위 단항 또는 next_syntax
            if len(syntax_stack) > 0:
                if codes[idx][0] == syntax_stack[-1][1]:  # 토큰이 n항 연산자의 다음 문법과 동일한 경우
                    state = 0
                    syntax_check_stack.append(codes[idx][0])
                    idx += 1
                    while len(stack) > 0:
                        if (
                            syntax_stack[-1][0] == stack[-1]["Op"]
                        ):  # next_syntax가 prev_syntax를 만날 때까지 스택의 연산자들을 전부 postfix 스택에 넣는다.
                            break
                        tree["ExprList"].append(stack.pop())  # type: ignore
                    syntax_stack.pop()
                    continue
            if codes[idx][0] == "RPAREN":
                while stack[-1]["Op"] != "LPAREN":
                    tree["ExprList"].append(stack.pop())  # type: ignore
                idx += 1
                stack.pop()
                continue
            try:
                expr, idx = getPostUnaryOp(codes=codes, idx=idx)
                push(expr=expr)
                state = 1
            except:
                state = 2
        elif state == 2:  # 이항 또는 삼항 연산자
            try:
                expr, idx = getBinaryOp(codes=codes, idx=idx)
                push(expr=expr)
            except:
                try:
                    expr, idx = getTernaryOp(codes=codes, idx=idx)
                    push(expr=expr)
                    syntax_list = [expr["Op"], *expr["NextSyntax"]]
                    syntax_list = [
                        (syntax_list[i], syntax_list[i + 1])
                        for i in range(len(syntax_list) - 1)
                    ]
                    for syntax in reversed(syntax_list):
                        syntax_stack.append(syntax)
                except:
                    break
            state = 0
    for op in reversed(stack):
        assert syntax_check(op), ""
        tree["ExprList"].append(op)  # type: ignore

    assert len(syntax_stack) == 0, ""
    return (tree, idx)


default_expression: list[
    Callable[[list[tuple[str, str]], int], tuple[dict[str, Any], int]]
] = [getExpr]
