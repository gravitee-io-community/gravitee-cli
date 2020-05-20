import enum
import logging
from ..modules import GraviteeioModule
from .apim.api import ApiClient
from .apim.auth import AuthClient
from graviteeio_cli.graviteeio.client.http_client import HttpClient
from graviteeio_cli.graviteeio.config import GraviteeioConfig_apim, GraviteeioConfig

logger = logging.getLogger("client.client_resources")

APIM_APIS_CONTEXT = "/management/{}apis/"
APIM_USER_CONEXT = "/management/{}user/"


class APIM_Client(enum.Enum):
    API = {
        'num': 1,
        'client': ApiClient
    }

    AUTH = {
        'num': 2,
        'client': AuthClient
    }

    def __init__(self, values):
        self.num = values['num']
        self.client = values['client']
    
    def http(self, config: GraviteeioConfig):
        apim_config = config.getGraviteeioConfig(GraviteeioModule.APIM)
        
        return self.client(apim_config)

class AM_Client(enum.IntEnum):
    AUTH = 1