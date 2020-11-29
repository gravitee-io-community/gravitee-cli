
from graviteeio_cli.lint.types.function_result import FunctionResult


def oasOp2xxResponse(value, **kwargs):
    toReturn = []

    for response in value.keys():
        if response == "default":
            continue
        if not (int(response) >= 200 and int(response) < 300):
            toReturn.append(FunctionResult(
                "operations must define at least one 2xx response"
            ))

    return toReturn
