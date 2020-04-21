import click

from .spec_group.apply import apply

@click.group()
# @click.command()
@click.pass_context
def spec(ctx):
    """This group allow handling api spec"""
    pass

spec.add_command(apply)