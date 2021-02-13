from graviteeio_cli.resolvers.conf_resolver import ConfigResolver, Config_Type
import os
import json

dir_name = os.path.abspath(".") + "/test"
resources_folder_yaml = "{}/resources/sk_default_yaml".format(dir_name)
resources_folder_json = "{}/resources/sk_default_json".format(dir_name)


def read_result(file_name):
    with open("{}/resources/assets/{}".format(dir_name, file_name)) as file:
        return file.read()


def return_json_data_and_expected(api_data, result_file):
    json_data = json.dumps(api_data)
    file_data_expected = read_result(result_file)
    data_expected = json.loads(file_data_expected)
    json_data_expected = json.dumps(data_expected)

    return (json_data, json_data_expected)


def test_generate_simple_api_yaml():
    api_sch = ConfigResolver(resources_folder_yaml)
    api_data = api_sch.get_data(Config_Type.API)

    json_data, json_data_expected = return_json_data_and_expected(api_data, "result_api.json")

    assert api_data['version'] == '1.0'
    assert json_data == json_data_expected


def test_generate_simple_api_json():
    api_sch = ConfigResolver(resources_folder_json)
    api_data = api_sch.get_data(Config_Type.API)

    json_data, json_data_expected = return_json_data_and_expected(api_data, "result_api.json")

    assert api_data['version'] == '1.0'
    assert json_data == json_data_expected


def test_generate_api_overide():
    api_sch = ConfigResolver(resources_folder_yaml)
    api_data = api_sch.get_data(Config_Type.API, set_values=["name=test", "endpoints[0]=https://api.gravitee.io/echo2"])

    json_data, json_data_expected = return_json_data_and_expected(api_data, "result_api_set.json")

    assert json_data == json_data_expected


def test_generate_api_overide_with_add_value():
    api_sch = ConfigResolver(resources_folder_yaml)
    api_data = api_sch.get_data(Config_Type.API, set_values=["name=test", "endpoints[1]=https://api.gravitee.io/echo2"])

    json_data, json_data_expected = return_json_data_and_expected(api_data, "result_api_set_add_value.json")

    assert json_data == json_data_expected
