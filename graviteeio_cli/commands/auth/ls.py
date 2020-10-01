# Credentialed accounts
import click

from graviteeio_cli.core.output import OutputFormatType


@click.command(short_help="Display account authenticated")
@click.option('--output', '-o',
              default="table", show_default=True,
              help='Set the format for printing command output resources.',
              type=click.Choice(OutputFormatType.list_name(), case_sensitive=False))
@click.pass_obj
def ls(obj, output):
    """
    This command display the account autenticated.
    """
    auth_list = obj['config'].getGraviteeioConfig(obj['module']).display_auth_list()

    outputFormatType = OutputFormatType.value_of(output)

    if auth_list:
        outputFormatType.echo(auth_list, header=["Name", "Type"])
    else:
        click.echo("No authentiication.")
