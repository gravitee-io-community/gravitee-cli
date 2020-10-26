import click

from .spec_group.apply import apply
from .spec_group.lint import lint


@click.group(short_help="Manage API Configuration from API spec")
@click.pass_context
def spec(ctx):
    """This group allow handling commands regarding API specification."""
    pass


spec.add_command(apply)
spec.add_command(lint)
