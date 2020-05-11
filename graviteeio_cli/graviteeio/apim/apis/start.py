import click

from ....exeptions import GraviteeioError

@click.command()
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.pass_obj
def start(obj, api_id):
    """Start an API"""
    api_client = obj['api_client']
    try:
        response = api_client.start(api_id)
    except GraviteeioError:
        click.echo("Error: " + click.style("API [{}]could not be started".format(api_id), fg="red"))
    
    click.echo("API [{}] is started".format(api_id))