from graviteeio_cli.http_client.auth.auth_client import AuthClient
from graviteeio_cli.core.config import GraviteeioConfig_apim


class AuthApimClient(AuthClient):

    def __init__(self, config: GraviteeioConfig_apim, debug=False):
        AuthClient.__init__(self, config, "/management/{}user/", debug)

    def login(self, username, password):
        return AuthClient.login(self, "login", "token", (username, password))

    def logout(self):
        AuthClient.logout(self, "logout")

    def tokens(self):
        return self.httpClient.get("tokens").json()
