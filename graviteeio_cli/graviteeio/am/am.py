import click

from graviteeio_cli.graviteeio.modules import GraviteeioModule

from .auth.auth import auth


@click.group()
@click.pass_context
def am(ctx):
    "Access Management commmands"
    ctx.obj['module'] = GraviteeioModule.AM
    pass


am.add_command(auth)
