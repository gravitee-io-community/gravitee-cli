import click

from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.http_client.apim.api import ApiClient
from graviteeio_cli.services import lint_service
from graviteeio_cli.lint.types.document import DocumentType
from graviteeio_cli.core.config import GraviteeioConfig


@click.command(short_help="Create/Update an API from spec.")
@click.option('--api', 'api_id',
              help='API id',
              required=False)
@click.option('--file', '-f', type=click.Path(exists=True), required=True,
              help="Spec file (Swagger 2.0 / OAS 3.0)")
@click.pass_obj
def apply(obj, api_id, file):
    """
    Allow to create/update an API from spec API like Swagger or OpenApiSpec (OAS)
    """
    api_client: ApiClient = obj['api_client']
    gio_config: GraviteeioConfig = obj['config']

    try:
        with open(file, 'r') as f:
            api_spec = f.read()
    except FileNotFoundError:
        raise GraviteeioError("Missing values file {}".format(file))

    #lint
    valid = lint_service.validate_from_file(file, api_spec, DocumentType.oas, gio_config.linter_conf)
    if not valid:
        click.echo(click.style(" oas specification has not been applied", fg="red"))
        return

    if api_id:
        resp = api_client.update_oas(api_id, api_spec)
        click.echo("API {} is updated".format(api_id))
    else:
        click.echo("Start Create")
        resp = api_client.create_oas(api_spec)
        click.echo("API has been created with id {}".format(resp["id"]))
