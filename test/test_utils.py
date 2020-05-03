# import yaml
# import json
# from jinja2 import Template
# from graviteeio_cli.gravitee.utils import convert_proxy_config
from graviteeio_cli.graviteeio.utils import is_uri_valid

def test_url_valid():
    url_1='https://gravitee.io/'
    url_2='http://gravitee.io/'
    url_3='http://gravitee.io'
    url_4='http://gravitee.io:80'

    assert is_uri_valid(url_1)
    assert is_uri_valid(url_2)
    assert is_uri_valid(url_3)
    assert is_uri_valid(url_4)

def test_url_not_valid():
    url_1='gravitee.io'
    url_2='http:/gravitee.io/'
    url_3='http://gravitee'
    url_4='gravitee.io:80'

    assert not is_uri_valid(url_1)
    assert not is_uri_valid(url_2)
    assert not is_uri_valid(url_3)
    assert not is_uri_valid(url_4)


# def test_convert_proxy_config():
#     with open("test/proxy.json",'r') as f:
#         json_string = f.read()
#     with open("test/proxy.yml",'r') as f:
#         yaml_string = f.read()

#     proxy_data = yaml.load(yaml_string, Loader=yaml.SafeLoader)
#     convert_proxy_config(proxy_data)
#     proxy_json = json.dumps(proxy_data, sort_keys=True)

#     proxy_data2 = json.loads(json_string)
#     proxy_json2 = json.dumps(proxy_data2, sort_keys=True)

#     assert proxy_json == proxy_json2

# def test_convert_api_config():
#     with open("test/api_result.json",'r') as f:
#         json_result_string = f.read()
#     with open("test/api_tempate.yml.j2",'r') as f:
#         yaml_template_string = f.read()
#     with open("test/api_value.yml",'r') as f:
#         yaml_value_string = f.read()

#     template = Template(yaml_template_string)
#     api_value = yaml.load(yaml_value_string, Loader=yaml.SafeLoader)
    

#     request_yaml = template.render(api= api_value, config={})
#     print("yaml: ")
#     print(request_yaml)
#     request_data = yaml.load(request_yaml, Loader=yaml.SafeLoader)
#     if 'version' in request_data:
#         request_data['version'] =  str(request_data['version'])
#     #verifier les règles SSL
    
#     request_json = json.dumps(request_data)

#     print("-----")
#     print(request_json.replace(' ', ''))
    
#     result_data = json.loads(json_result_string)
#     new_json_result = json.dumps(result_data, separators=(',', ":"))
#     print("New JSON")
#     print(new_json_result)

#     print(json_result_string.replace('\n', '').replace('\r', '').replace('    ', '').replace(' ', ''))
    
#     assert request_json.replace(' ', '') == json_result_string.replace('\n', '').replace('\r', '').replace('    ', '').replace(' ', '')
#     #proxy_data = yaml.load(yaml_string, Loader=yaml.SafeLoader)
#     #convert_proxy_config(proxy_data)
#     #proxy_json = json.dumps(proxy_data, sort_keys=True)
#     #print(proxy_json)

#     #proxy_data2 = json.loads(json_string)
#     #proxy_json2 = json.dumps(proxy_data2, sort_keys=True)

#     #assert proxy_json == proxy_json2
#     #{% set connectTimeout = config.stackowerflow.connect.timeout | default(config.stackowerflow.timeout) | default(config.timeout) | default(42) -%}