
import enum
import json
import logging
from datetime import datetime, timedelta

import requests
from requests import RequestException

from graviteeio_cli.exeptions import GraviteeioRequestError
from graviteeio_cli.graviteeio.client.http_client import HttpClient
from graviteeio_cli.graviteeio.config import GraviteeioConfig_apim

logger = logging.getLogger("client.api_client")

class Api_Action(enum.IntEnum):
    START = 0
    STOP = 1

class ApiClient:

    def __init__(self, config: GraviteeioConfig_apim, debug=False):
        self.httpClient = HttpClient("/management/{}apis/", config)

    def get(self, id = None, response_filter = None):
        response =self.httpClient.get("{}".format(id) if id else "")
        json_body = response.json()
        if response_filter:
            response_filter(json_body)
        return json_body
    
    def create_import(self, api_data):
        return self.httpClient.post("import", data = json.dumps(api_data)).json()
    
    def create_oas(self, oas):
        data = {
            "with_documentation": True,
            "with_path_mapping": True,
            "with_policy_paths": False,
            "with_policies":[],
            "type": "INLINE",
            "payload": oas
        }
        return self.httpClient.post("import/swagger", data = json.dumps(data)).json()
    
    def get_export(self, id, response_filter = None):
        params = {
            "exclude": "groups,members,pages",
            "version": "default"
        }

        response = self.httpClient.get("{}/export".format(id), params = params).json()
        if response_filter:
            response_filter(response)

        return response

    def update(self, id, api_data):
        return self.httpClient.put("{}".format(id), data = json.dumps(api_data)).json()
        
    def update_import(self, id, api_data):
        return self.httpClient.post("{}/import".format(id), data = json.dumps(api_data)).json()

    def update_oas(self, id, oas):
        data = {
            "with_documentation": True,
            "with_path_mapping": True,
            "with_policy_paths": False,
            "with_policies":[],
            "type": "INLINE",
            "payload": oas
        }
        return self.httpClient.post("{}/import/swagger".format(id), data = data).json()

    def action(self, id, action_type: Api_Action):
        # params = {
        #     "action": action_type.name
        # }
        # return self.httpClient.post("{}".format(id), params)
        return self.httpClient.post("{}?action={}".format(id, action_type.name))

    def start(self, id):
        return self.action(id, Api_Action.START)

    def stop(self, id):
        return self.action(id, Api_Action.STOP)

    def state(self, id):
        return self.httpClient.get("{}/state".format(id)).json()
    
    def deploy(self, id):
        return self.httpClient.post("{}/deploy".format(id))
    
    def status(self, id, time_frame_seconds = 300):
        
        now = datetime.now()
        new_date = now - timedelta(seconds=time_frame_seconds)
    
        new_date_millisec = int(new_date.timestamp() * 1000)
        now_millisec = int(now.timestamp() * 1000)
        
        return self.httpClient.get("{}/analytics?type=group_by&field=status&ranges=100:199%3B200:299%3B300:399%3B400:499%3B500:599&interval=600000&from={}&to={}&" \
            .format(id, new_date_millisec, now_millisec)).json()

    def health(self, id):
        params =  {
            "type": "availability"
        }
        return self.httpClient.get("{}/health".format(id), params).json()

    def pages_fetch(self, id):
        return self.httpClient.post("{}/pages/_fetch".format(id))
