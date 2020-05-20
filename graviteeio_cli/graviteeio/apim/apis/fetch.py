import click

from graviteeio_cli.graviteeio.client.apim.api import ApiClient


@click.command()
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.pass_obj
def fetch(obj, api_id):
    """Fetch API documentation"""
    api_client: ApiClient = obj['api_client']
    api_client.pages_fetch(api_id)
    click.echo("API [{}] Documentation is uptodate.".format(api_id))
