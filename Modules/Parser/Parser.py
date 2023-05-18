class state:
    def __init__(self) -> None:
        self.VarState: bool = False
        self.LoopState: bool = False
        self.IfState: bool = False
        self.IndentState: int = 0
        self.ExprState: bool = False
        self.DefState: bool = False
        self.EndOfLineState: bool = False  #

        self.ClassSet: set[str] = set()
        self.FuncSet: set[str] = set()
        self.VarSet: set[str] = set()
        self.StructSet: set[str] = set()
        self.StaticVarSet: set[str] = set()

        self.FuncStack: list[str] = list()
        self.BracketStack: list[str] = list()  #


def cleanup(codes: list[tuple[str, str]]) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    _state: state = state()
    _state.EndOfLineState = True
    for code in codes:
        if (
            code[0] == "INDENT"
            and _state.EndOfLineState
            and len(_state.BracketStack) == 0
        ):
            result.append(code)
        elif code[0] == "EOL" and len(_state.BracketStack) == 0:
            result.append(code)
            _state.EndOfLineState = True
        elif code[0] in ["LSQB", "LBRACE", "LPAREN"]:
            result.append(code)
            _state.BracketStack.append(code[0])
        elif code[0] in ["RSQB", "RBRACE", "RPAREN"]:
            if _state.BracketStack[-1] != ("L" + code[0][1:]):
                raise SyntaxError()
            result.append(code)
            _state.BracketStack.pop()
        elif code[0] != "INDENT" and code[0] != "EOL":
            result.append(code)
            _state.EndOfLineState = False
    return result


def isEndOfLine(codes: list[tuple[str, str]]) -> bool:
    return codes[-1][0] == "EOL"
