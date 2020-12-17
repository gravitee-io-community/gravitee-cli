import click

from graviteeio_cli.http_client.apim.api import ApiClient

from ....exeptions import GraviteeioError


@click.command()
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.pass_obj
def stop(obj, api_id):
    """Stops an API."""
    api_client: ApiClient = obj['api_client']
    try:
        api_client.stop(api_id)
        click.echo(f"API [{api_id}] is stopped.")
    except GraviteeioError:
        click.echo("Error: " + click.style(f"API [{api_id}]could not be stopped.", fg="red"))
