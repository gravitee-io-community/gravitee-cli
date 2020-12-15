import logging

import click
from graviteeio_cli.resolvers.api_conf_resolver import ApiConfigResolver
from graviteeio_cli.services import lint_service
from graviteeio_cli.lint.types.document import DocumentType
from graviteeio_cli.core.config import GraviteeioConfig

# from graviteeio_cli.http_client.apim.api import ApiClient


logger = logging.getLogger("command-apim-def-lint")


@click.command(short_help="Check format of api definition configuration generated.")
@click.option(
    '--def-path', 'config_path', default=".",
    type=click.Path(exists=False),
    required=False,
    help="Path where api definition is generated. The default value is the current directory"
)
@click.option(
    '--file', '-f',
    type=click.Path(exists=True), required=False,
    help="Value file"
)
@click.option(
    '--set', '-s', multiple=True,
    help="Overload the value(s) of value file eg: `--set proxy.groups[0].name=mynewtest`"
)
@click.pass_obj
def lint(obj, config_path, file, set):
    """This command allow to run a serie of tests to verify that api definition configuration is correctly formed."""
    gio_config: GraviteeioConfig = obj['config']

    api_resolver = ApiConfigResolver(config_path, file)
    api_def_config = api_resolver.get_api_data(debug=False, set_values=set)

    lint_service.validate(api_def_config, DocumentType.gio_apim, gio_config.linter_conf, display_summary=True)
