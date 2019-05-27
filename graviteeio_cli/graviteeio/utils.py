from .config import Graviteeio_configuration

def update_dic_with_set(set_value, dic):
    (key, value) = set_value.split('=')

    __update_dict(key, value, dic)

    return dic

def __update_dict(key, value, dic):
    
    keys = key.split('.', 1)
    new_key = keys[0]
    index_list = None

    if new_key.find('[') > 0 and new_key.find(']') > 0:
        index_list = int(new_key[new_key.find('[')+1: new_key.find(']')])
        new_key = new_key[0:new_key.find('[')]
        

    if len(keys) == 1:
        if index_list == None:
            dic[new_key] = value
        else:
            dic[new_key][index_list] = value
    else:
        if index_list == None:
            __update_dict(keys[1], value, dic[new_key])
        else:
            __update_dict(keys[1], value, dic[new_key][index_list])

def convert_proxy_config(yaml_dictionary):
    #strip_context_path
    if 'strip_context_path' not in yaml_dictionary['proxy']:
     yaml_dictionary['proxy']['strip_context_path'] = False
    
    for group in yaml_dictionary['proxy']['groups']:
        if 'endpoints' in group:
            for endpoint in group['endpoints']:
                if 'backup' not in endpoint:
                    endpoint['backup'] = False
                if 'http' not in endpoint and 'inherit' not in endpoint:
                    endpoint['inherit'] = True

        if 'services' not in group or group['services'] is None:
            group['services'] = {}

        if 'discovery' not in group['services'] or group['services']['discovery'] is None:
            group['services']['discovery'] = {}
            group['services']['discovery']['enabled'] = False

        if 'proxy' not in group:
            group['proxy'] = {}
            group['proxy']['enabled'] = False
            group['proxy']['host'] = "null"
            group['proxy']['port'] = 0
            group['proxy']['type'] = "HTTP"
        elif 'enabled' not in group['proxy']:
            group['proxy']['enabled'] = False

        #HTTP
        if 'http' not in group:
            group['http'] = {}
        
        config = Gravitee_configuration()
        config.load_http(group['http'])

        if 'load_balancing' not in group:
            group['load_balancing'] = {}
        if 'type' not in group['load_balancing']:
            group['load_balancing']['type'] = "ROUND_ROBIN"

        #SSL
        if 'ssl' not in group:
            group['ssl'] = {}
        if 'trustAll' not in group['ssl']:
            group['ssl']['trustAll'] = False
        if 'hostnameVerifier' not in group['ssl']:
            group['ssl']['hostnameVerifier'] = False
    
def clean_api(api):
    del api["deployed_at"]
    del api["created_at"]
    del api["updated_at"]
#    del api["visibility"]
    del api["state"]
#    del api["permission"]
    del api["owner"]
    del api["picture_url"]
#    del api["views"]
#    del api["groups"]
#    del api["etag"]
    del api["context_path"]
    del api["id"]

