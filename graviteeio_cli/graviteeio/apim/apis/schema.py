import click

from .schema_group.apply import apply
from .schema_group.diff import diff
from .schema_group.generate import generate

@click.group()
# @click.command()
@click.pass_context
def schema(ctx):
    """This group allow handling api definition"""
    pass

schema.add_command(apply)
schema.add_command(diff)
schema.add_command(generate)