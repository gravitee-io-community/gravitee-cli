import os
import json
import yaml

from graviteeio_cli.lint.functions.casing import casing
from graviteeio_cli.lint.gio_linter import Gio_linter
from graviteeio_cli.lint.types.document import Document, DocumentType

dir_name = os.path.abspath(".") + "/test"


def read_json(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return json.loads(file.read())


def read_yml(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return yaml.load(file.read(), Loader=yaml.SafeLoader)


def setup_linter(file_name, rule):
    linter = Gio_linter()

    source = read_yml(file_name)
    document = Document(source, DocumentType.oas)

    linter.setFunction(casing)
    linter.setRules(rule)

    diagResult = linter.run(document)

    return diagResult


def test_casing():
    rule = {
        "camel-case-name": {
            "description": "Title should be camelCased",
            "formats": ["oas3"],
            "query": "info.title",
            "severity": "Error",
            "validator": {
                "func": "casing",
                "args": {
                    "type": "camel"
                }
            }
        }
    }

    diagResult = setup_linter("petstore_spec_V3_0.yml", rule)

    assert len(diagResult) == 1
    assert diagResult[0].message == "Title should be camelCased"
    assert diagResult[0].path is not None


def test_camel_case():
    type_case = "camel"

    functionResult = casing("test", type=type_case)
    assert len(functionResult) == 0

    functionResult = casing("testTest", type=type_case)
    assert len(functionResult) == 0

    functionResult = casing("test Test", type=type_case)
    assert len(functionResult) == 1

    functionResult = casing("test_Test", type=type_case)
    assert len(functionResult) == 1

    functionResult = casing("test-Test", type=type_case)
    assert len(functionResult) == 1

def test_snake_case():
    type_case = "snake"

    functionResult = casing("test", type=type_case)
    assert len(functionResult) == 0

    functionResult = casing("testTest", type=type_case)
    assert len(functionResult) == 1

    functionResult = casing("test Test", type=type_case)
    assert len(functionResult) == 1

    functionResult = casing("test_Test", type=type_case)
    assert len(functionResult) == 1

    functionResult = casing("test_test", type=type_case)
    assert len(functionResult) == 0

    functionResult = casing("test-Test", type=type_case)
    assert len(functionResult) == 1
