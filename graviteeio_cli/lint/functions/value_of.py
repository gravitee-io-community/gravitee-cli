from graviteeio_cli.lint.types.function_result import FunctionResult


def value_of(value: list, **kwargs):
    values = None

    if "values" in kwargs and type(kwargs["values"]) is list:
        values = kwargs["values"]

    results = []

    if value not in values:
        results.append(
            FunctionResult("{} is not a value of {}".format(value, values))
        )

    return results
