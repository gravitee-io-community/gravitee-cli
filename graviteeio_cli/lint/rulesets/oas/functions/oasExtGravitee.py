from graviteeio_cli.lint.functions.schema import schema


def oasExtGravitee(value, **kwargs):
    toReturn = []
    if value is not None and type(value) is dict and "x-graviteeio-definition" in value:
        source = value["x-graviteeio-definition"]
        toReturn = schema(source, **kwargs)

    if toReturn and len(toReturn) > 0:
        for returnFunction in toReturn:
            # newPath = ["x-graviteeio-definition"].extend(returnFunction.path)
            newPath = ["x-graviteeio-definition"]
            if returnFunction.path:
                newPath.extend(returnFunction.path)
            returnFunction.path = newPath

    return toReturn
