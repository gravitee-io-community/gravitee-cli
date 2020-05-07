import click

from ....exeptions import GraviteeioError

@click.command()
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.pass_obj
def deploy(obj, api_id):
    """Deploy API configuration"""
    api_client = obj['api_client']
    try:
        response = api_client.deploy(api_id)
    except GraviteeioError:
        click.echo("Error: " + click.style("API could not be deployed", fg="red"))

    click.echo("API {} is deployed".format(api_id))