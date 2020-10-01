import configparser
import enum
import json
import os

from .. import environments
from ..exeptions import GraviteeioError
from graviteeio_cli.modules.gio_module import GioModule
from .output import OutputFormatType
from graviteeio_cli.extensions.configparser_interpolation import GioInterpolation

DEFAULT_ENV_PROFILE = 'env_sys'


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
        self.config = configparser.ConfigParser(
                        interpolation=GioInterpolation()
                    )

        self.proxies = {
            "http": os.environ.get("http_proxy"),
            "https": os.environ.get("https_proxy")
        }

        self.config_module = {}
        self.config_module[GioModule.APIM] = GraviteeioConfig_apim(self.config, self.proxies, self)
        self.config_module[GioModule.AM] = GraviteeioConfig_am(self.config, self.proxies, self)

        if not os.path.isfile(config_file):

            self.profile = DEFAULT_ENV_PROFILE
            self.config['DEFAULT'] = {
                "current_profile": self.profile
            }

            for key in self.config_module:
                # self.config_module[key].init_values(self.profile)
                self.config_module[key].load_env_values()

            # with open(self.config_file, 'w') as fileObj:
            #     self.config.write(fileObj)
        else:
            self.config.read(config_file)
            self._load_config()

    def getGraviteeioConfigData(self, module: GioModule):
        return self.config_module[module].data

    def getGraviteeioConfig(self, module: GioModule):
        return self.config_module[module]

    def profiles(self):
        profiles = [DEFAULT_ENV_PROFILE]
        profiles.extend(self.config.sections())
        return profiles

    def load(self, profile, no_save=False):
        if profile == "DEFAULT":
            raise GraviteeioError('No profile [%s] accepted.' % profile)
        if not self.config.has_section(profile) and profile != DEFAULT_ENV_PROFILE:
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

        if profile == DEFAULT_ENV_PROFILE:
            raise GraviteeioError('Profile [%s] can\'t be modified.' % DEFAULT_ENV_PROFILE)

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
        if profile == DEFAULT_ENV_PROFILE:
            raise GraviteeioError('Profile [%s] can\'t be removed.' % DEFAULT_ENV_PROFILE)

        if not self.config.has_section(profile):
            raise GraviteeioError('No profile [%s] found.' % profile)

        self.config.remove_section(profile)

        if profile == self.profile:
            self.profile = self.config.sections()[0]
            self.config.set("DEFAULT", "current_profile", self.profile)
            self._load_config()

        with open(self.config_file, 'w') as fileObj:
            self.config.write(fileObj)

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

    # def init_values(self, profile):
    #     self.data = self.get_init_values()
    #     self._apply_config(profile, self.data)

    def load_env_values(self):
        self.data = self.get_env_values()

    def _apply_config(self, profile, data=None):
        if (not self.config.has_section(profile)):
            self.config.add_section(profile)

        if data:
            self.config.set(profile, self.module, json.dumps(data))

    # def get_init_values(self):
    #     pass

    def get_env_values(self):
        pass

    def load_config(self, profile):
        if profile != DEFAULT_ENV_PROFILE and self.config.has_section(profile):
            data_str = self.config.get(profile, self.module, fallback="{}")
            self.data = json.loads(data_str)
        elif profile == DEFAULT_ENV_PROFILE:
            self.load_env_values()
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
        auth = {}

        if "authn_name" in self.data and self.data["authn_name"]:
            auth["name"] = self.data["authn_name"]

        if "authn_type" in self.data and self.data["authn_type"]:
            auth["type"] = self.data["authn_type"]

        if self.is_active_bearer():
            auth["is_active"] = "active"
            auth["Token"] = "***"

        if auth:
            to_return.append(auth)

        return to_return

    def is_logged_in(self):
        return self.is_active_bearer() and self.data["authn_type"] == Auth_Type.CREDENTIAL.name.lower()

    def is_active_bearer(self):
        return "bearer" in self.data and self.data["bearer"]

    def get_authn_name(self):
        return self.data["authn_name"] if "authn_name" in self.data else None

    def save_active_auth(self, authn_name, type: Auth_Type, bearer):
        self.save(authn_name=authn_name, bearer=bearer, authn_type=type.name.lower())

    def remove_active_auth(self):
        self.save(authn_name=None, bearer=None, authn_type=None)

    def get_bearer(self):
        bearer = None
        if self.is_active_bearer():
            bearer = self.data["bearer"]
        return bearer

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
        GraviteeioConfig_abstract.__init__(self, GioModule.AM, config_parser, proxies, graviteeioConfig)

    # def get_init_values(self):
    #     if environments.DEFAULT_AM_TOKEN:
    #         default_value = {
    #             "address_url": environments.DEFAULT_AM_ADDRESS_URL,
    #             "bearer": environments.DEFAULT_AM_TOKEN,
    #             "authn_type": Auth_Type.PERSONAL_ACCESS_TOKEN.name.lower(),
    #             "authn_name": "Environment Token"
    #         }
    #     else:
    #         default_value = {
    #             "address_url": environments.DEFAULT_AM_ADDRESS_URL
    #         }

    #     return default_value

    def get_env_values(self):
        if environments.DEFAULT_AM_TOKEN:
            default_value = {
                "address_url": environments.DEFAULT_AM_ADDRESS_URL,
                "bearer": environments.DEFAULT_AM_TOKEN,
                "authn_type": Auth_Type.PERSONAL_ACCESS_TOKEN.name.lower(),
                "authn_name": "Environment Token"
            }
        else:
            default_value = {
                "address_url": environments.DEFAULT_AM_ADDRESS_URL
            }

        return default_value

    def url(self, path):
        org_and_env = "organizations/{}/environments/{}/".format(self.data["org"], self.data["env"]) if "env" in self.data and "org" in self.data else ""
        return self.data["address_url"] + path.format(org_and_env)


class GraviteeioConfig_apim(GraviteeioConfig_abstract):

    def __init__(self, config_parser, proxies, graviteeioConfig: GraviteeioConfig):
        GraviteeioConfig_abstract.__init__(self, GioModule.APIM, config_parser, proxies, graviteeioConfig)

    # def get_init_values(self):
    #     if environments.DEFAULT_APIM_TOKEN:
    #         default_value = {
    #             "address_url": environments.DEFAULT_APIM_ADDRESS_URL,
    #             "bearer": environments.DEFAULT_APIM_TOKEN,
    #             "authn_type": Auth_Type.PERSONAL_ACCESS_TOKEN.name.lower(),
    #             "authn_name": "Environment Token"
    #         }

    #         if environments.DEFAULT_APIM_ORG:
    #             default_value["org"] = environments.DEFAULT_APIM_ORG

    #         if environments.DEFAULT_APIM_ENV:
    #             default_value["env"] = environments.DEFAULT_APIM_ENV

    #     else:
    #         default_value = {
    #             "address_url": environments.DEFAULT_APIM_ADDRESS_URL
    #         }

    #     return default_value

    def get_env_values(self):
        if environments.DEFAULT_APIM_TOKEN:
            default_value = {
                "address_url": environments.DEFAULT_APIM_ADDRESS_URL,
                "bearer": environments.DEFAULT_APIM_TOKEN,
                "authn_type": Auth_Type.PERSONAL_ACCESS_TOKEN.name.lower(),
                "authn_name": "Environment Token"
            }

            if environments.DEFAULT_APIM_ORG:
                default_value["org"] = environments.DEFAULT_APIM_ORG

            if environments.DEFAULT_APIM_ENV:
                default_value["env"] = environments.DEFAULT_APIM_ENV

        else:
            default_value = {
                "address_url": environments.DEFAULT_APIM_ADDRESS_URL
            }

        return default_value

    def display_profile(self):
        to_return = {}

        if self.data and "address_url" in self.data:
            to_return = {
                "address_url": self.data["address_url"],
                "authentification": self.display_auth_list()
            }
        if self.data and "env" in self.data:
            to_return["environments"] = self.data["env"]

        if self.data and "org" in self.data:
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
        address_url = self.data["address_url"]

        org_and_env = "organizations/{}/environments/{}/".format(self.data["org"], self.data["env"]) if "env" in self.data and "org" in self.data else ""
        return address_url + path.format(org_and_env)
