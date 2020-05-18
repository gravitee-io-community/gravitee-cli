import click

from graviteeio_cli.graviteeio.modules import GraviteeioModule
from graviteeio_cli.graviteeio.client.gio_resources import APIM_Client

from .login import login
from .logout import logout
from .ls import ls
from .create import create
from .load import load

@click.group()
@click.pass_context
def auth(ctx):
    """
    authentication commands
    """
    ctx.obj['auth_client'] = APIM_Client.AUTH.http(ctx.obj['config'])
    # ctx.obj['auth_client'] = GioClient.APIM(config=ctx.obj['config'].getGraviteeioConfig(GraviteeioModule.APIM), http_client_type = APIM_client_type.AUTH)

auth.add_command(login)
auth.add_command(logout)
auth.add_command(ls, "list")
# auth.add_command(create)
# auth.add_command(load)
