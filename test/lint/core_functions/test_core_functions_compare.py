import os
import yaml
import json

from graviteeio_cli.lint.gio_linter import Gio_linter
from graviteeio_cli.lint.types.document import Document, DocumentType
from graviteeio_cli.lint.functions.compare import compare

dir_name = os.path.abspath(".") + "/test"


def test_compare_equ():

    params = {
        "equal": "abc"
    }

    functionResult = compare('abc', **params)
    assert len(functionResult) == 0

    params = {
        "equal": 12
    }

    functionResult = compare(12, **params)
    assert len(functionResult) == 0


def test_compare_notEqual():
    params = {
        "notEqual": "abcd",
    }

    functionResult = compare('abc', **params)
    assert len(functionResult) == 0

    params = {
        "notEqual": 123,
    }

    functionResult = compare(12, **params)
    assert len(functionResult) == 0


def read_json(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return json.loads(file.read())


def setup_linter(source, rule, document_type=DocumentType.oas):
    linter = Gio_linter()

    document = Document(source, document_type)

    linter.setRules(rule)

    diagResult = linter.run(document)

    return diagResult


def test_pattern_valide_target_api_def():

    rule = {
        "not-white-cards-for-cors ": {
            "description": "cors should not have white cards.",
            "formats": ["gio_apim"],
            "severity": "Error",
            "query": "proxy.cors.allowOrigin[*]",
            "validator": {
                "func": "compare",
                "args": {
                    "notEqual": "'*'"
                }
            }
        }
    }

    source = read_json("api_def.json")

    diagResult = setup_linter(source, rule, DocumentType.gio_apim)

    assert len(diagResult) == 1
