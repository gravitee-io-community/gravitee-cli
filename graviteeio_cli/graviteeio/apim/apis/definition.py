import click

from .definition_group.apply import apply
from .definition_group.diff import diff
from .definition_group.generate import generate
from .definition_group.create import create

@click.group()
@click.pass_context
def definition(ctx):
    """This group allow handling API definition commands from templating and value files"""
    pass

definition.add_command(apply)
definition.add_command(diff)
definition.add_command(create)
definition.add_command(generate)