import click
from graviteeio_cli.commands.apim.pages.fetch import fetch
from graviteeio_cli.commands.apim.pages.update import update_content
from graviteeio_cli.commands.apim.pages.get import get
from graviteeio_cli.http_client.gio_resources import APIM_Client


@click.group()
@click.pass_context
def pages(ctx):
    """
    This group includes the commands regarding documentation pages.
    """
    ctx.obj['page_client'] = APIM_Client.PAGE.http(ctx.obj['config'])


pages.add_command(fetch)
pages.add_command(update_content)
pages.add_command(get)
