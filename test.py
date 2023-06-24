from Modules.Parser import Parser
from Modules.Lexer import Lexer
from Modules.Parser import Container
from Modules.Parser import Object
from Modules.Parser import Expression
from Modules.Parser import Checker
from Modules.Parser import Syntax
from Modules.Parser.Expression import priority
import time

d: dict[int, int] = {}
s: float = time.time()
for i in range(10000000):
    d[i] = i
print(time.time() - s)
