import click

from graviteeio_cli.http_client.gio_resources import AM_Client

from graviteeio_cli.commands.auth.login import login
from graviteeio_cli.commands.auth.logout import logout
from graviteeio_cli.commands.auth.ls import ls


@click.group()
@click.pass_context
def auth(ctx):
    """
    This group includes the commands regarding authentication.
    """
    ctx.obj['auth_client'] = AM_Client.AUTH.http(ctx.obj['config'])


auth.add_command(login)
auth.add_command(logout)
auth.add_command(ls, "list")
