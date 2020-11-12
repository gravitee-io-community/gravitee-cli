from graviteeio_cli.lint.functions.schema import schema


def oasDocumentSchema(value, **kwargs):
    return schema(value, **kwargs)
