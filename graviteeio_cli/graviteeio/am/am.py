import click

from graviteeio_cli.graviteeio.modules import GraviteeioModule

from .auth.auth import auth


@click.group()
@click.pass_context
def am(ctx):
    "This group includes all commands regarding Access Management tool."
    ctx.obj['module'] = GraviteeioModule.AM
    pass


am.add_command(auth)
