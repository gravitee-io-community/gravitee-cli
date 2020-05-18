import enum
import logging
from ..modules import GraviteeioModule
from .apim.api import api_client
from .apim.auth import auth_client
from graviteeio_cli.graviteeio.client.http_client import HttpClient
from graviteeio_cli.graviteeio.config import GraviteeioConfig_apim, GraviteeioConfig

logger = logging.getLogger("client.client_resources")

APIM_APIS_CONTEXT = "/management/{}apis/"
APIM_USER_CONEXT = "/management/{}user/"


class APIM_Client(enum.Enum):
    API = {
        'num': 1,
        'context': "/management/{}apis/",
        'client': api_client
    }

    AUTH = {
        'num': 2,
        'context': "/management/{}user/",
        'client': auth_client
    }

    def __init__(self, values):
        self.num = values['num']
        self.context = values['context']
        self.client = values['client']
    
    def get_http_client(self, config: GraviteeioConfig_apim):
        return HttpClient(self.context, config)
    
    def http(self, config: GraviteeioConfig):
        apim_config = config.getGraviteeioConfig(GraviteeioModule.APIM)
        httpClient = self.get_http_client(apim_config)

        # httpClient = type(self.client, self.get_http_client(config.getGraviteeioConfig(GraviteeioModule.APIM)))
        
        return self.client(httpClient)

class AM_Client(enum.IntEnum):
    AUTH = 1