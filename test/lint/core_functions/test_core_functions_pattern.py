import os
import yaml
import json

from graviteeio_cli.lint.gio_linter import Gio_linter
from graviteeio_cli.lint.types.document import Document, DocumentType
from graviteeio_cli.lint.functions.pattern import pattern

dir_name = os.path.abspath(".") + "/test"


def test_pattern():

    params = {
        "match": "[abc]+"
    }

    functionResult = pattern('abc', **params)
    assert len(functionResult) == 0


def test_pattern_with_flag():
    params = {
        "match": "[A-Z]",
        "match_flag": "i"
    }

    functionResult = pattern('abc', **params)
    assert len(functionResult) == 0


def test_pattern_with_match_and_no_match():
    params = {
        "match": "[def]",
        "no_match": "[abc]"
    }

    functionResult = pattern('def', **params)
    assert len(functionResult) == 0


def read_yml(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return yaml.load(file.read(), Loader=yaml.SafeLoader)


def read_json(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return json.loads(file.read())


def setup_linter(source, rule, document_type=DocumentType.oas):
    linter = Gio_linter()

    document = Document(source, document_type)

    linter.setRules(rule)

    diagResult = linter.run(document)

    return diagResult


def test_pattern_with_key():

    rule = {
        "path-keys-no-trailing-slash": {
            "description": "paths should not end with a slash.",
            "formats": ["oas3"],
            "severity": "Error",
            "query": "paths",
            "field": "@key",
            "validator": {
                "func": "pattern",
                "args": {
                    "notMatch": ".+\\/$"
                }
            }
        }
    }

    source = read_yml("petstore_spec_V3_0.yml")
    diagResult = setup_linter(source, rule)

    assert len(diagResult) == 0


def test_pattern_with_key_return_error():

    rule = {
        "path-keys-no-trailing-slash": {
            "description": "paths should not end with a slash.",
            "formats": ["oas3"],
            "severity": "Error",
            "query": "paths",
            "field": "@key",
            "validator": {
                "func": "pattern",
                "args": {
                    "notMatch": ".+\\/$"
                }
            }
        }
    }

    source = read_yml("petstore_spec_V3_0.yml")
    source["paths"]["/pets/"] = source["paths"]["/pets"]

    diagResult = setup_linter(source, rule)

    assert len(diagResult) == 1


def test_pattern_valide_target_api_def():

    rule = {
        "not-white-cards-for-cors ": {
            "description": "cors should not have white cards.",
            "formats": ["gio_apim"],
            "severity": "Error",
            "query": "proxy.cors.allowOrigin[*]",
            "validator": {
                "func": "pattern",
                "args": {
                    "notMatch": ".+\\/$"
                }
            }
        }
    }

    source = read_json("api_def.json")

    diagResult = setup_linter(source, rule, DocumentType.gio_apim)

    assert len(diagResult) == 1
