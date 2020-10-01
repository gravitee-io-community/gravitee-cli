from graviteeio_cli.http_client.http_client import HttpClient
from graviteeio_cli.core.config import GraviteeioConfig_abstract


class AuthClient:

    def __init__(self, config: GraviteeioConfig_abstract, path: str, debug=False):
        self.httpClient = HttpClient(path, config)

    def login(self, path, token_name, credential: tuple):
        response = self.httpClient.post(path, auth=credential).json()
        return response[token_name]

    def logout(self, path):
        self.httpClient.post(path, allow_redirects=False)
