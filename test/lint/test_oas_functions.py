
import os
import json
import yaml
import jmespath

from graviteeio_cli.lint.rulesets.oas.functions.oasDocumentSchema import oasDocumentSchema
from graviteeio_cli.lint.rulesets.oas.functions.oasExtGravitee import oasExtGravitee

dir_name = os.path.abspath(".") + "/test"
petstore_v2_file = "{}/resources/gio_oas/petstore_spec_v2.json".format(dir_name)


def read_oas_json(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return json.loads(file.read())


def read_oas_yml(file_name):
    with open("{}/lint/gio_oas/{}".format(dir_name, file_name)) as file:
        return yaml.load(file.read(), Loader=yaml.SafeLoader)


def test_petstore_spec_v2():
    source = read_oas_json("petstore_spec_v2.json")
    errors = oasDocumentSchema(source, schema="oas/schemas/schema_oas2.json")

    for error in errors:
        print('%s %s' % (error.path, error.message))

    assert len(errors) == 0


def test_petstore_spec_v3():
    source = read_oas_json("petstore_spec_v3_0.json")
    errors = oasDocumentSchema(source, schema="oas/schemas/schema_oas3.json")

    for error in errors:
        print('%s %s' % (error.path, error.message))

    assert len(errors) == 0


def test_petstore_spec_x_gravitee():
    # query = '"x-graviteeio-definition"'
    source = read_oas_yml("petstore_spec_gravitee.yml")

    # result = jmespath.search(query, source)

    errors = oasExtGravitee(source, schema="oas/schemas/ext_gravitee/xGraviteeIODefinition.json")

    for error in errors:
        print('path: %s message: %s' % (error.path, error.message))

    assert len(errors) == 0


def test_petstore_spec_with_none_x_gravitee():
    # query = '"x-graviteeio-definition"'
    source = read_oas_json("petstore_spec_v3_0.json")

    # result = jmespath.search(query, source)

    errors = oasExtGravitee(source, schema="oas/schemas/ext_gravitee/xGraviteeIODefinition.json")

    for error in errors:
        print('%s %s' % (error.path, error.message))

    assert len(errors) == 0


def test_petstore_spec_oasOpIdUnique():
    query = "paths.*.*.operationId[]"
    source = read_oas_json("petstore_spec_v3_0.json")

    result = jmespath.search(query, source)

    print("test")
