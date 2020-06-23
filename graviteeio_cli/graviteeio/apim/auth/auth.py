import click

from graviteeio_cli.graviteeio.modules import GraviteeioModule
from graviteeio_cli.graviteeio.client.gio_resources import APIM_Client

from graviteeio_cli.graviteeio.auth.login import login
from graviteeio_cli.graviteeio.auth.logout import logout
from graviteeio_cli.graviteeio.auth.ls import ls
from graviteeio_cli.graviteeio.apim.auth.token import token


@click.group()
@click.pass_context
def auth(ctx):
    """
    This group includes the commands regarding authentication.
    """
    ctx.obj['auth_client'] = APIM_Client.AUTH.http(ctx.obj['config'])

auth.add_command(login)
auth.add_command(logout)
auth.add_command(ls, "list")
auth.add_command(token)
# auth.add_command(create)
# auth.add_command(load)
