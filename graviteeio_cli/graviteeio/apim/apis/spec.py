import click

from .spec_group.apply import apply

@click.group()
# @click.command()
@click.pass_context
def spec(ctx):
    """Allow handling api spec commands"""
    pass

spec.add_command(apply)