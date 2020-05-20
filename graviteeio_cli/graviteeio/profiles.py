import click

from .. import environments
from ..exeptions import GraviteeioError
from .apim.auth.logout import logout
from .client.gio_resources import APIM_Client
from .config import GraviteeioConfig
from .modules import GraviteeioModule
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
@click.option('--url', help='graviteeio module url', required=True)
@click.option('--module', 
                        help='graviteeio module', required=True, 
                    type=click.Choice(GraviteeioModule.list_name(), case_sensitive=False))
@click.option('--environment', "--env", help='config graviteeio environment')
@click.option('--organization', "--org",help='config graviteeio organization')
@click.argument('profile_name', required=True)
@click.pass_obj
def create(obj, profile_name, module, url, environment, organization):
    """This command create a new profile configuration according to module"""

    gio_config:GraviteeioConfig = obj['config']

    if not is_uri_valid(url):
        raise GraviteeioError('URL [%s] not valid.' % url)

    data = {
        "address_url": url
    }
    
    if environment:
        data["env"] = environment
    if organization:
        data["org"] = organization

    gio_config.save(profile = profile_name, module = module, **data)

    click.echo("Data saved for profile [{}].".format(profile_name))

@click.command()
@click.option('--url', help='graviteeio module url')
@click.option('--environment', "--env", help='config graviteeio environment')
@click.option('--organization', "--org",help='config graviteeio organization')
@click.option('--module', 
                        help='graviteeio module', required=True,
                    type=click.Choice(GraviteeioModule.list_name(), case_sensitive=False))
@click.argument('profile_name', required=True)
@click.pass_obj
def set_(obj, profile_name, module, url, environment, organization):
    """This command writes configuration values according to profile and module"""

    gio_config:GraviteeioConfig = obj['config']

    if url or environment or organization:
        data = {}

        if url:
            if not is_uri_valid(url):
                raise GraviteeioError('URL " %s " not valid' % url)
            
            data["address_url"] = url
        if environment:
            data["env"] = environment
        
        if organization:
            data["org"] = organization

        gio_config.save(profile = profile_name, module = module, **data)
        click.echo("Profile data saved")


@click.command()
@click.option('--output', '-o',  
              default="table",
              help='Set the format for printing command output resources. The supported formats are: `table`, `json`, `yaml`, `tsv`.',
              show_default=True,
              type=click.Choice(OutputFormatType.list_name(), case_sensitive=False))
@click.pass_obj
def ls(obj, output):
    """
    Display profile list
    """
    gio_config:GraviteeioConfig = obj['config']

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
              help='Output format.', show_default=True,
              type=click.Choice(['table','json', 'yaml'], case_sensitive=False))
@click.pass_obj
def get(obj, profile, output):
    """
    Display configuration for the filled profile
    """
    # gio_config = obj['config']
    gio_config =  GraviteeioConfig(obj['path-config'])
    gio_config.load(profile, no_save=True)
    to_display = gio_config.display_profile()

    output = OutputFormatType.value_of(output)
    if(output == OutputFormatType.TABLE):
        click.echo("")
        output.echo([], header= ["Profile: "+ to_display['profile']])
        for module in to_display['modules']:
            # data_to_display = {}
            # for key, value in module.items():
            #     if type(value) is list:
            #         data_to_display[key] = output.output.string(value,header=["",""])
            #     else:
            #         data_to_display[key] = value
                
            output.echo(module, header = [""])

    else:
        output.echo(to_display)

@click.command()
@click.argument('profile_name', required=True)
@click.pass_obj
def remove(obj, profile_name):
    """remove profile"""

    gio_config:GraviteeioConfig = obj['config']
    gio_config.remove(profile = profile_name)

    click.echo("Profile [%s] removed." % profile_name)

@click.command()
@click.argument('profile_name', required=True)
@click.pass_context
def load(ctx, profile_name):
    """
    Load current profile
    """
    gio_config:GraviteeioConfig = ctx.obj['config']
    old_profile = gio_config.profile

    if gio_config.config_module[GraviteeioModule.APIM] and gio_config.config_module[GraviteeioModule.APIM].is_logged_in():
        ctx.obj['auth_client'] = APIM_Client.AUTH.http(ctx.obj['config'])
        ctx.invoke(logout)

    gio_config.load(profile_name)
    click.echo("Switch profile from [{}] to [{}].".format(old_profile, profile_name))


profiles.add_command(ls, name = "list")
profiles.add_command(get)
profiles.add_command(set_, name="set")
profiles.add_command(load)
profiles.add_command(create)
profiles.add_command(remove)

