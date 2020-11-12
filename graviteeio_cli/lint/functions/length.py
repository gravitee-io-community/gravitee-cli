from graviteeio_cli.lint.types.function_result import FunctionResult


def lenght(value, **kwargs):
    """Count the length of a string an or array, the number of properties in an object, or a numeric value, and define minimum and/or maximum values."""

    min = None
    max = None
    if "min" in kwargs and type(kwargs["min"]) is int:
        min = kwargs["min"]

    if "max" in kwargs and type(kwargs["max"]) is int:
        max = kwargs["max"]

    value_length = 0
    if value:
        if type(value) is (int or float):
            value_length = value
        else:
            value_length = len(value)

    results = []

    if min and value_length < min:
        results.append(
            FunctionResult("min length is {}".format(min))
        )

    if max and value_length > max:
        results.append(
            FunctionResult("max length is {}".format(max))
        )

    return results
