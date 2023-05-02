from dataclasses import dataclass


@dataclass
class state:
    VarState: bool = False
    LoopState: bool = False
    IfState: bool = False
    IndentState: int = 0
    ExprState: bool = False
    DefState: bool = False
    EndOfLineState: bool = False  #

    ClassSet: set[str] = set()
    FuncSet: set[str] = set()
    VarSet: set[str] = set()
    StructSet: set[str] = set()
    StaticVarSet: set[str] = set()

    FuncStack: list[str] = []


class Parser:
    def __init__(self) -> None:
        self._state: state = state()

    def clean(self, codes: list[tuple[str, str]]) -> list[tuple[str, str]]:
        result: list[tuple[str, str]] = []
        self._state.EndOfLineState = True
        for code in codes:
            if code[0] == "INDENT" and self._state.EndOfLineState:
                result.append(code)
            elif code[0] == "EOL":
                result.append(code)
                self._state.EndOfLineState = True
            elif code[0] != "INDENT":
                result.append(code)
                self._state.EndOfLineState = False
        return result
