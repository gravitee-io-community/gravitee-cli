import click

from graviteeio_cli.modules.gio_module import GioModule

from .auth.auth import auth


@click.group()
@click.pass_context
def am(ctx):
    "This group includes all commands regarding Access Management tool."
    ctx.obj['module'] = GioModule.AM
    pass


am.add_command(auth)
