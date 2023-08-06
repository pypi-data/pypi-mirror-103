"""Write me."""
from __future__ import annotations

import inspect as inspect
import re as re
import subprocess

RE_LAMBDA_FUNC = re.compile(r".*(lambda)(.+?):(.*?)")
RE_LAMBDA_RATE_FUNC = re.compile(r".*(lambda)(.+?):(.*?),")
RE_LAMBDA_ALGEBRAIC_MODULE_FUNC = re.compile(r".*(lambda)(.+?):(.*[\(\[].+[\)\]]),")
RE_TO_SBML = re.compile(r"([^0-9_a-zA-Z])")
RE_FROM_SBML = re.compile(r"__(\d+)__")
SBML_DOT = "__SBML_DOT__"


def warning_on_one_line(message: str, category, filename: str, lineno: int, file=None, line=None):
    """Format warnings to only show the message."""
    return f"{category.__name__}: {message}\n"


##########################################################################
# Source code functions
##########################################################################


def get_function_source_code(function: callable) -> str:
    """Get source code of a function."""
    try:
        return inspect.getsource(function)[:-1]  # Remove line break
    except OSError:
        return function.__source__


def patch_lambda_function_name(function: callable, name: str):
    """Add a name to a lambda function."""
    if function.__name__ == "<lambda>":
        function.__name__ = name
    # function_source = get_function_source_code(function)
    # if "lambda" in function_source:
    # function.__name__ = name


def functionify_lambda(lambda_function_code: str, function_name: str, pattern: re.Pattern) -> str:
    """Convert lambda function to a proper function."""
    _, args, code = re.match(pattern=pattern, string=lambda_function_code).groups()
    return f"def {function_name}({args.strip()}):\n    return {code.strip()}"


def get_formatted_function_source_code(function_name: str, function: callable, function_type: str) -> str:
    """Get source code of a function and format it using black."""
    source = get_function_source_code(function=function)

    if "lambda" in source:
        if function_type == "rate":
            source = functionify_lambda(
                lambda_function_code=source,
                function_name=function_name,
                pattern=RE_LAMBDA_RATE_FUNC,
            )
        elif function_type == "module":
            source = functionify_lambda(
                lambda_function_code=source,
                function_name=function_name,
                pattern=RE_LAMBDA_ALGEBRAIC_MODULE_FUNC,
            )
        elif function_type == "function":
            source = functionify_lambda(
                lambda_function_code=source,
                function_name=function_name,
                pattern=RE_LAMBDA_FUNC,
            )
        else:
            raise ValueError("Can only handle rate or module functions")
    blacked_string = subprocess.run(["black", "-c", source], stdout=subprocess.PIPE)
    return blacked_string.stdout.decode("utf-8")[:-2]  # Removing new lines


##########################################################################
# SBML functions
##########################################################################


def escape_non_alphanumeric(re_sub: re.sub) -> str:
    """Convert a non-alphanumeric charactor to a string representation of its ascii number."""
    return f"__{ord(re_sub.group(0))}__"


def ascii_to_character(re_sub: re.sub) -> str:
    """Convert an escaped non-alphanumeric character."""
    return chr(int(re_sub.group(1)))


def convert_id_to_sbml(id_: str, prefix: str) -> str:
    """Add prefix if id startswith number."""
    new_id = RE_TO_SBML.sub(escape_non_alphanumeric, id_).replace(".", SBML_DOT)
    if not new_id[0].isalpha():
        return f"{prefix}_{new_id}"
    return new_id


def convert_sbml_id(sbml_id: str, prefix: str) -> str:
    """Convert an model object id to sbml-compatible string.

    Adds a prefix if the id starts with a number."""
    new_id = sbml_id.replace(SBML_DOT, ".")
    new_id = RE_FROM_SBML.sub(ascii_to_character, new_id)
    return new_id.lstrip(f"{prefix}_")
