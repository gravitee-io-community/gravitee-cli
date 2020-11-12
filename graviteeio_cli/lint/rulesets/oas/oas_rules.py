from graviteeio_cli.lint.types.enums import DiagSeverity
from .functions.oasDocumentSchema import oasDocumentSchema
from .functions.oasExtGravitee import oasExtGravitee

oas_rules = {
    "formats": ["oas2", "oas3"],
    "functions": [
        oasDocumentSchema,
        oasExtGravitee
    ],
    "rules": {
        "oas2-schema": {
            "description": "Validate structure of OpenAPI v2 specification.",
            "message": "{error}, path: {path}",
            "formats": ["oas2"],
            "severity": "Error",
            "validator": "oasDocumentSchema",
            "validator_args": {
                "schema": "oas/schemas/schema_oas2.json"
            }
        },
        "oas3-schema": {
            "description": "Validate structure of OpenAPI v3 specification.",
            "message": "{error}, path: {path}",
            "formats": ["oas3"],
            "severity": "Error",
            "validator": "oasDocumentSchema",
            "validator_args": {
                "schema": "oas/schemas/schema_oas3.json"
            }
        },
        "x-gravitee-schema": {
            "description": "Validate x-gravitee specification.",
            "message": "{error}",
            "formats": ["oas2", "oas3"],
            "severity": "Error",
            "validator": "oasExtGravitee",
            "validator_args": {
                "schema": "oas/schemas/ext_gravitee/xGraviteeIODefinition.json"
            }
        }
    }
}
