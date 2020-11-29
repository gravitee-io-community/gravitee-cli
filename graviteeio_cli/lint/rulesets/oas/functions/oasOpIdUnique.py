from graviteeio_cli.lint.types.function_result import FunctionResult


def oasOpIdUnique(value, **kwargs):
    toReturn = []

    operationList = {}

    for path in value["paths"]:
        for verbe, operation_obj in value["paths"][path].items():
            if "operationId" in operation_obj:
                if operation_obj["operationId"] not in operationList:
                    operationList[operation_obj["operationId"]] = []

                operationList[operation_obj["operationId"]].append({
                    "path": ["paths", path, verbe, "operationId"],
                    "operationId": operation_obj["operationId"]
                })

    for operation in operationList.values():
        if len(operation) > 1:
            for op in operation:
                toReturn.append(FunctionResult(
                    "operationId must be unique. {} operationId [{}] found"
                        .format(len(operation), op["operationId"]),
                    op["path"]))

    # FunctionResult(''operationId must be unique'', error.path)
    # expression = jsonpath.parse("paths.*.*.operationId")
    # print(expression)
            # values = expression.find(value)
            # for value in values:
            #     targets.append({
            #         "path": convert_to_path_array(value.full_path),
            #         "value": value.value
            #     })

            # if len(values) == 0:
            #     targets.append({
            #         "path": [],
            #         "value": None
            #     })

    # unique

    return toReturn