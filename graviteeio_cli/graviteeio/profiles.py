import configparser
import enum
import os
import json

import click

from .. import environments
from .modules import GraviteeioModule
from ..exeptions import GraviteeioError
from .output import OutputFormatType
from .utils import is_uri_valid

@click.group()
def profiles():
    """
    `profiles` command allow to config modules APIM and AM

    Configuration values are stored in file with structure of INI file. The config file is located `~/graviteeio`.
    
    Each section contains the configuration by profile for each module. Environment can mean staging, production...
    
    Default environment: `demo`. The configuration of demo environment point to `https://demo.gravitee.io/`

    Environment Variables:
    
    * `GRAVITEEIO_CONF_FILE`: file of CLI conf. Default `~/graviteeio`.
    
    """
    pass


@click.command()
@click.option('--user', help='authentication user')
@click.option('--pwd', help='authentication password')
@click.option('--url', help='graviteeio Rest Management url')
@click.option('--env', help='config graviteeio environment')
@click.option('--module', 
                        help='graviteeio module', required=True,
                    type=click.Choice(GraviteeioModule.list_name(), case_sensitive=False))
@click.argument('profile_name', required=True)
@click.pass_obj
def set_(obj, profile_name, module, user, pwd, url, env):
    """This command writes configuration values according to profile and module"""

    gio_config = obj['config']

    if user or pwd or url or env:
        data = {}

        if user:
            data["user"] = user
        if pwd:
            data["password"] = pwd
        if url:
            if not is_uri_valid(url):
                raise GraviteeioError('URL " %s " not valid' % url)
            
            data["address_url"] = url
        if env:
            data["env"] = env

        gio_config.save(profile_name, module, data)

        click.echo("Profile data saved")


@click.command()
@click.option('--output', '-o',  
              default="table",
              help='Set the format for printing command output resources. The supported formats are: `table`, `json`, `yaml`, `tsv`. Default is: `table`',
              show_default=True,
              type=click.Choice(OutputFormatType.list_name(), case_sensitive=False))
@click.pass_obj
def ls(obj, output):
    """
    Display profile list
    """
    gio_config = obj['config']

    profiles = gio_config.profiles()
    new_profiles = []
    for profile in profiles:
        if profile == gio_config.profile:
            new_profiles.append("{} (active)".format(profile))
        else:
            new_profiles.append(profile)

    OutputFormatType.value_of(output).echo(new_profiles, header = ["Profiles"])


@click.command()
@click.argument('profile', required=True, metavar='[PROFILE]')
@click.option('--output', '-o',  
              default="table",
              help='Set the format for printing command output resources. The supported formats are: `table`, `json`, `yaml`, `tsv`. Default is: `table`',
              type=click.Choice(OutputFormatType.list_name(), case_sensitive=False))
@click.pass_obj
def get(obj, profile, output):
    """
    Display configuration for the filled profile
    """
    gio_config = obj['config']
    OutputFormatType.value_of(output).echo(gio_config.display_profile(profile), header = ["Configuration", ""])
        

@click.command()
# @click.option('--user', help='authentication user', required=True)
# @click.option('--pwd', help='authentication password', required=True)
@click.option('--url', help='graviteeio Rest Management url', required=True)
@click.option('--module', 
                        help='graviteeio module', required=True,
                    type=click.Choice(GraviteeioModule.list_name(), case_sensitive=False))
@click.option('--env', help='config graviteeio environment')
@click.argument('profile_name', required=True)
@click.pass_obj
def create(obj, profile_name, module, url, env):
    """This command create a new profile configuration according to module"""

    gio_config = obj['config']

    if not is_uri_valid(url):
        raise GraviteeioError('URL [%s] not valid.' % url)

    data = {
        "address_url": url
    }
    
    if env:
        data["env"] = env
    gio_config.save(profile = profile_name, module = module, **data)

    click.echo("Datas saved for profile [{}].".format(profile_name))

@click.command()
@click.argument('profile_name', required=True)
@click.pass_obj
def remove(obj, profile_name):
    """remove profile"""

    gio_config = obj['config']
    gio_config.remove(profile = profile_name)

    click.echo("Profile [%s] removed." % profile_name)

@click.command()
@click.argument('profile_name', required=True)
@click.pass_obj
def load(obj, profile_name):
    """
    Load current profile
    """
    gio_config = GraviteeioConfig()

    old_profile = gio_config.profile
    gio_config.load(profile_name)
    click.echo("Switch profile from [{}] to [{}].".format(old_profile, profile_name))


profiles.add_command(ls, name = "list")
profiles.add_command(get)
profiles.add_command(set_, name="set")
profiles.add_command(load)
profiles.add_command(create)
profiles.add_command(remove)

class Auth_Type(enum.IntEnum):
    CREDENTIAL = 0,
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

    def getGraviteeioConfigData(self, module):
        return self.config_module[module].data
    
    def getGraviteeioConfig(self, module):
        return self.config_module[module]
        
    def profiles(self):
        return self.config.sections()

    def load(self, profile):
        if profile is "DEFAULT":
            raise GraviteeioError('No profile [%s] accepted.' % profile)
        if not self.config.has_section(profile):
            raise GraviteeioError('No profile [%s] found.' % profile)
        
        self.config.set("DEFAULT", "current_profile", profile)
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

    def display_default(self, parameter_list):
        to_return = {}
        to_return["-- Default --"] = ""

        for key, value in self.proxies.items():
            to_return[key] = "{}".format(value)

        return to_return


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
    
    def display_profile(self, profile):
        if not self.config.has_section(profile):
            raise GraviteeioError('No profile [%s] found.' % profile)

        to_return = {
            "Profile": "{}".format(profile)
        }

        for key in self.config_module:
            to_return["## Module"] = "{}".format(self.config_module[key].module)
            to_return.update(self.config_module[key].display_profile(profile))
        
        return to_return

class GraviteeioConfig_abstract:
    def __init__(self, module, config_parser, proxies, graviteeioConfig: GraviteeioConfig):
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
        if self.config.has_section(profile):
            self.data = json.loads(self.config[profile][self.module])
        else:
            raise GraviteeioError('No profile [%s ]found.' % profile)
    
    # def display_current(self):
    #     to_return = {}
    #     if self.data:
    #         for key, value in self.data.items():
    #             to_return[key] = "{}".format(value)
    #     return to_return
    
    def display_profile(self, profile):
        to_return = {}
        datas = json.loads(self.config[profile][self.module])
        to_return["address_url"] = datas["address_url"]
        to_return["auth"] = datas["active_auth"]["username"]
        if "env" in datas:
            to_return["auth"] = datas["env"]

        return to_return

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
        
        if self.data and "auth" in self.data:
            for auth in self.data["auth"]:
                to_return.append({
                    "username": auth["username"],
                    "type": auth["type"],
                    "is_active": "active" if auth["is_active"] else ""
                })
        return to_return
    
    def get_active_auth(self):
        return  self.data["active_auth"] if "active_auth" in self.data else None
    
    def get_bearer(self):
        return self.data["bearer"] if "bearer" in self.data else None

    def get_bearer_header(self):
        return {"Authorization": "Bearer {}".format(self.data["bearer"])} if "bearer" in self.data else None
    
    def load_auth(self, username):
        bearer_old = self.get_bearer()
        beare_new = None

        active_auth = None
        auth_list = self.get_auth_list()
        for auth in auth_list:
            if auth["username"] == username:
                auth["is_active"] = True
                active_auth = auth
                if 'bearer' in auth:
                    beare_new = auth["bearer"]
            elif auth["is_active"]:
                auth["is_active"] = False
                auth["bearer"] = bearer_old

        if not active_auth:
            raise GraviteeioError("Username [{}] not exist.".format(username))

        self.save(auth = auth_list, bearer = beare_new, active_auth = active_auth)


class GraviteeioConfig_am(GraviteeioConfig_abstract):
    def __init__(self, config_parser, proxies, graviteeioConfig: GraviteeioConfig):
        GraviteeioConfig_abstract.__init__(self,GraviteeioModule.APIM, config_parser, proxies, graviteeioConfig)

    def getInitValues(self):
        return {}
 
class GraviteeioConfig_apim(GraviteeioConfig_abstract):
    def __init__(self, config_parser, proxies, graviteeioConfig: GraviteeioConfig):
        GraviteeioConfig_abstract.__init__(self,GraviteeioModule.APIM, config_parser, proxies, graviteeioConfig)

    def getInitValues(self):
        return {
            "address_url": environments.DEFAULT_ADDRESS_URL,
            "active_auth": {"username": environments.DEFAULT_USER, "type": Auth_Type.CREDENTIAL.name.lower()},
            "auth": [
                {"username": environments.DEFAULT_USER, "type": Auth_Type.CREDENTIAL.name.lower(), "is_active": True} 
            ]
        }
    
    def url(self, path):
        return self.data["address_url"] + path.format(self.data["env"] + "/" if "env" in self.data else "")


