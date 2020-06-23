import configparser
import enum
import json
import os

from .. import environments
from ..exeptions import GraviteeioError
from .modules import GraviteeioModule
from .output import OutputFormatType
from .utils import is_uri_valid


class Auth_Type(enum.IntEnum):
    CREDENTIAL = 0,
    PERSONAL_ACCESS_TOKEN = 1
    # OIDC = 1,
    # TOKEN_EXCHANGE = 2

    @staticmethod
    def list_name():
        return list(map(lambda c: c.name.lower(), Auth_Type))
    
    @staticmethod
    def value_of(value):
        for output in OutputFormatType:
            if output.name == value.upper():
                return output

class GraviteeioConfig:
    def __init__(self, config_file=environments.GRAVITEEIO_CONF_FILE):
        self.config_file = config_file
        self.config = configparser.ConfigParser()

        self.proxies = {
            "http": os.environ.get("http_proxy"),
            "https": os.environ.get("https_proxy")
        }

        self.config_module = {}
        self.config_module[GraviteeioModule.APIM] = GraviteeioConfig_apim(self.config, self.proxies, self)
        self.config_module[GraviteeioModule.AM] = GraviteeioConfig_am(self.config, self.proxies, self)

        if not os.path.isfile(config_file):

            self.profile = "demo"
            self.config['DEFAULT'] = {
                "current_profile": self.profile
            }

            for key in self.config_module:
                self.config_module[key].init_values(self.profile)

            with open(self.config_file, 'w') as fileObj:
                self.config.write(fileObj)
        else:
            self.config.read(config_file)
            self._load_config()

    def getGraviteeioConfigData(self, module: GraviteeioModule):
        return self.config_module[module].data
    
    def getGraviteeioConfig(self, module: GraviteeioModule):
        return self.config_module[module]
        
    def profiles(self):
        return self.config.sections()

    def load(self, profile, no_save = False):
        if profile is "DEFAULT":
            raise GraviteeioError('No profile [%s] accepted.' % profile)
        if not self.config.has_section(profile):
            raise GraviteeioError('No profile [%s] found.' % profile)
        
        self.config.set("DEFAULT", "current_profile", profile)
        if not no_save:
            with open(self.config_file, 'w') as fileObj:
                    self.config.write(fileObj)
        
        self._load_config()

    def _load_config(self):
        self.profile = self.config['DEFAULT']['current_profile']
        for key in self.config_module:
                self.config_module[key].load_config(self.profile)

    def save(self, profile, module, **kwargs):
        if not profile:
            profile = self.profile

        if (not self.config.has_section(profile)):
            
            self.config.add_section(profile)
            current_data = kwargs
        else:
            current_data = json.loads(self.config[profile][module])
            for key in kwargs:
                current_data[key] = kwargs[key]

        self.config.set(profile, module, json.dumps(current_data))

        with open(self.config_file, 'w') as fileObj:
            self.config.write(fileObj)
            
        if profile == self.profile:
            self._load_config()

    def remove(self, profile):
        if not self.config.has_section(profile):
            raise GraviteeioError('No profile [%s] found.' % profile)

        self.config.remove_section(profile)

        if profile == self.profile:
            self.profile = self.config.sections()[0]
            self.config.set("DEFAULT", "current_profile", self.profile)
            self._load_config()
        
        with open(self.config_file, 'w') as fileObj:
            self.config.write(fileObj)

    # def display_default(self, parameter_list):
    #     to_return = {}
    #     to_return["-- Default --"] = ""

    #     for key, value in self.proxies.items():
    #         to_return[key] = "{}".format(value)

    #     return to_return


    # def display_current_profile(self, profile = None):
    #     profile = self.config["DEFAULT"]["current_profile"]
        
    #     to_return = {
    #         "-- Default --": ""
    #     }

    #     to_return["Profile"] = "{}".format(profile)

    #     for key in self.config_module:
    #         to_return["## Module"] = "{}".format(self.config_module[key].module)
    #         to_return.update(self.config_module[key].display_current())

    #     return to_return
    
    def display_profile(self):

        to_return = {
            "profile": "{}".format(self.profile),
            "modules": []
        }

        for key in self.config_module:
            module_data = {
                "module": self.config_module[key].module 
            }

            if self.config_module[key].display_profile():
                module_data.update(self.config_module[key].display_profile())
            
            to_return["modules"].append(module_data)
        
        return to_return

class GraviteeioConfig_abstract:
    def __init__(self, module, config_parser: configparser.ConfigParser, proxies, graviteeioConfig: GraviteeioConfig):
        self.module = module.name
        self.config = config_parser
        self.proxies = proxies
        self.graviteeioConfig = graviteeioConfig
        self.data = {}
    
    def init_values(self, profile):
        self.data = self.getInitValues()
        self._apply_config(profile, self.data)

    def _apply_config(self, profile, data = None):
        if (not self.config.has_section(profile)) :
            self.config.add_section(profile)

        if data:
            self.config.set(profile, self.module, json.dumps(data))
    
    def getInitValues(self):
        pass

    def load_config(self, profile):
        if self.config.has_section(profile) :
            data_str = self.config.get(profile, self.module, fallback="{}")
            self.data = json.loads(data_str)
        else:
            raise GraviteeioError('No profile [%s] found.' % profile)
    
    # def display_current(self):
    #     to_return = {}
    #     if self.data:
    #         for key, value in self.data.items():
    #             to_return[key] = "{}".format(value)
    #     return to_return
    
    def display_profile(self):
        pass

    def save(self, **kwargs):
        self.graviteeioConfig.save(None, self.module, **kwargs)

    def url(self, path):
        pass

    def credential(self):
        pass

    def get_auth_list(self):
        return self.data["auth"] if "auth" in self.data else None
    
    def display_auth_list(self):
        to_return = []
        
        # if self.data and "auth" in self.data:
        #     for auth in self.data["auth"]:
        #         to_return.append({
        #             "username": auth["username"],
        #             "type": auth["type"],
        #             "is_active": "active" if auth["is_active"] else ""
        #         })
        # if self.is_logged_in():
        auth = self.get_active_auth()
        if auth:
            to_return.append({
                    "username": auth["username"],
                    "type": auth["type"],
                    "is_active": "active"
                })

        return to_return
    
    def is_logged_in(self):
        return "active_auth" in self.data and self.data["active_auth"] and "bearer" in self.data["active_auth"] and self.data["active_auth"]["bearer"] and self.data["active_auth"]["type"] == Auth_Type.CREDENTIAL.name.lower()

    def get_active_auth(self):
        return  self.data["active_auth"] if "active_auth" in self.data else None
    
    def set_active_auth(self, username, type: Auth_Type, bearer):
        self.save(active_auth = {"username": username, "bearer": bearer, "type": type.name.lower()})
    
    def remove_active_auth(self):
        self.save(active_auth = None)

    def get_bearer(self):
        return self.data["active_auth"]["bearer"] if "bearer" in self.data["active_auth"] else None

    def get_bearer_header(self):
        return {"Authorization": "Bearer {}".format(self.get_bearer())} if self.get_bearer() else None
    
    # def load_auth(self, username):
    #     bearer_old = self.get_bearer()
    #     beare_new = None

    #     active_auth = None
    #     auth_list = self.get_auth_list()
    #     for auth in auth_list:
    #         if auth["username"] == username:
    #             auth["is_active"] = True
    #             active_auth = auth
    #             if 'bearer' in auth:
    #                 beare_new = auth["bearer"]
    #         elif auth["is_active"]:
    #             auth["is_active"] = False
    #             auth["bearer"] = bearer_old

    #     if not active_auth:
    #         raise GraviteeioError("Username [{}] not exist.".format(username))

    #     self.save(auth = auth_list, bearer = beare_new, active_auth = active_auth)


class GraviteeioConfig_am(GraviteeioConfig_abstract):
    def __init__(self, config_parser, proxies, graviteeioConfig: GraviteeioConfig):
        GraviteeioConfig_abstract.__init__(self,GraviteeioModule.AM, config_parser, proxies, graviteeioConfig)

    def getInitValues(self):
        return {
            "address_url": environments.DEFAULT_AM_ADDRESS_URL
        }

    def url(self, path):
        org_and_env = "organizations/{}/environments/{}/".format(self.data["org"], self.data["env"]) if "env" in self.data and "org" in self.data else  ""
        return self.data["address_url"] + path.format(org_and_env)

 
class GraviteeioConfig_apim(GraviteeioConfig_abstract):
    def __init__(self, config_parser, proxies, graviteeioConfig: GraviteeioConfig):
        GraviteeioConfig_abstract.__init__(self,GraviteeioModule.APIM, config_parser, proxies, graviteeioConfig)

    def getInitValues(self):
        return {
            "address_url": environments.DEFAULT_APIM_ADDRESS_URL
        }

    def display_profile(self):
        to_return = {}

        if "address_url" in self.data:
            to_return = {
                "address_url": self.data["address_url"],
                "authentification": self.display_auth_list()
            }
        if "env" in self.data:
            to_return["environments"] = self.data["env"]
        
        if "org" in self.data:
            to_return["organisations"] = self.data["org"]

        return to_return
    
    # def display_profile(self, profile):
    #     other_data = []

    #     data_str = self.config.get(profile, self.module, fallback="{}")
    #     datas = json.loads(data_str)

    #     data = {
    #         "address_url": datas["address_url"]
    #     }
    #     if "env" in datas:
    #         data["env"] = datas["env"]

    #     other_data.append({
    #         "type": "Authentification",
    #         "to_display":self.display_auth_list()})

    #     return (data, other_data)
    
    def url(self, path):
        # https://nightly.gravitee.io/api/management/organizations/DEFAULT/environments/DEFAULT/apis/
        org_and_env = "organizations/{}/environments/{}/".format(self.data["org"], self.data["env"]) if "env" in self.data and "org" in self.data else  ""
        return self.data["address_url"] + path.format(org_and_env)