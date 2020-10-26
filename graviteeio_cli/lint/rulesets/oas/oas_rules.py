from graviteeio_cli.lint.types.enums import DiagSeverity
from .functions.oasDocumentSchema import oasDocumentSchema

oas_rules = {
    "formats": ["oas2", "oas3"],
    "functions": [
        oasDocumentSchema
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
        }
    }
}
