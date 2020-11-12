import os
import json
import yaml

import jsonpath_ng as jsonpath
from graviteeio_cli.lint.functions.length import lenght
from graviteeio_cli.lint.gio_linter import Gio_linter
from graviteeio_cli.lint.types.document import Document, DocumentType

dir_name = os.path.abspath(".") + "/test"


def read_json(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return json.loads(file.read())


def read_yml(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return yaml.load(file.read(), Loader=yaml.SafeLoader)


def test_lenght_max():
    linter = Gio_linter()

    source = read_yml("petstore_spec_V3_0.yml")
    document = Document(source, DocumentType.oas)

    linter.setValidator(lenght)
    linter.setRules({
        "operation-singular-tag": {
            "description": "Operation may only have one tag.",
            "message": "{error}, path: {path}",
            "formats": ["oas3"],
            "selector": "paths.*.(get, put, post, delete, options, head, patch, trace).tags",
            "severity": "Error",
            "validator": "lenght",
            "validator_args": {
                "max": 1
            }
        }
    })

    diagResult = linter.run(document)

    assert len(diagResult) == 0


def test_lenght_with_error():
    linter = Gio_linter()

    source = read_yml("petstore_spec_V3_0_with_error.yml")
    document = Document(source, DocumentType.oas)

    linter.setValidator(lenght)
    linter.setRules({
        "operation-singular-tag": {
            "description": "Operation may only have one tag.",
            "message": "{error}, path: {path}",
            "formats": ["oas3"],
            "severity": "Error",
            "selector": "paths.*.(get, put, post, delete, options, head, patch, trace)",
            "field": "tags",
            "validator": "lenght",
            "validator_args": {
                "max": 1,
                "min": 1
            }
        }
    })

    diagResult = linter.run(document)

    assert len(diagResult) == 2
    assert diagResult[0].path is not None
    assert diagResult[0].path == ['paths', '/pets', 'post', 'tags']
    assert diagResult[1].path == ['paths', '/pets/{petId}', 'get', 'tags']

def test_lenght_with_error():
    linter = Gio_linter()

    source = read_yml("petstore_spec_V3_0_with_error.yml")
    document = Document(source, DocumentType.oas)

    linter.setValidator(lenght)
    linter.setRules({
        "operation-singular-tag": {
            "description": "Operation may only have one tag.",
            "message": "{error}, path: {path}",
            "formats": ["oas3"],
            "severity": "Error",
            "selector": "paths.*.(get, put, post, delete, options, head, patch, trace)",
            "field": "tags",
            "validator": "lenght",
            "validator_args": {
                "min": 1
            }
        }
    })

    diagResult = linter.run(document)

    assert len(diagResult) == 1
    assert diagResult[0].path is not None
    assert diagResult[0].path == ['paths', '/pets', 'post', 'tags']


def test_length_function():
    query = "paths.*.(get, put, post, delete, options, head, patch, trace).tags"
    source = read_yml("petstore_spec_V3_0.yml")

    expression = jsonpath.parse(query)
    results = expression.find(source)

    toReturn = []
    for result in results:
        functionResult = lenght(result.value, min=2)
        toReturn.extend(functionResult)

    print(toReturn)
