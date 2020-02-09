
import logging
from datetime import datetime, timedelta

import requests
from requests import RequestException

from graviteeio_cli.exeptions import GraviteeioRequestError

APIS_CONTEXT = "/management/{}apis/"

logger = logging.getLogger("client.api_client")
class api_client:
    def __init__(self, config=None, debug=False):
        self.config = config
        self.timeout = 10

    def get(self, id):
        return self._request("GET", "{}".format(id))
    
    def create(self, api_data):
        return self._request("POST", "import", data = api_data)

    def update(self, id, api_data):
        return self._request("PUT", "{}".format(id), data = api_data)

    def start(self, id):
        return self._request("POST", "{}?action=START".format(id))

    def stop(self, id):
        return self._request("POST", "{}?action=STOP".format(id))

    def state(self, id):
        return self._request("GET", "{}/state".format(id))
    
    def deploy(self, id):
        return self._request("GET", "{}/deploy".format(id))
    
    def status(self, id, time_frame_seconds = 300):
        
        now = datetime.now()
        new_date = now - timedelta(seconds=time_frame_seconds)
    
        new_date_millisec = int(new_date.timestamp() * 1000)
        now_millisec = int(now.timestamp() * 1000)
        
        return self._request("GET", "{}/analytics?type=group_by&field=status&ranges=100:199%3B200:299%3B300:399%3B400:499%3B500:599&interval=600000&from={}&to={}&".format(id, new_date_millisec, now_millisec))

    def health(self, id):
        return self._request("GET", "{}/health?type=availability".format(id))

    def pages_fetch(self, id):
        return self._request("POST", "{}/pages/_fetch".format(id))
    
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
            logger.exception("api_client Request exception")
            raise GraviteeioRequestError(msg = "Error Connecting to server")

    def _check(self, response):
        
        if not response.status_code:
            raise GraviteeioRequestError(msg = "Request error")
        if response.status_code >= 400:
            try:
                logger.debug("response status %s %s", response.status_code, response.reason)

                error = response.json()
                raise GraviteeioRequestError(msg = error['message'], error_code = error['http_status'] )
            except ValueError:
                logger.exception("api_client Value error")
                raise GraviteeioRequestError(msg = response.reason, error_code = response.status_code )

# curl 'https://demo.gravitee.io/management/apis/import' -H 'sec-fetch-mode: cors' 
# -H 'origin: https://demo.gravitee.io' 
# -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7' -H 'x-requested-with: XMLHttpRequest' -H 'cookie: _ga=GA1.2.1715653817.1508833929; Auth-Graviteeio-APIM=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxODI2YTZjNS1iMmU2LTQ0NDEtYTZhNi1jNWIyZTY2NDQxMWEiLCJmaXJzdG5hbWUiOm51bGwsInBlcm1pc3Npb25zIjpbeyJhdXRob3JpdHkiOiJQT1JUQUw6QURNSU4ifSx7ImF1dGhvcml0eSI6Ik1BTkFHRU1FTlQ6QURNSU4ifV0sImlzcyI6ImdyYXZpdGVlLW1hbmFnZW1lbnQtYXV0aCIsImV4cCI6MTU3MjQyNTI3MCwiaWF0IjoxNTcxODIwNDcwLCJlbWFpbCI6bnVsbCwianRpIjoiYmEzNDhmYTItM2ZhNy00YTI5LWIzNjUtMzk0NWMwNDM4ODRkIiwibGFzdG5hbWUiOm51bGx9.KkHgjEe-2_or3MpzyiMOyHnXCaBzYbC0bU-v7P6wWgQ' -H 'pragma: no-cache' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36' -H 'content-type: application/json;charset=UTF-8' -H 'accept: application/json, text/plain, */*' -H 'cache-control: no-cache' -H 'authority: demo.gravitee.io' -H 'referer: https://demo.gravitee.io/' -H 'sec-fetch-site: same-origin' 
# --data-binary '{"proxy":{"endpoints":[{"name":"default","target":"http://test.com","inherit":true}],"context_path":"/testest"},"pages":[],"plans":[],"tags":[],"name":"test","description":"test","version":"1.0"}' --compressed

#curl 'http://localhost:3000/management/apis/import' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Accept: application/json, text/plain, */*' -H 'Origin: http://localhost:3000' -H 'X-Requested-With: XMLHttpRequest' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36' -H 'Content-Type: application/json;charset=UTF-8' -H 'Sec-Fetch-Site: same-origin' -H 'Sec-Fetch-Mode: cors' -H 'Referer: http://localhost:3000/' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7' -H 'Cookie: io=j4sz5EdX01KerkWHAAAD; Auth-Graviteeio-APIM=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZjg3YTkxZi1mNTQ1LTRkODctODdhOS0xZmY1NDU5ZDg3NDgiLCJmaXJzdG5hbWUiOm51bGwsInBlcm1pc3Npb25zIjpbeyJhdXRob3JpdHkiOiJQT1JUQUw6QURNSU4ifSx7ImF1dGhvcml0eSI6Ik1BTkFHRU1FTlQ6QURNSU4ifV0sImlzcyI6ImdyYXZpdGVlLW1hbmFnZW1lbnQtYXV0aCIsImV4cCI6MTU3MzQxMjIyNCwiaWF0IjoxNTcyODA3NDI0LCJlbWFpbCI6bnVsbCwianRpIjoiNWMzNDBkNzgtN2RmNC00MjQ4LTgyMjktMmFiZTViYTRjMTEyIiwibGFzdG5hbWUiOm51bGx9.xUj48FxN9uN0MYaC6kUEZGGNVBJsb1o6YyRJwg9HSlU' --data-binary '{"proxy":{"endpoints":[{"name":"default","target":"http://test.com","inherit":true}],"context_path":"/testest"},"pages":[],"plans":[],"tags":[],"name":"test","version":"1.0","description":"test"}' --compressed
