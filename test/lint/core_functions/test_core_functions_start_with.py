import json
import os

from graviteeio_cli.lint.functions.starts_with import starts_with
from graviteeio_cli.lint.gio_linter import Gio_linter
from graviteeio_cli.lint.types.document import Document, DocumentType


def test_start_with():
    functionResult = starts_with("https://www.test.com", str="https")
    assert len(functionResult) == 0

    functionResult = starts_with("http://www.test.com", str="https")
    assert len(functionResult) == 1


dir_name = os.path.abspath(".") + "/test"


def read_json(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return json.loads(file.read())


def setup_linter(source, rule):
    linter = Gio_linter()

    document = Document(source, DocumentType.gio_apim)

    linter.setRules(rule)
    diagResult = linter.run(document)

    return diagResult


def test_rule_start_with():

    rule = {
        "target-with-https": {
            "description": "target should start with https.",
            "formats": ["gio_apim"],
            "severity": "Error",
            "query": "proxy.groups[*].endpoints[*]",
            "field": "target",
            "validator": {
                "func": "starts_with",
                "args": {
                    "str": "https"
                }
            }
        }
    }

    source = read_json("api_def.json")
    diagResult = setup_linter(source, rule)

    assert len(diagResult) == 0
