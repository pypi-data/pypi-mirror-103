import unicodedata
from re import sub as re_sub
from typing import Any

from bleach import clean, linkify
from slugify import slugify

from .constants import CaseStyle
from .wrappers import validate_string


def process_case_style(case_style: str) -> str:
    style: str = (case_style or "").upper()

    if style not in CaseStyle.choices:
        raise ValueError(
            f"Invalid case style '{style}'. Choices are "
            f"{', '.join(CaseStyle.choices)}"
        )

    return style


@validate_string
def to_slug(string: str, lowercase: bool = True, separator: str = "-") -> str:
    return slugify(string, lowercase=lowercase, separator=separator)


@validate_string
def special_convert_case(string: str) -> str:
    if (
        all(
            unicodedata.category(char) in ("Ll", "Lu", "Lo") for char in string
        )
        and string.upper() == string
    ):
        return string.lower()
    return string


@validate_string
def to_pascal_case(string: str) -> str:
    string = re_sub(r"(\s|-)+", "_", string)
    string = re_sub(
        r"([0-9]+|\.)([a-zA-Z])([a-zA-Z])",
        lambda m: m.group(1) + m.group(2).upper() + m.group(3),
        string,
    )
    string = re_sub(
        r"(?:^|_+)([a-zA-Z])([a-zA-Z]*)",
        lambda m: m.group(1).upper() + special_convert_case(m.group(2)),
        string,
    )
    string = re_sub(
        r"(\.)([A-Z])([a-zA-Z0-9]*)",
        lambda m: m.group(1) + m.group(2).upper() + m.group(3),
        string,
    )
    return string[:1].upper() + string[1:]


@validate_string
def to_camel_case(string: str) -> str:
    string = re_sub(r"(\s|-)+", "_", string)
    string = re_sub(
        r"([0-9]+|\.)([a-zA-Z])([a-zA-Z])",
        lambda m: m.group(1) + m.group(2).upper() + m.group(3),
        string,
    )
    string = re_sub(
        r"(?:^|_+)([a-zA-Z])([a-zA-Z]*)",
        lambda m: m.group(1).upper() + special_convert_case(m.group(2)),
        string,
    )
    string = re_sub(
        r"(\.)([A-Z])([a-zA-Z0-9]*)",
        lambda m: m.group(1) + m.group(2).lower() + m.group(3),
        string,
    )
    return string[:1].lower() + string[1:]


@validate_string
def to_snake_case(string: str, screaming: bool = False) -> str:
    string = re_sub(r"\s+", "_", string.strip())
    string = re_sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", string)
    string = re_sub(r"([a-z\d])([A-Z])", r"\1_\2", string)
    string = re_sub(r"([a-z]+)([0-9]+)", r"\1_\2", string)
    string = re_sub(r"([0-9]+)([a-z]+)", r"\1_\2", string)
    string = string.replace("-", "_")
    return string.upper() if screaming else string.lower()


@validate_string
def to_kebab_case(string: str) -> str:
    return to_snake_case(string).replace("_", "-")


def convert_string_case(string: str, case_style: str = CaseStyle.CAMEL) -> str:
    case_style = process_case_style(case_style=case_style)
    kwargs = dict(string=string)
    if case_style == CaseStyle.SCREAMING_SNAKE:
        kwargs["screaming"] = True
        case_style = CaseStyle.SNAKE
    return globals()[f"to_{case_style.lower()}_case"](**kwargs)


def convert_dict_keys_case(obj: Any, case_style: str = CaseStyle.CAMEL):
    """
    This function recursively changes the case of all the keys in the obj
    argument
    """
    case_style = process_case_style(case_style=case_style)

    if isinstance(obj, (tuple, list)):
        return type(obj)(
            [convert_dict_keys_case(item, case_style) for item in obj]
        )
    elif isinstance(obj, dict):
        return {
            convert_string_case(key, case_style): convert_dict_keys_case(
                value, case_style
            )
            for key, value in obj.items()
            if key
        }
    else:
        return obj


@validate_string
def sanitize_string(string: str) -> str:
    """
    strip content of XSS markings
    :param string: string value to sanitize
    """
    return clean(string)
