from graviteeio_cli.lint.types.function_result import FunctionResult


def starts_with(value: str, **kwargs):
    string = None
    if "str" in kwargs and type(kwargs["str"]) is str and value and type(value) is str:
        string = kwargs["str"]

    results = []

    if not value.startswith(string):
        results.append(
            FunctionResult("must be started by {}".format(string))
        )

    return results
