from graviteeio_cli.graviteeio.client.http_client import HttpClient
from graviteeio_cli.graviteeio.config import GraviteeioConfig_apim

class AuthClient:

    def __init__(self,config: GraviteeioConfig_apim, debug=False):
        self.httpClient = HttpClient("/management/{}user/", config)

    def login(self, username, password):
        response = self.httpClient.post("login", auth = (username, password)).json()
        return response["token"]

    def logout(self):
        self.httpClient.post("logout")
