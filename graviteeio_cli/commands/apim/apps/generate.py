import logging
import os

import click

from graviteeio_cli.http_client.apim.app import AppClient

from graviteeio_cli.core.dic_filter_data import filter_app_values
from graviteeio_cli.resolvers.conf_resolver import ConfigResolver, Config_Type, CONFIG_FORMATS
from graviteeio_cli.core.file_format import File_Format_Enum

logger = logging.getLogger("command-apps-generate")


@click.command(short_help="Generate application.")
@click.option(
    '--def-path', 'config_path', default=".",
    type=click.Path(exists=False),
    required=False,
    help="Path where app definition is generated. The default value is the current directory"
)
@click.option(
    '--format', default="yaml",
    show_default=True,
    type=click.Choice(list(map(lambda f: f.name.lower(), CONFIG_FORMATS)), case_sensitive=False),
    help='Generated format.',
)
@click.option(
    '--from-id',
    help='Generate templates and value file from existing app', required=False
)
@click.pass_obj
def generate(obj, config_path, format, from_id):
    """Generate default templates, setting and value files for api definition"""
    if not os.path.exists(config_path):
        os.mkdir(config_path)

    app_string = None
    if from_id:
        app_client: AppClient = obj['app_client']
        app_string = app_client.get_export(from_id, filter_app_values)

    resolver = ConfigResolver(config_path)

    resolver.generate_init(
        Config_Type.APP,
        format=File_Format_Enum.value_of(format),
        config_values=app_string
    )
