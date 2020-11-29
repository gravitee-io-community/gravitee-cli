import os
import json
import yaml

from graviteeio_cli.lint.rulesets.oas.functions.oasOp2xxResponse import oasOp2xxResponse
from graviteeio_cli.lint.gio_linter import Gio_linter
from graviteeio_cli.lint.types.document import Document, DocumentType

dir_name = os.path.abspath(".") + "/test"


def read_json(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return json.loads(file.read())


def read_yml(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return yaml.load(file.read(), Loader=yaml.SafeLoader)


RULE = {
        "operation-singular-tag": {
            "description": "Operation must have at least one `2xx` response.",
            "formats": ["oas3"],
            "query": "paths.*.(get, put, post, delete, options, head, patch, trace)",
            "field": "responses",
            "severity": "Error",
            "validator": {
                "func": "oasOp2xxResponse",
            }
        }
    }


def test_Op2xxResponse():
    linter = Gio_linter()

    source = read_yml("petstore_spec_V3_0.yml")
    source["paths"]["/pets"]["get"]["operationId"] = "listPets"
    source["paths"]["/pets"]["post"]["operationId"] = "listPets"

    document = Document(source, DocumentType.oas)

    linter.setFunction(oasOp2xxResponse)
    linter.setRules(RULE)

    diagResult = linter.run(document)

    assert len(diagResult) == 0


def test_Op2xxResponse_with_error():
    linter = Gio_linter()

    source = read_yml("petstore_spec_V3_0.yml")
    response = source["paths"]["/pets"]["get"]["responses"]["200"]
    del(source["paths"]["/pets"]["get"]["responses"]["200"])
    source["paths"]["/pets"]["get"]["responses"]["300"] = response

    document = Document(source, DocumentType.oas)

    linter.setFunction(oasOp2xxResponse)
    linter.setRules(RULE)

    diagResult = linter.run(document)

    assert len(diagResult) == 1
    assert diagResult[0].path == ['paths', '/pets', 'get', 'responses']
