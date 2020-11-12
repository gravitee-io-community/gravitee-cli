from graviteeio_cli.lint.rulesets.utils import get_schema
from graviteeio_cli.lint.types.function_result import FunctionResult
from jsonschema import validators


def schema(value, **kwargs):
    schema_file = kwargs["schema"]
    schema = get_schema(schema_file)

    cls = validators.validator_for(schema)
    validator = cls(schema)

    errors = validator.iter_errors(value)
    # for error in errors:
    #     print(error.path)
    return list(map(lambda error: FunctionResult(error.message, error.path), errors))
