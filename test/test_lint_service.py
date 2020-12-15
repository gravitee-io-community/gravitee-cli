import yaml
import os

from graviteeio_cli.services import lint_service
from graviteeio_cli.lint.types.document import DocumentType


dir_name = os.path.abspath(".") + "/test"


def read_yml(file_name):
    with open("{}/resources/{}".format(dir_name, file_name)) as file:
        return yaml.load(file.read(), Loader=yaml.SafeLoader)


def test_lint_service():
    api_spec = read_yml("petstore_spec.yml")

    assert not lint_service.validate(api_spec, DocumentType.oas)


def test_lint_service_with_ruleset_path():
    api_spec = read_yml("petstore_spec.yml")

    assert not lint_service.validate(api_spec, DocumentType.oas, {"ruleset_files": ["{}/resources/{}".format(dir_name, "ruleset.yml")], "ruleset_ttl": 5})


# def test_lint_service():
#     api_spec = read_yml("petstore_spec.yml")

#     assert not lint_service.validate(api_spec, DocumentType.oas, {"rulset_file": "https://raw.githubusercontent.com/GGui/graviteeio-lint-ruleset/main/ruleset.yml","rulset_ttl":5})
