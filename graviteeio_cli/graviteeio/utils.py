from urllib.parse import urlparse


def is_uri_valid(url, qualifying=('scheme', 'netloc')):
    tokens = urlparse(url)
    return all([getattr(tokens, qualifying_attr)
                for qualifying_attr in qualifying])

