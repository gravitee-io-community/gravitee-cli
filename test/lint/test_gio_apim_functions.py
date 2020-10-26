import os
import json

from graviteeio_cli.lint.rulesets.gio_apim.functions.gioApimDocumentSchema import gio_apim_Document_Schema

dir_name = os.path.abspath(".") + "/test"
oas_file = "{}/resources/gio_oas/openapi.json".format(dir_name)


def read_api_def(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return json.loads(file.read())


def test_gio_apim_api_def():
    source = read_api_def("api_def.json")
    errors = gio_apim_Document_Schema(source, schema="gio_apim/schemas/schema_gio_apimv3.json")

    for error in errors:
        print('%s %s' % (error.path, error.message))

    assert len(errors) == 0
