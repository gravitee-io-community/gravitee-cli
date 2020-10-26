
import os
import json

from graviteeio_cli.lint.rulesets.oas.functions.oasDocumentSchema import oasDocumentSchema

dir_name = os.path.abspath(".") + "/test"
petstore_v2_file = "{}/resources/gio_oas/petstore_spec_v2.json".format(dir_name)


def read_api_def(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return json.loads(file.read())


def test_petstore_spec_v2():
    source = read_api_def("petstore_spec_v2.json")
    errors = oasDocumentSchema(source, schema="oas/schemas/schema_oas2.json")

    for error in errors:
        print('%s %s' % (error.path_join(), error.message))

    assert len(errors) == 0


def test_petstore_spec_v3():
    source = read_api_def("petstore_spec_v3_0.json")
    errors = oasDocumentSchema(source, schema="oas/schemas/schema_oas3.json")

    for error in errors:
        print('%s %s' % (error["path"], error["message"]))

    assert len(errors) == 0
