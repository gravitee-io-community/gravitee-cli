from graviteeio_cli.lint.types.function_result import FunctionResult


def compare(value: str, **kwargs):
    results = []

    equal = None
    notEqual = None

    if "equal" in kwargs:
        equal = kwargs["equal"]

    if "notEqual" in kwargs:
        notEqual = kwargs["notEqual"]

    if value and equal and value != equal:
        results.append(
            FunctionResult("must be equal to {}".format(equal))
        )

    if value and notEqual and value == notEqual:
        results.append(
            FunctionResult("must not be equal to {}".format(notEqual))
        )

    return results
