from typing import List


class CaseStyle:
    CAMEL: str = "CAMEL"
    PASCAL: str = "PASCAL"
    SNAKE: str = "SNAKE"
    SCREAMING_SNAKE: str = "SCREAMING_SNAKE"
    KEBAB: str = "KEBAB"

    choices: List[str] = [CAMEL, PASCAL, KEBAB, SNAKE, SCREAMING_SNAKE]
