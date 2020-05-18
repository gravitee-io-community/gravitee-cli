import requests
import logging
from requests import RequestException

from graviteeio_cli.exeptions import GraviteeioRequestError

logger = logging.getLogger("client.HttpClient")

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
