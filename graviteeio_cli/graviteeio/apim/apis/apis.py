import os
import sys

import click
from graviteeio_cli.graviteeio.modules import GraviteeioModule

from graviteeio_cli.graviteeio.client.gio_resources import APIM_Client
from .plugins import COMMANDS
import pkgutil

add_command = ["list", "start", "stop", "deploy", "status", "health", "fetch", "definition", "spec", "get", "logs"]

class PluginCommand(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []

        if COMMANDS:
            rv.extend(COMMANDS)

        rv.extend(add_command)
        rv.sort()
        
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            
            methode_name = name
            if name in add_command:
                if name == 'list': methode_name = "ls"
                mod = __import__('graviteeio_cli.graviteeio.apim.apis.' + methode_name, None, None, [methode_name])
            else:
                mod = __import__('graviteeio_cli.graviteeio.apim.apis.plugins.cmd_' + methode_name, None, None, [methode_name])
        except ImportError:
            return

        return getattr(mod, methode_name)


@click.command(cls=PluginCommand)
@click.pass_context
def apis(ctx):
    """
    This group includes the commands regarding apis.
    """
    ctx.obj['api_client'] = APIM_Client.API.http(ctx.obj['config'])
    # ctx.obj['api_client'] = GioClient.APIM(config=ctx.obj['config'].getGraviteeioConfig(GraviteeioModule.APIM), http_client_type = APIM_client_type.API)
