import logging
import os

import click

from graviteeio_cli.graviteeio.client.apim.api import ApiClient

from ..utils import filter_api_values
from .api_schema import ApiSchema, Data_Template_Format

logger = logging.getLogger("command-apim-def-generate")

@click.command(short_help="Generate api definition.")
@click.option('--config-path', type=click.Path(exists=False), required=False, default="./",
              help="Configuration folder")
@click.option('--format', 
              default="yaml", show_default= True,
              help='Generated format.',
              type=click.Choice(Data_Template_Format.list_name(), case_sensitive=False))
@click.option('--from-id', 
              help='Generate templates and value file from existing api', required=False)
@click.pass_obj
def generate(obj, config_path, format, from_id):
    """Generate default templates, setting and value files for api definition"""
    if not os.path.exists(config_path):
        os.mkdir(config_path)

    api_def_string = None
    if from_id:
        api_client : ApiClient = obj['api_client']
        api_def_string = api_client.get_export(from_id, filter_api_values)

    apischema = ApiSchema(config_path)
    apischema.generate_schema(format = Data_Template_Format.value_of(format), api_def = api_def_string)
