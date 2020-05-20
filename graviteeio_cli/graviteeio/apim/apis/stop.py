import click

from ....exeptions import GraviteeioError
from graviteeio_cli.graviteeio.client.apim.api import ApiClient

@click.command()
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.pass_obj
def stop(obj, api_id):
    """This command allow to stop an API"""
    api_client : ApiClient = obj['api_client']
    try:
        api_client.stop(api_id)
    except GraviteeioError:
        click.echo("Error: " + click.style("API [{}]could not be stopped.".format(api_id), fg="red"))
    
    click.echo("API [{}] is stopped.".format(api_id))