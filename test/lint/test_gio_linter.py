import os
import json
import yaml
from graviteeio_cli.lint.gio_linter import Gio_linter
from graviteeio_cli.lint.types.document import DocumentType, Document

dir_name = os.path.abspath(".") + "/test"
oas_file = "{}/resources/gio_oas/openapi.json".format(dir_name)


def read_api_def(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return json.loads(file.read())


def read_oas_yml(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return yaml.load(file.read(), Loader=yaml.SafeLoader)


def test_gio_apim_api_def():
    linter = Gio_linter()

    source = read_api_def("api_def.json")
    document = Document(source, DocumentType.gio_apim)
    diagResult = linter.run(document)

    for error in diagResult:
        print('%s %s %s' % (error.severity, error.path, error.message))

    # error with lower case of visibility
    assert len(diagResult) == 1


def test_oas_v2():
    linter = Gio_linter()

    source = read_oas_yml("petstore_spec_V2.yml")
    document = Document(source, DocumentType.oas)
    diagResult = linter.run(document)

    assert len(diagResult) == 0


def test_oas_v3_0():
    linter = Gio_linter()

    source = read_oas_yml("petstore_spec_V3_0.yml")
    document = Document(source, DocumentType.oas)
    diagResult = linter.run(document)

    assert len(diagResult) == 0


# def test_oas_v3_1():
#     linter = Gio_linter()

#     source = read_oas_yml("petstore_spec_V3_1.yml")
#     document = Document(source, DocumentType.oas)
#     diagResult = linter.run(document)

#     for error in diagResult:
#         print('%s %s %s' % (error.severity, error.path, error.message))

#     assert len(diagResult) == 0

# def test_validation_api_def():
#     oas = None

#     with open(oas_file) as file:
#         oas_json = file.read()

#     oas = json.loads(oas_json)
#     api_entity_schema = oas['components']['schemas']['UpdateApiEntity']
# # ApiEntity
# # UpdateApiEntity
#     instance = read_api_def("api_def.json")

#     resolver = RefResolver.from_schema(oas)

#     # validator = Draft6Validator.check_schema(api_entity_schema)
#     validator = Draft6Validator(api_entity_schema, resolver=resolver)

#     # for error in sorted(validator.iter_errors(instance), key=str):
#     #     path_join
#     #     print(f"---- {error.path} {error.message}")
#     errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)

#     if errors:
#         for error in errors:
#             print('%s %s' % ('-'.join(error.path), error.message))
#         # print(', '.join(
#         #     '%s %s %s' % (error.path.popleft(), error.path.pop(), error.message) for error in errors
#         # ))


#     # validate(instance=instance, schema=api_entity_schema)
