import configparser
import enum
import os

import click

from .. import environments
from ..exeptions import GraviteeioError
from .output import FormatType, OutputFormat, gio


@click.group()
def config():
    """Configuration values are stored in file with structure of INI file. The config file is located `~/graviteeio`.
    
    Each section contains the configuration by environment for each module. Environment can mean staging, production...
    
    Default environment: `demo`. The configuration of demo environment point to `https://demo.gravitee.io/`

    Environment Variables:
    
    * `GRAVITEEIO_CONF_FILE`: The file of CLI conf. Default `~/graviteeio`.
    
    """
    pass


@click.command()
@click.option('--env', help='config environment (e.g staging, production..). Default: current environment loaded')
@click.option('--user', help='authentication user')
@click.option('--pwd', help='authentication password')
@click.option('--url', help='graviteeio Rest Management url')
@click.option('--v_env', help='config virtual graviteeio environment')
@click.pass_obj
def set(obj, user, pwd, url, env, v_env):
    """This command writes configuration values according to environment"""

    gio_config = obj['config']
    try:
        if user or pwd or url or env or load:
            old_env = gio_config.current_env if not env else env
            gio_config.save(user, pwd, url, old_env, v_env)

            click.echo("New config saved")

    except GraviteeioError:
        click.echo(click.style("Error: ", fg='red') + 'No environment " %s " found' % load, err=True)


@click.command()
@click.option('--env', help='print all environments configured', is_flag=True)
@click.option('--format',
              default="table",
              help='Set the format for printing command output resources. The supported formats are: `table`, `json`, `yaml`, `tsv`. Default is: `table`',
              type=click.Choice(FormatType.list_name(), case_sensitive=False))
@click.pass_obj
def get(obj, env, format):
    """
    This command prints current configuration values used
    """
    gio_config = obj['config']
    if not env:
        gio.echo(gio_config.to_display(), OutputFormat.value_of(format), ["Current Config ({})".format(gio_config.current_env), ""])
    else:
        gio.echo(gio_config.environements(), OutputFormat.value_of(format), ["Environments"])
        # click.echo("{}".format(gio_config.get_environements()))


@click.command()
@click.argument('environment', required=True)
@click.pass_obj
def load(obj, environment):
    """
    This command load current environment
    ENVIRONMENT: value that corresponds to the configuration that will be loaded for the execution of commands
    """
    gio_config = obj['config']

    old_env = gio_config.current_env_module()
    gio_config.load(environment)
    click.echo("Switch env from {} to {}".format(old_env, environment))


config.add_command(get)
config.add_command(set)
config.add_command(load)

class GraviteeioModule(enum.IntEnum):
    APIM = 0
    AM = 1

    @staticmethod
    def list_name():
        return list(map(lambda c: c.name, GraviteeioModule))

class GraviteeioConfiguration:

    user = environments.DEFAULT_USER
    password = environments.DEFAULT_PASSWORD
    address_url = environments.DEFAULT_ADDRESS_URL

    def __init__(self, module:GraviteeioModule, config_file=environments.GRAVITEEIO_CONF_FILE):

        self.config = configparser.ConfigParser()
        self.module = module.name

        if not os.path.isfile(config_file):
            # self.env = "DEFAULT"
            self.current_env = self._env("demo")
            self.virtual_env = None
            self.config.add_section(self.current_env)
            # elf.config.add_section(self.env)
            self.config.set(self.current_env, "user", self.user)
            self.config.set(self.current_env, "password", self.password)
            self.config.set(self.current_env, "address_url", self.address_url)
            self.config.set("DEFAULT", self.module + "_current_env", self.current_env)
            # self.config['DEFAULT'] = {'user' : self.user, 'password': self.password, 'url': self.url, 'env': self.env}

            with open(config_file, 'w') as fileObj:
                self.config.write(fileObj)
        else:
            self.config.read(config_file)
            self._load_values(
                self.config['DEFAULT'][self.module + '_current_env']
            )

        self.http_proxy = os.environ.get("http_proxy")
        self.https_proxy = os.environ.get("https_proxy")
        self.proxyDict = {
            "http": self.http_proxy,
            "https": self.https_proxy
        }

    def _change_values(self, user, password, url, env, v_env):
        if not env:
            env = self.current_env
        else:
            env = self._env(env)

        if (not self.config.has_section(env)) and env != "DEFAULT":
            self.config.add_section(env)

        if user:
            self.config.set(env, "user", user)
        if password:
            self.config.set(env, "password", password)
        if url:
            self.config.set(env, "address_url", url)
        if v_env:
            self.config.set(env, "virtual_env", v_env)

    def _load_values(self, load_env):
        if self.config.has_section(load_env):
            self.current_env = load_env
            self.user = self.config[self.current_env]['user']
            self.password = self.config[self.current_env]['password']
            self.address_url = self.config[self.current_env]['address_url']
            self.virtual_env = None
            self.config['DEFAULT'][self.module + "_" + 'current_env'] = self.current_env

            if self.config.has_option(self.current_env,'virtual_env'):
                self.virtual_env = self.config[self.current_env]['virtual_env']
        else:
            raise GraviteeioError('No environment " %s " found' % load)

    def _env(self, env):
        return self.module + "_" + env
    
    def _sub_env(self, env):
        return env[len(self.module + '_'):len(env)]

    def save(self, user, password, url, env, v_env = None):
        changes = False

        if user or password or url or env or v_env:
            self._change_values(user, password, url, env, v_env)
            with open(environments.GRAVITEEIO_CONF_FILE, 'w') as fileObj:
                self.config.write(fileObj)
            changes = True
            
        return changes

    def load(self, env):
        self._load_values(self._env(env))
        with open(environments.GRAVITEEIO_CONF_FILE, 'w') as fileObj:
                self.config.write(fileObj)

    def environements(self):
        return list(map(self._sub_env, self.config.sections()))

    def url(self, path):
        return self.address_url + path.format(self.virtual_env + "/" if self.virtual_env else "");

    def credential(self):
        return (self.user, self.password)

    def current_env_module(self):
            return self._sub_env(self.current_env)

    def load_http(self, http):
        if 'connectTimeout' not in http:
            http['connectTimeout'] = self.config.getint("HTTP", "connectTimeout",
                                                        fallback=environments.GRAVITEE_CLI_HTTP_CONNECTION_TIMEOUT)
        if 'idleTimeout' not in http:
            http['idleTimeout'] = self.config.getint("HTTP", "idleTimeout",
                                                     fallback=environments.GRAVITEE_CLI_HTTP_IDLE_TIMEOUT)
        if 'readTimeout' not in http:
            http['readTimeout'] = self.config.getint("HTTP", "readTimeout",
                                                     fallback=environments.GRAVITEE_CLI_HTTP_READ_TIMEOUT)
        if 'maxConcurrentConnections' not in http:
            http['maxConcurrentConnections'] = self.config.getint("HTTP", "maxConcurrentConnections",
                                                                  fallback=environments.GRAVITEE_CLI_HTTP_MAX_CONCURRENT_CONNECTION)
        if 'keepAlive' not in http:
            http['keepAlive'] = self.config.getboolean("HTTP", "keepAlive",
                                                       fallback=environments.GRAVITEE_CLI_HTTP_KEEP_ALIVE)
        if 'pipelining' not in http:
            http['pipelining'] = self.config.getboolean("HTTP", "pipelining",
                                                        fallback=environments.GRAVITEE_CLI_HTTP_PIPELINING)
        if 'useCompression' not in http:
            http['useCompression'] = self.config.getboolean("HTTP", "useCompression",
                                                            fallback=environments.GRAVITEE_CLI_HTTP_USE_COMPRESSION)
        if 'followRedirects' not in http:
            http['followRedirects'] = self.config.getboolean("HTTP", "followRedirects",
                                                             fallback=environments.GRAVITEE_CLI_HTTP_FOLLOW_REDIRECTS)
    def to_display(self):
        to_return = {
            "URL": "{}".format(self.address_url),
            "User": "{}".format(self.user),
            "Password": "{}".format(self.password),
            "Current environment": "{}".format(self._sub_env(self.current_env)),
        }

        if self.virtual_env:
            to_return["virtual_env"] = "{}".format(self.virtual_env)
        if self.http_proxy:
            to_return["http_proxy"] = "{}".format(self.http_proxy)
        if self.http_proxy:
            to_return["https_proxy"] = "{}".format(self.https_proxy)

        return to_return
