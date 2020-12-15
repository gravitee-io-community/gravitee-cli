import logging
import click

from graviteeio_cli.services import lint_service
from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.lint.types.document import DocumentType
from graviteeio_cli.core.config import GraviteeioConfig



logger = logging.getLogger("command-apim-spec-lint")


@click.command(short_help="Check format of api definition configuration generated.")
@click.option('--api', 'api_id',
              help='API id',
              required=False)
@click.option('--file', '-f', type=click.Path(exists=True), required=True,
              help="Spec file (Swagger 2.0 / OAS 3.0)")
@click.pass_obj
def lint(obj, api_id, file):
    """This command allow to run a serie of tests to verify that api specification is correctly formed."""

    try:
        with open(file, 'r') as f:
            api_spec = f.read()
    except FileNotFoundError:
        raise GraviteeioError("Missing values file {}".format(file))

    gio_config: GraviteeioConfig = obj['config']
    lint_service.validate_from_file(file, api_spec, DocumentType.oas, gio_config.linter_conf)
