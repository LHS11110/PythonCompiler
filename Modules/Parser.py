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


class Parser:
    def __init__(self) -> None:
        self._state: state = state()

    def cleanup(self, codes: list[tuple[str, str]]) -> list[tuple[str, str]]:
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

    def isEndOfLine(self, codes: list[tuple[str, str]]) -> bool:
        return codes[-1][0] == "EOL"
