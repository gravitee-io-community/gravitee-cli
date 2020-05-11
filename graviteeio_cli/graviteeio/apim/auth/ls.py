# Credentialed accounts
import logging
import click

from graviteeio_cli.graviteeio.modules import GraviteeioModule
from graviteeio_cli.graviteeio.output import OutputFormatType


@click.command()
@click.option('--output', '-o', 
              default="table",
              help='Set the format for printing command output resources. Default: `table`',
              type=click.Choice(OutputFormatType.list_name(), case_sensitive=False))
@click.pass_obj
def ls(obj, output):

    auth_list = obj['config'].getGraviteeioConfig(GraviteeioModule.APIM).display_auth_list()

    outputFormatType = OutputFormatType.value_of(output)

    header = None

    if auth_list:
        outputFormatType.echo(auth_list, header = ["username", "type"])
    else:
        click.echo("No auth")
