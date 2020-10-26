import click

from .definition_group.apply import apply
from .definition_group.diff import diff
from .definition_group.generate import generate
from .definition_group.create import create
from .definition_group.lint import lint


@click.group(short_help="Manage API definition configuration")
@click.pass_context
def definition(ctx):
    """This group allow handling API definition commands from templating and value files"""
    pass


definition.add_command(apply)
definition.add_command(diff)
definition.add_command(create)
definition.add_command(generate)
definition.add_command(lint)
