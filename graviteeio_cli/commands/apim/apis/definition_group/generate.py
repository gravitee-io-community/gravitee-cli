import logging
import os

import click

from graviteeio_cli.http_client.apim.api import ApiClient

from ..utils import filter_api_values
from graviteeio_cli.resolvers.api_conf_resolver import ApiConfigResolver, TEMPLATE_FORMAT
from graviteeio_cli.core.file_format import File_Format_Enum

logger = logging.getLogger("command-apim-def-generate")


@click.command(short_help="Generate api definition.")
@click.option(
    '--def-path', 'config_path', default=".",
    type=click.Path(exists=False),
    required=False,
    help="Path where api definition is generated. The default value is the current directory"
)
@click.option(
    '--format', default="yaml",
    show_default=True,
    type=click.Choice(list(map(lambda f: f.name.lower(), TEMPLATE_FORMAT)), case_sensitive=False),
    help='Generated format.',
)
@click.option(
    '--from-id',
    help='Generate templates and value file from existing api', required=False
)
@click.pass_obj
def generate(obj, config_path, format, from_id):
    """Generate default templates, setting and value files for api definition"""
    if not os.path.exists(config_path):
        os.mkdir(config_path)

    api_def_string = None
    if from_id:
        api_client: ApiClient = obj['api_client']
        api_def_string = api_client.get_export(from_id, filter_api_values)

    api_resolver = ApiConfigResolver(config_path)

    api_resolver.generate_init(
        format=File_Format_Enum.value_of(format),
        api_def=api_def_string
    )
