from dataclasses import dataclass


@dataclass
class state:
    VarState: bool = False
    LoopState: bool = False
    IfState: bool = False
    IndentState: int = 0
    ExprState: bool = False

    ClassSet: set[str] = set()
    FuncSet: set[str] = set()
    VarSet: set[str] = set()
    StructSet: set[str] = set()
