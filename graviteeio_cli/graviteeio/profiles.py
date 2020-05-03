import configparser
import enum
import os
import json

import click

from .. import environments
from ..environments import GraviteeioModule
from ..exeptions import GraviteeioError
from .output import OutputFormatType

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
def set(obj, profile_name, module, user, pwd, url, env):
    """This command writes configuration values according to profile and module"""

    gio_config = obj['config']
    try:
        if user or pwd or url or env:
            data = {}
            if user:
             data["user"] = user
            if pwd:
             data["password"] = pwd
            if url:
             data["address_url"] = url
            if env:
             data["env"] = env

            gio_config.save(profile_name, module, data)

            click.echo("Profile data saved")

    except GraviteeioError:
        click.echo(click.style("Error: ", fg='red') + 'No profile " %s " found' % load, err=True)


@click.command()
@click.option('--output', '-o',  
              default="table",
              help='Set the format for printing command output resources. The supported formats are: `table`, `json`, `yaml`, `tsv`. Default is: `table`',
              type=click.Choice(OutputFormatType.list_name(), case_sensitive=False))
@click.pass_obj
def list(obj, output):
    """
    Display profile list
    """
    gio_config = obj['config']

    profiles = gio_config.profiles()
    new_profiles = []
    for profile in profiles:
        if profile == gio_config.profile:
            new_profiles.append("{} (Current)".format(profile))
        else:
            new_profiles.append(profile)

    OutputFormatType.value_of(output).echo(new_profiles, header = ["Profiles"])


@click.command()
@click.argument('profile', required=True, metavar='[PROFILE]')
# @click.option('--profile', help='print data for the profile filled')
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
@click.option('--user', help='authentication user', required=True)
@click.option('--pwd', help='authentication password', required=True)
@click.option('--url', help='graviteeio Rest Management url', required=True)
@click.option('--module', 
                        help='graviteeio module', required=True,
                    type=click.Choice(GraviteeioModule.list_name(), case_sensitive=False))
@click.option('--env', help='config graviteeio environment')
@click.argument('profile_name', required=True)
@click.pass_obj
def create(obj, profile_name, module, user, pwd, url, env):
    """This command create a new profile configuration according to module"""

    gio_config = obj['config']
    try:
        data = {
            "user": user,
            "password": pwd,
            "address_url": url
        }
        if env:
            data["env"] = env
        gio_config.save(profile = profile_name, module = module, **data)

        click.echo("Profile data saved")

    except GraviteeioError:
        click.echo(click.style("Error: ", fg='red') + 'No profile " %s " found' % load, err=True)

@click.command()
@click.argument('profile_name', required=True)
@click.pass_obj
def remove(obj, profile_name):
    """This command create a new profile configuration according to module"""

    gio_config = obj['config']
    gio_config.remove(profile = profile_name)

    click.echo("Profile %s removed" % profile_name)

@click.command()
@click.argument('profile_name', required=True)
@click.pass_obj
def load(obj, profile_name):
    """
    This command load profile
    ENVIRONMENT: value that corresponds to the configuration that will be loaded for the execution of commands
    """
    gio_config = GraviteeioConfig()

    old_profile = gio_config.profile
    gio_config.load(profile_name)
    click.echo("Switch profile from {} to {}".format(old_profile, profile_name))


profiles.add_command(list)
profiles.add_command(get)
profiles.add_command(set)
profiles.add_command(load)
profiles.add_command(create)
profiles.add_command(remove)

class GraviteeioConfig:
    def __init__(self, config_file=environments.GRAVITEEIO_CONF_FILE):
        self.config_file = config_file
        self.config = configparser.ConfigParser()

        self.proxies = {
            "http": os.environ.get("http_proxy"),
            "https": os.environ.get("https_proxy")
        }

        self.config_module = {}
        self.config_module[GraviteeioModule.APIM] = GraviteeioConfig_apim(self.config, self.proxies)
        self.config_module[GraviteeioModule.AM] = GraviteeioConfig_am(self.config, self.proxies)

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
            raise GraviteeioError('No profile " %s " accepted' % profile)
        
        self.config.set("DEFAULT", "current_profile", profile)
        with open(self.config_file, 'w') as fileObj:
                self.config.write(fileObj)
        
        self._load_config()

    def _load_config(self):
        self.profile = self.config['DEFAULT']['current_profile']
        for key in self.config_module:
                self.config_module[key].load_config(self.profile)

    def save(self, profile, module, **kwargs):

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
            raise GraviteeioError('No profile " %s " found' % profile)

        self.config.remove_section(profile)

    def display_default(self, parameter_list):
        to_return = {}
        to_return["-- Default --"] = ""

        for key, value in self.proxies.items():
            to_return[key] = "{}".format(value)

        return to_return


    def display_current_profile(self, profile = None):
        profile = self.config["DEFAULT"]["current_profile"]
        
        to_return = {
            "-- Default --": ""
        }

        to_return["Profile"] = "{}".format(profile)

        for key in self.config_module:
            to_return["## Module"] = "{}".format(self.config_module[key].module)
            to_return.update(self.config_module[key].display_current())

        return to_return
    
    def display_profile(self, profile):
        if not self.config.has_section(profile):
            raise GraviteeioError('No profile " %s " found' % profile)

        to_return = {
            "Profile": "{}".format(profile)
        }

        for key in self.config_module:
            to_return["## Module"] = "{}".format(self.config_module[key].module)
            to_return.update(self.config_module[key].display_profile(profile))
        
        return to_return

class GraviteeioConfig_abstract:
    def __init__(self, module, config_parser, proxies):
        self.module = module.name
        self.config = config_parser
        self.proxies = proxies
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
            raise GraviteeioError('No profile " %s " found' % profile)
    
    def display_current(self):
        to_return = {}
        if self.data:
            for key, value in self.data.items():
                to_return[key] = "{}".format(value)
        return to_return
    
    def display_profile(self, profile):
        return json.loads(self.config[profile][self.module])

    def url(self, path):
        pass

    def credential(self):
        pass 

class GraviteeioConfig_am(GraviteeioConfig_abstract):
    def __init__(self, config_parser, proxies):
        GraviteeioConfig_abstract.__init__(self,GraviteeioModule.APIM, config_parser, proxies)

    def getInitValues(self):
        return {}

class GraviteeioConfig_apim(GraviteeioConfig_abstract):
    def __init__(self, config_parser, proxies):
        GraviteeioConfig_abstract.__init__(self,GraviteeioModule.APIM, config_parser, proxies)

    def getInitValues(self):
        return {
            "user": environments.DEFAULT_USER,
            "password": environments.DEFAULT_PASSWORD,
            "address_url": environments.DEFAULT_ADDRESS_URL
        }
    
    def url(self, path):
        return self.data["address_url"] + path.format(self.data["env"] + "/" if "env" in self.data else "")

    def credential(self):
        return (self.data["user"], self.data["password"])

# class Graviteeio_Config_abstract:

#     def __init__(self, module, config_file=environments.GRAVITEEIO_CONF_FILE):

#         self.config_file = config_file
#         self.module = module.name
#         self.config = configparser.ConfigParser()

#         if not os.path.isfile(config_file):

#             self.profile = "demo"
#             self.config['DEFAULT'] = {
#                 "current_profile": self.profile
#             }
#             self.set_data(self.init_value_demo())
#             self._writes_config(self.profile, self.init_value_demo())
#             # self._writes_config(self.profile, self.data, is_new_current_profile = True)

#         else:
#             self.config.read(config_file)
#             self._load_config(
#                 self.config['DEFAULT']['current_profile']
#             )

#         self.http_proxy = os.environ.get("http_proxy")
#         self.https_proxy = os.environ.get("https_proxy")
#         self.proxyDict = {
#             "http": self.http_proxy,
#             "https": self.https_proxy
#         }
    
#     def init_value_demo(self):
#         pass

#     def set_data(self, data):
#         pass

#     def get_data(self):
#         pass
    
#     def to_display(self):
#         pass

#     def _writes_config(self, profile, data = None):
#         if (not self.config.has_section(profile)) :
#             self.config.add_section(profile)

#         if data:
#             self.config.set(profile, self.module, json.dumps(data))

#         with open(self.config_file, 'w') as fileObj:
#             self.config.write(fileObj)

#     def _load_config(self, load_profile):
#         if self.config.has_section(load_profile):
#             self.profile = load_profile
#             self.set_data(json.loads(self.config[self.profile][self.module]))
#         else:
#             raise GraviteeioError('No profile " %s " found' % load_profile)
    
#     def save(self, profile, **kwargs):
#         if (not self.config.has_section(profile)):
#             self._writes_config(profile, kwargs)
#         else:
#             new_data = kwargs

#             current_data = json.loads(self.config[profile][self.module])
#             for key in new_data:
#                 current_data[key] = new_data[key]
            
#             self._writes_config(profile, current_data)

#     def load(self, profile):
#         if profile is "DEFAULT":
#             raise GraviteeioError('No profile " %s " accepted' % profile)
        
#         self.profile = profile
#         self.config.set("DEFAULT", "current_profile", profile)
#         self._writes_config(profile)

#     def profiles(self):
#         return self.config.sections()

#     def url(self, path):
#         return self.get_data()["address_url"] + path.format(self.get_data()["env"] + "/" if "env" in self.get_data() else "")

#     def credential(self):
#         return (self.get_data()["user"], self.get_data()["password"])
    
#     def to_display(self):
#         profile = self.config["DEFAULT"]["current_profile"]

#         to_return = {
#             "Profile": "{}".format(profile.upper())
#         }

#         for module_name in environments.GraviteeioModule.list_name():
#             to_return["Module"] = "{}".format(module_name)
            
#             if self.config.has_section(profile):
#                 data_module = json.loads(self.config[profile][module_name.upper()])

#                 for (key, value) in data_module:
#                     to_return[key] = "{}".format(value)

#         if self.http_proxy:
#             to_return["http_proxy"] = "{}".format(self.http_proxy)
#         if self.http_proxy:
#             to_return["https_proxy"] = "{}".format(self.https_proxy)

#         return to_return


# class Graviteeio_Config_apim(Graviteeio_Config):
#     def __init__(self, config_file=environments.GRAVITEEIO_CONF_FILE):
#         Graviteeio_Config.__init__(self,environments.GraviteeioModule.APIM, config_file)

#     def init_value_demo(self):
#         return {
#             "user": environments.DEFAULT_USER,
#             "password": environments.DEFAULT_PASSWORD,
#             "address_url": environments.DEFAULT_ADDRESS_URL
#         }
    
#     def set_data(self, data):
#         self.data = data
    
#     def get_data(self):
#         return self.data

# class Graviteeio_Config_am(Graviteeio_Config):
#     def __init__(self, config_file=environments.GRAVITEEIO_CONF_FILE):
#         Graviteeio_Config.__init__(self,environments.GraviteeioModule.AM, config_file)
    
#     def init_value_demo(self):
#         return {
#             "user": environments.DEFAULT_USER,
#             "password": environments.DEFAULT_PASSWORD,
#             "address_url": environments.DEFAULT_ADDRESS_URL
#         }
    
#     def set_data(self, data):
#         self.data = data
    
#     def get_data(self):
#         return self.data
    
#     def to_display(self):
#         to_return = {
#             "URL": "{}".format(self.data["address_url"]),
#             "User": "{}".format(self.data["user"]),
#             "Password": "{}".format(self.data["password"]),
#             "Current environment": "{}".format(self.profile),
#         }

#         if "env"in self.data:
#             to_return["env"] = "{}".format(self.data["env"])
#         if self.http_proxy:
#             to_return["http_proxy"] = "{}".format(self.http_proxy)
#         if self.http_proxy:
#             to_return["https_proxy"] = "{}".format(self.https_proxy)

#         return to_return


