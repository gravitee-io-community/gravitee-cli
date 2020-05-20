import json
import logging

import click

from graviteeio_cli.graviteeio.client.apim.api import ApiClient
from graviteeio_cli.graviteeio.output import OutputFormatType

from .utils import filter_api_values

logger = logging.getLogger("command-get")

@click.command()
@click.option('--output', '-o', 
              default="yaml", show_default=True,
              help='Output format.',
              type=click.Choice(['yaml', 'json'], case_sensitive=False))
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.pass_obj
def get(obj, output, api_id):
    """
    get api configuration
    """
    api_client: ApiClient = obj['api_client']

    api_server = api_client.get_export(api_id, filter_api_values)

    OutputFormatType.value_of(output).echo(api_server)
