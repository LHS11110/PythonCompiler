from dataclasses import dataclass, field


@dataclass
class state:
    VarState: bool = False
    LoopState: bool = False
    IfState: bool = False
    IndentState: int = 0
    ExprState: bool = False
    DefState: bool = False
    EndOfLineState: bool = False  #

    ClassSet: set[str] = field(default_factory=set)
    FuncSet: set[str] = field(default_factory=set)
    VarSet: set[str] = field(default_factory=set)
    StructSet: set[str] = field(default_factory=set)
    StaticVarSet: set[str] = field(default_factory=set)

    FuncStack: list[str] = field(default_factory=list)
    BracketStack: list[str] = field(default_factory=list)  #


def cleanup(tokens: list[tuple[str, str]]) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    _state: state = state()
    _state.EndOfLineState = True
    for token in tokens:
        if (
            token[0] == "INDENT"
            and _state.EndOfLineState
            and len(_state.BracketStack) == 0
        ):
            result.append(token)
        elif token[0] == "EOL" and len(_state.BracketStack) == 0:
            result.append(token)
            _state.EndOfLineState = True
        elif token[0] in ["LSQB", "LBRACE", "LPAREN"]:
            result.append(token)
            _state.BracketStack.append(token[0])
        elif token[0] in ["RSQB", "RBRACE", "RPAREN"]:
            if _state.BracketStack[-1] != ("L" + token[0][1:]):
                raise SyntaxError()
            result.append(token)
            _state.BracketStack.pop()
        elif token[0] != "INDENT" and token[0] != "EOL":
            result.append(token)
            _state.EndOfLineState = False
    return result


def isEOL(tokens: list[tuple[str, str]]) -> bool:
    return tokens[-1][0] == "EOL"
