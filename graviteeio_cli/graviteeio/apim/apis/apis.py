import click

from .ps import ps
from .actions import start, stop, deploy
from .update import update, create
from .load_template import init, upgrade
from ..client.api import api_client


@click.group()
@click.pass_context
def apis(ctx):
    ctx.obj['api_client'] = api_client(config=ctx.obj['config'])


apis.add_command(ps)
apis.add_command(start)
apis.add_command(stop)
apis.add_command(deploy)
apis.add_command(init)
apis.add_command(upgrade)
apis.add_command(update)
apis.add_command(create)
