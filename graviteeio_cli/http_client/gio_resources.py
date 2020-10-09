import enum
import logging
from graviteeio_cli.modules.gio_module import GioModule
from .apim.api import ApiClient
from .apim.auth import AuthApimClient
from .apim.page import PageClient
from .am.auth import AuthAmClient

from graviteeio_cli.core.config import GraviteeioConfig

logger = logging.getLogger("client.client_resources")


class APIM_Client(enum.Enum):
    API = {
        'num': 1,
        'client': ApiClient
    }

    AUTH = {
        'num': 2,
        'client': AuthApimClient
    }

    PAGE = {
        'num': 3,
        'client': PageClient
    }

    def __init__(self, values):
        self.num = values['num']
        self.client = values['client']

    def http(self, config: GraviteeioConfig):
        apim_config = config.getGraviteeioConfig(GioModule.APIM)

        return self.client(apim_config)


class AM_Client(enum.Enum):
    AUTH = {
        'num': 2,
        'client': AuthAmClient
    }

    def __init__(self, values):
        self.num = values['num']
        self.client = values['client']

    def http(self, config: GraviteeioConfig):
        apim_config = config.getGraviteeioConfig(GioModule.AM)

        return self.client(apim_config)
