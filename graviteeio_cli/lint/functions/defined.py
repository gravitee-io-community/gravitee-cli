from graviteeio_cli.lint.types.function_result import FunctionResult


def defined(value, **kwargs):
    results = []
    if value is None:
        results.append(FunctionResult("{field} is empty"))

    if type(value) is str:
        newvalue = value.strip()
        if len(newvalue) == 0:
            results.append(FunctionResult("{field} is empty"))

    return results
