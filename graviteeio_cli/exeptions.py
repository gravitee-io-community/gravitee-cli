import click
from click.exceptions import ClickException


class GraviteeioError(ClickException):
    def __init__(self, msg):
        self.message = click.style(msg, fg='red')

    def __str__(self):
        return repr('%s: %s' % (self.message))


class GraviteeioRequestError(GraviteeioError):
    def __init__(self, msg=None, error_code=None):

        self.message = click.style(msg, fg='red')
        self.error_code = error_code

        if self.error_code == 401:
            raise AuthenticationError(self.message)

    def __str__(self):
        return repr('%s: %s' % (self.error_code, self.message))


class AuthenticationError(GraviteeioRequestError):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return repr(self.message)
