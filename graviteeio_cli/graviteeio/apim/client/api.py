
import logging
import json
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
    
    def create_import(self, api_data):
        return self._request("POST", "import", data = json.dumps(api_data))
    
    def create_oas(self, oas):
        data = {
            "with_documentation": True,
            "with_path_mapping": True,
            "with_policy_paths": False,
            "with_policies":[],
            "type": "INLINE",
            "payload": oas
        }
        return self._request("POST", "import/swagger", data = json.dumps(data))
    
    def get_export(self, id):
        return self._request("GET", "{}/export?exclude=groups,members,pages&version=default".format(id))

    def update(self, id, api_data):
        return self._request("PUT", "{}".format(id), data = json.dumps(api_data))
    
    def update_import(self, id, api_data):
        return self._request("POST", "{}/import".format(id), data = json.dumps(api_data))

    def update_oas(self, id, oas):
        data = {
            "with_documentation": True,
            "with_path_mapping": True,
            "with_policy_paths": False,
            "with_policies":[],
            "type": "INLINE",
            "payload": oas
        }
        return self._request("POST", "{}/import/swagger".format(id), data = data)

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
                        proxies = self.config.proxies, \
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

        if response.status_code >= 400 and response.status_code < 500:
            try:
                logger.debug("response status %s reason: %s body:%s", response.status_code, response.reason, response.text)

                error = response.json()
                raise GraviteeioRequestError(msg = error['message'], error_code = error['http_status'] )
            except ValueError:
                logger.exception("api_client Value error")
                raise GraviteeioRequestError(msg = response.reason, error_code = response.status_code )
        elif response.status_code > 500:
            raise GraviteeioRequestError(msg = response.reason, error_code = response.status_code )

# curl 'https://demo.gravitee.io/management/apis/import' -H 'sec-fetch-mode: cors' 
# -H 'origin: https://demo.gravitee.io' 
# -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7' -H 'x-requested-with: XMLHttpRequest' -H 'cookie: _ga=GA1.2.1715653817.1508833929; Auth-Graviteeio-APIM=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxODI2YTZjNS1iMmU2LTQ0NDEtYTZhNi1jNWIyZTY2NDQxMWEiLCJmaXJzdG5hbWUiOm51bGwsInBlcm1pc3Npb25zIjpbeyJhdXRob3JpdHkiOiJQT1JUQUw6QURNSU4ifSx7ImF1dGhvcml0eSI6Ik1BTkFHRU1FTlQ6QURNSU4ifV0sImlzcyI6ImdyYXZpdGVlLW1hbmFnZW1lbnQtYXV0aCIsImV4cCI6MTU3MjQyNTI3MCwiaWF0IjoxNTcxODIwNDcwLCJlbWFpbCI6bnVsbCwianRpIjoiYmEzNDhmYTItM2ZhNy00YTI5LWIzNjUtMzk0NWMwNDM4ODRkIiwibGFzdG5hbWUiOm51bGx9.KkHgjEe-2_or3MpzyiMOyHnXCaBzYbC0bU-v7P6wWgQ' -H 'pragma: no-cache' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36' -H 'content-type: application/json;charset=UTF-8' -H 'accept: application/json, text/plain, */*' -H 'cache-control: no-cache' -H 'authority: demo.gravitee.io' -H 'referer: https://demo.gravitee.io/' -H 'sec-fetch-site: same-origin' 
# --data-binary '{"proxy":{"endpoints":[{"name":"default","target":"http://test.com","inherit":true}],"context_path":"/testest"},"pages":[],"plans":[],"tags":[],"name":"test","description":"test","version":"1.0"}' --compressed

#curl 'http://localhost:3000/management/apis/import' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Accept: application/json, text/plain, */*' -H 'Origin: http://localhost:3000' -H 'X-Requested-With: XMLHttpRequest' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36' -H 'Content-Type: application/json;charset=UTF-8' -H 'Sec-Fetch-Site: same-origin' -H 'Sec-Fetch-Mode: cors' -H 'Referer: http://localhost:3000/' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7' -H 'Cookie: io=j4sz5EdX01KerkWHAAAD; Auth-Graviteeio-APIM=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZjg3YTkxZi1mNTQ1LTRkODctODdhOS0xZmY1NDU5ZDg3NDgiLCJmaXJzdG5hbWUiOm51bGwsInBlcm1pc3Npb25zIjpbeyJhdXRob3JpdHkiOiJQT1JUQUw6QURNSU4ifSx7ImF1dGhvcml0eSI6Ik1BTkFHRU1FTlQ6QURNSU4ifV0sImlzcyI6ImdyYXZpdGVlLW1hbmFnZW1lbnQtYXV0aCIsImV4cCI6MTU3MzQxMjIyNCwiaWF0IjoxNTcyODA3NDI0LCJlbWFpbCI6bnVsbCwianRpIjoiNWMzNDBkNzgtN2RmNC00MjQ4LTgyMjktMmFiZTViYTRjMTEyIiwibGFzdG5hbWUiOm51bGx9.xUj48FxN9uN0MYaC6kUEZGGNVBJsb1o6YyRJwg9HSlU' --data-binary '{"proxy":{"endpoints":[{"name":"default","target":"http://test.com","inherit":true}],"context_path":"/testest"},"pages":[],"plans":[],"tags":[],"name":"test","version":"1.0","description":"test"}' --compressed


# curl 'https://demo.gravitee.io/management/apis/import/swagger' 
# -H 'authority: demo.gravitee.io' 
# -H 'pragma: no-cache' 
# -H 'cache-control: no-cache' 
# -H 'accept: application/json, text/plain, */*' 
# -H 'sec-fetch-dest: empty' 
# -H 'x-requested-with: XMLHttpRequest' 
# -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36' 
# -H 'content-type: application/json;charset=UTF-8' 
# -H 'origin: https://demo.gravitee.io' 
# -H 'sec-fetch-site: same-origin' 
# -H 'sec-fetch-mode: cors' 
# -H 'referer: https://demo.gravitee.io/' 
# -H 'accept-language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7' 
# -H 'cookie: _ga=GA1.2.1715653817.1508833929; Auth-Graviteeio-APIM=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzYzFiNDNiZC05Y2JlLTRjYzctOWI0My1iZDljYmUzY2M3YmQiLCJmaXJzdG5hbWUiOm51bGwsInBlcm1pc3Npb25zIjpbeyJhdXRob3JpdHkiOiJQT1JUQUw6QURNSU4ifSx7ImF1dGhvcml0eSI6Ik1BTkFHRU1FTlQ6QURNSU4ifV0sImlzcyI6ImdyYXZpdGVlLW1hbmFnZW1lbnQtYXV0aCIsImV4cCI6MTU4Njg1MDU0NywiaWF0IjoxNTg2MjQ1NzQ3LCJlbWFpbCI6bnVsbCwianRpIjoiYzNmMDY3NmYtZTFlMS00MDZiLWE5ZjktNWE1NTZhZDg2NGVmIiwibGFzdG5hbWUiOm51bGx9.TL51Ji_CBDljxnnTFJ0s-Cq9YWXtU_TMN3V_RUILOVs' 
# --data-binary $'
# {
# "with_documentation":true,
# "with_path_mapping":true,
# "with_policy_paths":false,
# "with_policies":[],
# "type":"INLINE",
# "payload":"openapi: \\"3.0.0\\"\\ninfo:\\n  version: 1.0.0\\n  title: Swagger Petstore\\n  description: A sample API that uses a petstore as an example to demonstrate features in the OpenAPI 3.0 specification\\n  termsOfService: http://swagger.io/terms/\\n  contact:\\n    name: Swagger API Team\\n    email: apiteam@swagger.io\\n    url: http://swagger.io\\n  license:\\n    name: Apache 2.0\\n    url: https://www.apache.org/licenses/LICENSE-2.0.html\\nservers:\\n  - url: http://petstore.swagger.io/api\\npaths:\\n  /pets:\\n    get:\\n      description: |\\n        Returns all pets from the system that the user has access to\\n        Nam sed condimentum est. Maecenas tempor sagittis sapien, nec rhoncus sem sagittis sit amet. Aenean at gravida augue, ac iaculis sem. Curabitur odio lorem, ornare eget elementum nec, cursus id lectus. Duis mi turpis, pulvinar ac eros ac, tincidunt varius justo. In hac habitasse platea dictumst. Integer at adipiscing ante, a sagittis ligula. Aenean pharetra tempor ante molestie imperdiet. Vivamus id aliquam diam. Cras quis velit non tortor eleifend sagittis. Praesent at enim pharetra urna volutpat venenatis eget eget mauris. In eleifend fermentum facilisis. Praesent enim enim, gravida ac sodales sed, placerat id erat. Suspendisse lacus dolor, consectetur non augue vel, vehicula interdum libero. Morbi euismod sagittis libero sed lacinia.\\n\\n        Sed tempus felis lobortis leo pulvinar rutrum. Nam mattis velit nisl, eu condimentum ligula luctus nec. Phasellus semper velit eget aliquet faucibus. In a mattis elit. Phasellus vel urna viverra, condimentum lorem id, rhoncus nibh. Ut pellentesque posuere elementum. Sed a varius odio. Morbi rhoncus ligula libero, vel eleifend nunc tristique vitae. Fusce et sem dui. Aenean nec scelerisque tortor. Fusce malesuada accumsan magna vel tempus. Quisque mollis felis eu dolor tristique, sit amet auctor felis gravida. Sed libero lorem, molestie sed nisl in, accumsan tempor nisi. Fusce sollicitudin massa ut lacinia mattis. Sed vel eleifend lorem. Pellentesque vitae felis pretium, pulvinar elit eu, euismod sapien.\\n      operationId: findPets\\n      parameters:\\n        - name: tags\\n          in: query\\n          description: tags to filter by\\n          required: false\\n          style: form\\n          schema:\\n            type: array\\n            items:\\n              type: string\\n        - name: limit\\n          in: query\\n          description: maximum number of results to return\\n          required: false\\n          schema:\\n            type: integer\\n            format: int32\\n      responses:\\n        \'200\':\\n          description: pet response\\n          content:\\n            application/json:\\n              schema:\\n                type: array\\n                items:\\n                  $ref: \'#/components/schemas/Pet\'\\n        default:\\n          description: unexpected error\\n          content:\\n            application/json:\\n              schema:\\n                $ref: \'#/components/schemas/Error\'\\n    post:\\n      description: Creates a new pet in the store.  Duplicates are allowed\\n      operationId: addPet\\n      requestBody:\\n        description: Pet to add to the store\\n        required: true\\n        content:\\n          application/json:\\n            schema:\\n              $ref: \'#/components/schemas/NewPet\'\\n      responses:\\n        \'200\':\\n          description: pet response\\n          content:\\n            application/json:\\n              schema:\\n                $ref: \'#/components/schemas/Pet\'\\n        default:\\n          description: unexpected error\\n          content:\\n            application/json:\\n              schema:\\n                $ref: \'#/components/schemas/Error\'\\n  /pets/{id}:\\n    get:\\n      description: Returns a user based on a single ID, if the user does not have access to the pet\\n      operationId: find pet by id\\n      parameters:\\n        - name: id\\n          in: path\\n          description: ID of pet to fetch\\n          required: true\\n          schema:\\n            type: integer\\n            format: int64\\n      responses:\\n        \'200\':\\n          description: pet response\\n          content:\\n            application/json:\\n              schema:\\n                $ref: \'#/components/schemas/Pet\'\\n        default:\\n          description: unexpected error\\n          content:\\n            application/json:\\n              schema:\\n                $ref: \'#/components/schemas/Error\'\\n    delete:\\n      description: deletes a single pet based on the ID supplied\\n      operationId: deletePet\\n      parameters:\\n        - name: id\\n          in: path\\n          description: ID of pet to delete\\n          required: true\\n          schema:\\n            type: integer\\n            format: int64\\n      responses:\\n        \'204\':\\n          description: pet deleted\\n        default:\\n          description: unexpected error\\n          content:\\n            application/json:\\n              schema:\\n                $ref: \'#/components/schemas/Error\'\\ncomponents:\\n  schemas:\\n    Pet:\\n      allOf:\\n        - $ref: \'#/components/schemas/NewPet\'\\n        - required:\\n          - id\\n          properties:\\n            id:\\n              type: integer\\n              format: int64\\n\\n    NewPet:\\n      required:\\n        - name  \\n      properties:\\n        name:\\n          type: string\\n        tag:\\n          type: string    \\n\\n    Error:\\n      required:\\n        - code\\n        - message\\n      properties:\\n        code:\\n          type: integer\\n          format: int32\\n        message:\\n          type: string\\n"}' --compressed