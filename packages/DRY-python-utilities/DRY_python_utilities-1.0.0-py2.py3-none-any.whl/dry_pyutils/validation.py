from json import JSONDecodeError, loads as json_loads
from uuid import UUID

from .constants import CaseStyle
from .transformation import convert_string_case, to_slug
from .wrappers import validate_string


def eval_expression(string: str):
    code = compile(string, "<string>", "eval")
    if code.co_names:
        raise NameError(f"Use of names not allowed")
    return eval(code, {"__builtins__": {}}, {})


@validate_string
def is_palindrome(string: str) -> bool:
    return string.lower() == string[::-1].lower()


def is_slug(string: str) -> bool:
    return string == to_slug(string)


def is_camel_case(string: str) -> bool:
    return string == convert_string_case(string, CaseStyle.CAMEL)


def is_pascal_case(string: str) -> bool:
    return string == convert_string_case(string, CaseStyle.PASCAL)


def is_kebab_case(string: str) -> bool:
    return string == convert_string_case(string, CaseStyle.KEBAB)


def is_snake_case(string: str) -> bool:
    return string == convert_string_case(string, CaseStyle.SNAKE)


@validate_string
def is_integer(string: str) -> bool:
    try:
        return isinstance(eval_expression(string), int)
    except Exception:
        return False


@validate_string
def is_float(string: str) -> bool:
    try:
        return isinstance(eval_expression(string), float)
    except Exception:
        return False


@validate_string
def is_number(string: str) -> bool:
    return is_integer(string) or is_float(string)


@validate_string
def is_json_string(string: str) -> bool:
    try:
        return isinstance(json_loads(string), (list, dict))
    except (TypeError, ValueError, JSONDecodeError):
        return False


@validate_string
def is_uuidv4_string(string: str) -> bool:
    try:
        UUID(string)
        return True
    except (TypeError, AttributeError, ValueError):
        return False
