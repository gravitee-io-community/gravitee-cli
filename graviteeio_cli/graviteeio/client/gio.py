import enum
import logging

import requests
from requests import RequestException

from graviteeio_cli.exeptions import GraviteeioRequestError

from .apim.api import api_client
from .apim.auth import auth_client

logger = logging.getLogger("client.gio")

APIM_APIS_CONTEXT = "/management/{}apis/"
APIM_USER_CONEXT = "/management/{}user/"

class APIM_client_type(enum.Enum):
    API = {
        'num': 1,
        'context': "/management/{}apis/"
        
    }

    AUTH = {
        'num': 2,
        'context': "/management/{}user/"
        
    }

    def __init__(self, values):
        self.num = values['num']
        self.context = values['context']

class AM_client_type(enum.IntEnum):
    AUTH = 1

class GioClient:
    
    @staticmethod
    def APIM(http_client_type: APIM_client_type, config, debug=False):
        if http_client_type is APIM_client_type.API:
            return  api_client(HttpClient(http_client_type.context, config))
        elif http_client_type is APIM_client_type.AUTH:
            return auth_client(HttpClient(http_client_type.context, config))
    
    @staticmethod
    def AM(http_client_type: AM_client_type, config, debug=False):
        pass

class HttpClient:
    def __init__(self, context, config = None):
        self.config = config
        self.timeout = 10
        self.context = context
        self.headers = {'Content-type': 'application/json'}

    def get(self, path, params = None, **kwargs):
        return self.request("GET", path = path, params= params, **kwargs)

    def post(self, path, data = None, **kwargs):
        return self.request("POST", path = path, data = data, **kwargs)

    def put(self, path, data = None, **kwargs):
        return self.request("PUT", path = path, data = data, **kwargs)

    def request(self, verbe, path = "", **kwargs):
        try:

            params = kwargs

            params["proxies"] = self.config.proxies
            params["timeout"] = self.timeout

            if self.config.get_bearer():
                self.headers["Authorization"] = self.config.get_bearer_header()["Authorization"]

            params["headers"] = self.headers
            response = requests.request(verbe, self.config.url(self.context + path), **params)
            self._check(response)
            return response
        except RequestException:
            logger.exception("api_client Request exception")
            raise GraviteeioRequestError(msg = "Error Connecting to server")

    def _check(self, response):
        
        if not response.status_code:
            raise GraviteeioRequestError(msg = "Request error")

        if response.status_code >= 400 and response.status_code < 500:
            try:
                logger.debug("response status %s reason: %s body:%s", response.status_code, response.reason, response.text)

                error = response.json()
                raise GraviteeioRequestError(msg = error['message'], error_code = error['http_status'] )
            except ValueError:
                logger.exception("api_client Value error")
                raise GraviteeioRequestError(msg = response.reason, error_code = response.status_code )
        elif response.status_code >= 500:
            raise GraviteeioRequestError(msg = response.reason, error_code = response.status_code )
