import click

from .apis.apis import apis
from .auth.auth import auth
from graviteeio_cli.modules.gio_module import GioModule


@click.group(invoke_without_command=False)
@click.pass_context
def apim(ctx):
    "This group includes all commands regarding Api Management tool."
    ctx.obj['module'] = GioModule.APIM
    pass


apim.add_command(apis)
apim.add_command(auth)
