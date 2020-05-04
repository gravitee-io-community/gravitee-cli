import logging
import os

import click

from ..utils import filter_api_values
from .api_schema import ApiSchema, Data_Template_Format

logger = logging.getLogger("command-generate")

@click.command()
@click.option('--config-path', type=click.Path(exists=False), required=False, default="./",
              help="Config folder")
@click.option('--format', 
              default="yaml",
              help='Generated format. Default: `yaml`',
              type=click.Choice(Data_Template_Format.list_name(), case_sensitive=False))
@click.option('--from-id', 
              help='generate skeleton from existing api', required=False)
@click.pass_obj
def generate(obj, config_path, format, from_id):
    """Generate skeleton template exemple to create or update api"""
    if not os.path.exists(config_path):
        os.mkdir(config_path)

    api_def_string = None
    if from_id:
        api_client = obj['api_client']
        api_def_string = api_client.get_export(from_id).json()
        filter_api_values(api_def_string)

    apischema = ApiSchema(config_path)
    apischema.generate_schema(format = Data_Template_Format.value_of(format), api_def = api_def_string)

