import os
import json
import yaml

from graviteeio_cli.lint.functions.defined import defined
from graviteeio_cli.lint.gio_linter import Gio_linter
from graviteeio_cli.lint.types.document import Document, DocumentType

dir_name = os.path.abspath(".") + "/test"


def read_json(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return json.loads(file.read())


def read_yml(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return yaml.load(file.read(), Loader=yaml.SafeLoader)


def get_source():
    return read_yml("petstore_spec_V3_0.yml")


def setup_linter(source, rule):
    linter = Gio_linter()

    document = Document(source, DocumentType.oas)

    linter.setFunction(defined)
    linter.setRules(rule)

    diagResult = linter.run(document)

    return diagResult


def test_defined():

    rule = {
        "contact-properties": {
            "description": "Contact object should have `name`",
            "formats": ["oas3"],
            "severity": "Error",
            "query": "info.contact",
            "field": "name",
            "validator": {
                "func": "defined"
            }
        }
    }

    diagResult = setup_linter(get_source(), rule)

    assert len(diagResult) == 0


def test_defined_with_error_empty_contact_field():

    rule = {
        "contact-properties": {
            "description": "Contact object should have `email`",
            "formats": ["oas3"],
            "query": "info.contact",
            "field": "email",
            "severity": "Error",
            "validator": {
                "func": "defined"
            }
        }
    }
    source = get_source()

    diagResult = setup_linter(source, rule)

    assert len(diagResult) == 1
    assert diagResult[0].message == "Contact object should have `email`"

    source["info"]["contact"]["name"] = "Gravitee Team"

    diagResult = setup_linter(source, rule)

    assert len(diagResult) == 1
    assert diagResult[0].message == "Contact object should have `email`"

    source["info"]["contact"]["email"] = ""

    diagResult = setup_linter(source, rule)

    assert len(diagResult) == 1
    assert diagResult[0].message == "Contact object should have `email`"
