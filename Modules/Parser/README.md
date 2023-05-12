## 트리
Python의 딕셔너리 자료구조로 구현되며 파서로 인해 생성된 트리에는 Category와 ObjectType 멤버가 항상 있어야 한다.
### Category
해당 오브젝트의 큰 범주를 의미한다. 카테고리에는 `Object`와 `Expression`이 올 수 있다.
### ObjectType
오브젝트의 세부 카테고리를 의미한다. 역할이나 자료구조를 나타낼 수 있다.
### NextSyntax
`_ if _ else _` 연산자는 삼항 연산자와 같은 형태를 가지고 있다. 삼항 연산자는 문법이 여러개가 올 수 있기 때문에 `else`같은 문법이 온다면, 트리에 `NextSyntax` 리스트 멤버를 포함시키고 리스트에 다음에 올 수 있는 문법을 차례대로 append 한다.

예: 만약 삼항 연산자와 같은 역할을 하는 `_ if _ else _`의 경우, tree["NextSyntax"] = ["in"]