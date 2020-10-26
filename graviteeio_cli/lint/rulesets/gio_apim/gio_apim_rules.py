from graviteeio_cli.lint.rulesets.gio_apim.functions.gioApimDocumentSchema import gio_apim_Document_Schema

gio_apim_rules = {
    "formats": ["gio_apim"],
    "functions": [
        gio_apim_Document_Schema
    ],
    "rules": {
        "gio_apim-schema": {
            "description": "Validate structure of gio apim api specification.",
            "message": "{error}, path: {path}",
            "formats": ["gio_apim"],
            "severity": "Error",
            "validator": "gio_apim_Document_Schema",
            "validator_args": {
                "schema": "gio_apim/schemas/schema_gio_apimv3.json"
            }
        }
    }
}
