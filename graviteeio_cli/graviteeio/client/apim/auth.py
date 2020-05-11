class auth_client:
    def __init__(self, httpClient, debug=False):
        self.httpClient = httpClient

    def login(self, username, password):
        response = self.httpClient.post("login", auth = (username, password)).json()
        return response["token"]

    def logout(self):
        self.httpClient.post("logout")
