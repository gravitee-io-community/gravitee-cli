import logging

import click

from graviteeio_cli.http_client.apim.api import ApiClient
from graviteeio_cli.core.output import OutputFormatType

from .utils import filter_api_values

logger = logging.getLogger("command-apim-get")


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
    Get api configuration.
    """
    api_client: ApiClient = obj['api_client']

    api_server = api_client.get_export(api_id, filter_api_values)

    OutputFormatType.value_of(output).echo(api_server)
