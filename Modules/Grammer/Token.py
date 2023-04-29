from typing import Optional


def Enumerater(*str_list: str) -> dict[str, int]:
    return {str_list[idx]: idx for idx in range(len(str_list))}


token: Optional[dict[str, int]] = None

with open("Modules/Grammer/tokens.txt", "r") as file:
    token = Enumerater(
        *[n for n, _ in [line.split() for line in file.read().split("\n")]]
    )
