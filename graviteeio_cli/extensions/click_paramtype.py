from urllib.parse import urlparse

from click import ParamType


class URLParamType(ParamType):
    name = 'URL'

    def convert(self, value, param, ctx):

        if is_uri_valid(value):
            return value
        else:
            self.fail('%s is not a valid url' % value, param, ctx)

        if isinstance(value, bool):
            return bool(value)

    def __repr__(self):
        return 'URL'


def is_uri_valid(url, qualifying=('scheme', 'netloc')):
    tokens = urlparse(url)
    return all([getattr(tokens, qualifying_attr) for qualifying_attr in qualifying])


URL = URLParamType()
