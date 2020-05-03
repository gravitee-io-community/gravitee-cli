import os
import sys

import click
from graviteeio_cli.environments import GraviteeioModule

from ..client.api import api_client
from .plugins import COMMANDS
import pkgutil

add_command = ["ps", "init", "start", "stop", "deploy", "status", "health", "fetch", "definition", "spec", "get"]

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
            if name in add_command:
                mod = __import__('graviteeio_cli.graviteeio.apim.apis.' + name, None, None, [name])
            else:
                mod = __import__('graviteeio_cli.graviteeio.apim.apis.plugins.cmd_' + name, None, None, [name])
        except ImportError:
            return
        return getattr(mod, name)


@click.command(cls=PluginCommand)
@click.pass_context
def apis(ctx):
    """
    apis commands
    """
    ctx.obj['api_client'] = api_client(config=ctx.obj['config'].getGraviteeioConfig(GraviteeioModule.APIM))
