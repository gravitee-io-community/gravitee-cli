import click, configparser, os, requests

from .. import environments

from ..exeptions import GraviteeioError

#texttable

@click.group()
def config():
    pass

@click.command()
@click.option('--user', help='authentication user')
@click.option('--pwd', help='authentication password')
@click.option('--url', help='gravitee Rest Management Url')
@click.option('--env', help='config environment')
@click.option('--load', help='load an environment saved')
def update(user, pwd, url, env, load):
    """update configuration"""

    try:
        if user or pwd or url or env or load:
            config = Graviteeio_configuration()
            old_env = config.env
            config.save(user, pwd, url, env, load)
            
            click.echo("Save")
            if env:
                click.echo("Switch env from {} to {}".format(old_env, env))
        
    except GraviteeioError as error:
        click.echo(click.style("Error: ", fg='red') + 'No environment " %s " found' % load , err=True)

@click.command()
def show():
    """display current configuration"""
    config = Graviteeio_configuration()
    click.echo("Current Config:")
    click.echo("{}".format(config.display_current_env()))

config.add_command(update)
config.add_command(show)

class Graviteeio_configuration:
        user = environments.DEFAULT_USER
        password = environments.DEFAULT_PASSWORD
        address_url = environments.DEFAULT_ADDRESS_URL
        

        def __init__(self, config_file = environments.GRAVITEEIO_CONF_FILE): 

            self.config = configparser.ConfigParser()

            if not os.path.isfile(config_file):
                self.env = "DEFAULT"
                #elf.config.add_section(self.env)
                self.config.set(self.env, "user", self.user)
                self.config.set(self.env, "password", self.password)
                self.config.set(self.env, "address_url", self.address_url)
                self.config.set(self.env, "env", self.env)
                #self.config['DEFAULT'] = {'user' : self.user, 'password': self.password, 'url': self.url, 'env': self.env}
                
                with open(config_file, 'w') as fileObj:
                    self.config.write(fileObj)
            else:
                self.config.read(config_file)
                self.env = self.config['DEFAULT']['env']
                self.user = self.config[self.env]['user']
                self.password = self.config[self.env]['password']
                self.address_url = self.config[self.env]['address_url']

            self.http_proxy = os.environ.get("http_proxy")
            self.https_proxy = os.environ.get("https_proxy")
            self.proxyDict = {
                "http"  : self.http_proxy,
                "https" : self.https_proxy
            }
        
        def _change_values(self, user, password, url, env = 'DEFAULT'):
            if env is None:
                env = "DEFAULT"

            if not self.config.has_section(env) and env != "DEFAULT":
                self.config.add_section(env)
            print(env)
            if user:
                self.config.set(env, "user", user)
                #self.config[env]['user'] = user
            if password:
                 self.config.set(env, "password", password)
            if url:
                self.config.set(env, "address_url", url)
        
        def _load_values(self, load):
            if self.config.has_section(load) or load == "DEFAULT":
                self.env = load
                self.user = self.config[self.env]['user']
                self.password = self.config[self.env]['password']
                self.address_url = self.config[self.env]['address_url']
                self.config['DEFAULT']['env'] = load
            else:
                raise GraviteeioError('No environment " %s " found' % load)


        def save(self, user, password, url, env, load):
            changes = False
            
            if user or password or url or env or load:
                changes = True
            
            self._change_values(user, password, url, env)
            if load:
                self._load_values(load)
            else:
                self._load_values(self.env)

            if changes:
                with open(environments.GRAVITEE_CLI_CONF_FILE, 'w') as fileObj:
                        self.config.write(fileObj)
            
            return changes

        def url(self, path):
            return self.address_url + path;
        
        def credential(self):
            return (self.user, self.password)
        
        def load_http(self, http):
            if 'connectTimeout' not in http:
                http['connectTimeout'] = self.config.getint("HTTP", "connectTimeout", fallback = environments.GRAVITEE_CLI_HTTP_CONNECTION_TIMEOUT)
            if 'idleTimeout' not in http:
                http['idleTimeout'] = self.config.getint("HTTP", "idleTimeout", fallback = environments.GRAVITEE_CLI_HTTP_IDLE_TIMEOUT)
            if 'readTimeout' not in http:
                http['readTimeout'] = self.config.getint("HTTP", "readTimeout", fallback = environments.GRAVITEE_CLI_HTTP_READ_TIMEOUT)
            if 'maxConcurrentConnections' not in http:
                http['maxConcurrentConnections'] = self.config.getint("HTTP", "maxConcurrentConnections", fallback = environments.GRAVITEE_CLI_HTTP_MAX_CONCURRENT_CONNECTION)
            if 'keepAlive' not in http:
                http['keepAlive'] = self.config.getboolean("HTTP", "keepAlive", fallback = environments.GRAVITEE_CLI_HTTP_KEEP_ALIVE)
            if 'pipelining' not in http:
                http['pipelining'] = self.config.getboolean("HTTP", "pipelining", fallback = environments.GRAVITEE_CLI_HTTP_PIPELINING)
            if 'useCompression' not in http:
                http['useCompression'] = self.config.getboolean("HTTP", "useCompression", fallback = environments.GRAVITEE_CLI_HTTP_USE_COMPRESSION)
            if 'followRedirects' not in http:
                http['followRedirects'] = self.config.getboolean("HTTP", "followRedirects", fallback = environments.GRAVITEE_CLI_HTTP_FOLLOW_REDIRECTS)
        
        def display_current_env(self):
            toreturn = []

            toreturn.append(" - URL: {}\n".format(self.address_url))
            toreturn.append(" - User: {}\n".format(self.user))
            toreturn.append(" - Password: {}\n".format(self.password))
            toreturn.append(" - Environment: %s\n" % self.env)
            if self.http_proxy:
                toreturn.append(" - http_proxy: %s\n" % self.http_proxy)
            if self.http_proxy:
                toreturn.append(" - https_proxy: %s\n" % self.https_proxy)
            return ''.join(toreturn)

