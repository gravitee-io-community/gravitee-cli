import os
import json
import yaml
import jmespath

from graviteeio_cli.lint.functions.length import lenght

dir_name = os.path.abspath(".") + "/test"


def read_oas_json(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return json.loads(file.read())


def read_oas_yml(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return yaml.load(file.read(), Loader=yaml.SafeLoader)


def test_length_function():
    query = "paths.*.*.tags[]"
    source = read_oas_yml("petstore_spec_V3_0.yml")

    expression = jmespath.compile(query)
    result = expression.search(source)

    functionResult = lenght(result, min=1)

    print(result)