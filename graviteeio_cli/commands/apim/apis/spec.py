import click

from .spec_group.apply import apply


@click.group(short_help="Manage API Configuration from API spec")
@click.pass_context
def spec(ctx):
    """This group allow handling commands regarding API specification."""
    pass


spec.add_command(apply)
