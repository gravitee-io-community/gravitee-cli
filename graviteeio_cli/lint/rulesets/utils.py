import os
import json

from graviteeio_cli.lint import rulesets


def get_schema(schema_file):
    schema_path = os.path.join(
        os.path.dirname(rulesets.__file__),
        schema_file
    )
    with open(schema_path) as f:
        schema = json.load(f)

    return schema
