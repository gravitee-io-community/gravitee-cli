import click

from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.http_client.apim.api import ApiClient


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

    try:
        with open(file, 'r') as f:
            api_spec = f.read()
    except FileNotFoundError:
        raise GraviteeioError("Missing values file {}".format(file))

    if api_id:
        resp = api_client.update_oas(api_id, api_spec)
        click.echo("API {} is updated".format(api_id))
    else:
        click.echo("Start Create")
        resp = api_client.create_oas(api_spec)
        click.echo("API has been created with id {}".format(resp["id"]))
