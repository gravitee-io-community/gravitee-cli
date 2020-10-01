import click

from graviteeio_cli.http_client.apim.api import ApiClient

from ....exeptions import GraviteeioError


@click.command()
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.pass_obj
def deploy(obj, api_id):
    """Deploys API configuration."""
    api_client: ApiClient = obj['api_client']
    try:
        response = api_client.deploy(api_id)
    except GraviteeioError:
        click.echo("Error: " + click.style("API [{}]could not be deployed.".format(api_id), fg="red"))

    click.echo("API [{}] is deployed.".format(api_id))
