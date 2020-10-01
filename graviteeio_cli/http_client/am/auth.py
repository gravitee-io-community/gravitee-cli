from graviteeio_cli.http_client.auth.auth_client import AuthClient
from graviteeio_cli.core.config import GraviteeioConfig_am


class AuthAmClient(AuthClient):

    def __init__(self, config: GraviteeioConfig_am, debug=False):
        AuthClient.__init__(self, config, "/management/auth/", debug)

    def login(self, username, password):
        return AuthClient.login(self, "token", "access_token", (username, password))

    def logout(self):
        AuthClient.logout(self, "logout")
