import click

from graviteeio_cli.http_client.gio_resources import APIM_Client
from .ls import ls
from .apply import apply
from .generate import generate


@click.group()
@click.pass_context
def apps(ctx):
    """
    This group includes the commands regarding application.
    """
    ctx.obj['app_client'] = APIM_Client.APP.http(ctx.obj['config'])


apps.add_command(ls, "list")
apps.add_command(apply, "apply")
apps.add_command(generate, "generate")
