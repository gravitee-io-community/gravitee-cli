import requests
import logging
from requests import RequestException

from graviteeio_cli.exeptions import GraviteeioRequestError, GraviteeioError, AuthenticationError

logger = logging.getLogger("client.HttpClient")


def decorator_json_function(fn):
    def new_json(**kwargs):
        try:
            return fn(**kwargs)
        except ValueError:
            raise GraviteeioError(msg="Response could not be decoded. (Check APIM url configuration)")

    return new_json


class HttpClient:
    def __init__(self, context, config=None):
        self.config = config
        self.timeout = 10
        self.context = context
        self.headers = {'Content-type': 'application/json'}

    def get(self, path, params=None, **kwargs):
        return self.request("GET", path=path, params=params, **kwargs)

    def post(self, path, data=None, **kwargs):
        return self.request("POST", path=path, data=data, **kwargs)

    def put(self, path, data=None, **kwargs):
        return self.request("PUT", path=path, data=data, **kwargs)

    def request(self, verbe, path="", **kwargs):

        params = kwargs

        params["proxies"] = self.config.proxies
        params["timeout"] = self.timeout

        if self.config.get_bearer():
            self.headers["Authorization"] = self.config.get_bearer_header()["Authorization"]
        else:
            logger.debug("No Bearer found")

        params["headers"] = self.headers
        try:
            response = requests.request(verbe, self.config.url(self.context + path), **params)
            self._check(response)

            response.json = decorator_json_function(response.json)
            return response
        except RequestException:
            logger.exception("api_client Request exception")
            raise GraviteeioRequestError(msg="Error Connecting to server")
        except AuthenticationError:
            msg = "Unauthorized access to the resource."
            auth = self.config.get_bearer_header()
            if not auth or "Authorization" not in auth:
                msg = msg + " No authentication found."
            raise AuthenticationError(msg)

    def _check(self, response):

        if not response.status_code:
            raise GraviteeioRequestError(msg="Request error")

        if response.status_code >= 400 and response.status_code < 500:
            try:
                logger.debug("response status %s reason: %s body:%s", response.status_code, response.reason, response.text)

                error = response.json()
                raise GraviteeioRequestError(msg=error['message'], error_code=error['http_status'])
            except ValueError:
                logger.exception("api_client Value error")
                raise GraviteeioRequestError(msg=response.reason, error_code=response.status_code)
        elif response.status_code >= 500:
            raise GraviteeioRequestError(msg=response.reason, error_code=response.status_code)
