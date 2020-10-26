from graviteeio_cli.lint.rulesets.utils import get_schema
from graviteeio_cli.lint.types.function_result import FunctionResult

from jsonschema import Draft7Validator, RefResolver


def gio_apim_Document_Schema(value, **kwargs):
    schema_file = kwargs["schema"]
    schema = get_schema(schema_file)

    api_entity_schema = schema['components']['schemas']['UpdateApiEntity']
    resolver = RefResolver.from_schema(schema)

    validator = Draft7Validator(api_entity_schema, resolver=resolver)
    # errors = sorted(validator.iter_errors(value), key=lambda e: e.path)

    return list(map(lambda error: FunctionResult(error.message, error.path), validator.iter_errors(value)))
