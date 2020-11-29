import os
import json
import yaml

from graviteeio_cli.lint.rulesets.oas.functions.oasOpIdUnique import oasOpIdUnique
from graviteeio_cli.lint.gio_linter import Gio_linter
from graviteeio_cli.lint.types.document import Document, DocumentType

dir_name = os.path.abspath(".") + "/test"


def read_json(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return json.loads(file.read())


def read_yml(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return yaml.load(file.read(), Loader=yaml.SafeLoader)


def test_OpIdUnique():
    linter = Gio_linter()

    source = read_yml("petstore_spec_V3_0.yml")
    source["paths"]["/pets"]["get"]["operationId"] = "listPets"
    source["paths"]["/pets"]["post"]["operationId"] = "listPets"

    document = Document(source, DocumentType.oas)

    linter.setFunction(oasOpIdUnique)
    linter.setRules({
        "operation-singular-tag": {
            "description": "Every operation must have a unique `operationId`.",
            "message": "{error}, path: {path}",
            "formats": ["oas3"],
            "severity": "Error",
            "validator": {
                "func": "oasOpIdUnique",
            }
        }
    })

    diagResult = linter.run(document)

    assert len(diagResult) == 2
    assert diagResult[0].path == ['paths', '/pets', 'get', 'operationId']
    assert diagResult[1].path == ['paths', '/pets', 'post', 'operationId']
