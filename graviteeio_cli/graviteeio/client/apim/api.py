
import logging
import json
import enum
from datetime import datetime, timedelta

import requests
from requests import RequestException

from graviteeio_cli.exeptions import GraviteeioRequestError

APIS_CONTEXT = "/management/{}apis/"

logger = logging.getLogger("client.api_client")

class Api_Action(enum.IntEnum):
    START = 0
    STOP = 1

class api_client:
    def __init__(self, httpClient, debug=False):
        self.httpClient = httpClient

    def get(self, id):
        return self.httpClient.get("{}".format(id))
    
    def create_import(self, api_data):
        return self.httpClient.post("import", data = json.dumps(api_data))
    
    def create_oas(self, oas):
        data = {
            "with_documentation": True,
            "with_path_mapping": True,
            "with_policy_paths": False,
            "with_policies":[],
            "type": "INLINE",
            "payload": oas
        }
        return self.httpClient.post("import/swagger", data = json.dumps(data))
    
    def get_export(self, id):
        params = {
            "exclude": "groups,members,pages",
            "version": "default"
        }
        return self.httpClient.get("{}/export".format(id), params = params)

    def update(self, id, api_data):
        return self.httpClient.put("{}".format(id), data = json.dumps(api_data))
        
    def update_import(self, id, api_data):
        return self.httpClient.post("{}/import".format(id), data = json.dumps(api_data))

    def update_oas(self, id, oas):
        data = {
            "with_documentation": True,
            "with_path_mapping": True,
            "with_policy_paths": False,
            "with_policies":[],
            "type": "INLINE",
            "payload": oas
        }
        return self.httpClient.post("{}/import/swagger".format(id), data = data)

    def action(self, id, action_type: Api_Action):
        params = {
            "action": action_type.name
        }
        return self.httpClient.post("{}".format(id, action_type))

    def start(self, id):
        return self.action(id, Api_Action.START)

    def stop(self, id):
        return self.action(id, Api_Action.STOP)

    def state(self, id):
        return self.httpClient.get("{}/state".format(id))
    
    def deploy(self, id):
        return self.httpClient.post("{}/deploy".format(id))
    
    def status(self, id, time_frame_seconds = 300):
        
        now = datetime.now()
        new_date = now - timedelta(seconds=time_frame_seconds)
    
        new_date_millisec = int(new_date.timestamp() * 1000)
        now_millisec = int(now.timestamp() * 1000)
        
        return self.httpClient.get("{}/analytics?type=group_by&field=status&ranges=100:199%3B200:299%3B300:399%3B400:499%3B500:599&interval=600000&from={}&to={}&".format(id, new_date_millisec, now_millisec))

    def health(self, id):
        params =  {
            "type": "availability"
        }
        return self.httpClient.get("{}/health".format(id), params)

    def pages_fetch(self, id):
        return self.httpClient.post("{}/pages/_fetch".format(id))