
import requests
from graviteeio_cli.graviteeio.config import Graviteeio_configuration
from graviteeio_cli.exeptions import GraviteeioRequestError
from requests import RequestException

APIS_CONTEXT = "/management/apis/"

class apim_api:
    def __init__(self, conf=None, debug=False):
        self.config = Graviteeio_configuration()
        self.timeout = 1

    def get_apis(self):
        return self._request("GET")

    def get_api(self, id):
        return self._request("GET", "{}".format(id))
    
    def update_api(self, id, api_data):
        return self._request("PUT", "{}".format(id), data = api_data)

    def start_api(self, id):
        return self._request("POST", "{}?action=START".format(id))

    def stop_api(self, id):
        return self._request("POST", "{}?action=STOP".format(id))

    def state_api(self, id):
        return self._request("GET", "{}/state".format(id))
    
    def deploy_api(self, id):
        return self._request("GET", "{}/deploy".format(id))
    
    def _request(self, verbe, path = "", data = None):
        try:
            headers = {'Content-type': 'application/json'}
            response = requests.request(verbe, self.config.url(APIS_CONTEXT + path), \
                        auth = self.config.credential(), \
                        proxies = self.config.proxyDict, \
                        timeout=self.timeout,
                        data = data,
                        headers = headers)
            self._check(response)
            return response
        except RequestException:
            raise GraviteeioRequestError(msg = "Error Connecting to server")

    def _check(self, response):
        if not response.status_code:
            raise GraviteeioRequestError(msg = "Request error")
        if response.status_code == 400:
            try:
                error = response.json()
                raise GraviteeioRequestError(msg = error['message'], error_code = error['http_status'] )
            except ValueError:
                raise GraviteeioRequestError(msg = response.reason, error_code = response.status_code )
        if response.status_code > 400:
            raise GraviteeioRequestError(msg = response.reason, error_code = response.status_code )