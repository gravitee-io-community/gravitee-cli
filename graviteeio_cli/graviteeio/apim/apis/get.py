import logging
import json
import click
from graviteeio_cli.graviteeio.output import OutputFormatType
from .utils import filter_api_values

logger = logging.getLogger("command-get")

@click.command()
@click.argument('api_id', required=True)
@click.option('--output', '-o', 
              default="yaml",
              help='Output format. Default: `yaml`',
              type=click.Choice(['yaml', 'json'], case_sensitive=False))
@click.pass_obj
def get(obj, output, api_id):
    """
    get api configuration
    """
    api_client = obj['api_client']

    api_server = api_client.get_export(api_id).json()
    filter_api_values(api_server)

    OutputFormatType.value_of(output).echo(api_server)


