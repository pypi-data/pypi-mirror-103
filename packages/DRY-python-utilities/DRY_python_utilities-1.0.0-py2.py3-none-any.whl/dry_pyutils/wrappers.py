from functools import wraps


def validate_string(f):
    @wraps(f)
    def wrapper(string, *args, **kwargs):
        if not isinstance(string, str):
            raise ValueError(f"Invalid string {string}")
        return f(string, *args, **kwargs)

    return wrapper
