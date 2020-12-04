from graviteeio_cli.lint.types.function_result import FunctionResult


def undefined(value, **kwargs):
    results = []
    if value is not None:
        results.append(FunctionResult("{field} is not empty"))

    return results
