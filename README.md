# PythonCompiler
파이썬을 C++로 컴파일하는 컴파일러이다. 컴파일 과정은 아래와 같다.

1. Lexer가 Tokenize의 역할을 하는 동시에 분석하여 토큰열 반환
2. Parser가 딕셔너리 자료형으로 구현된 트리 반환
3. Compiler가 트리를 C++ 코드로 변환
4. Make 빌드 도구를 활용하여 변환된 C++ 코드를 컴파일한다.