import logging
import os
from urllib.parse import urlparse

from ..exeptions import GraviteeioError

logger = logging.getLogger("utils")


def is_uri_valid(url, qualifying=('scheme', 'netloc')):
    tokens = urlparse(url)
    return all([getattr(tokens, qualifying_attr)
                for qualifying_attr in qualifying])


def is_env_value(value):
    return value.startswith("env:")


def get_env_value(value):
    to_return = None
    if is_env_value(value):
        to_return = os.environ.get(value[4:])
        if not to_return:
            raise GraviteeioError('No environement value found for [{}].'.format(value[4:]))
            logger.error("No environement value found for [{}].".format(to_return))

    return to_return
