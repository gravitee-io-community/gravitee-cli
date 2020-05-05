import click

@click.command()
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.pass_obj
def deploy(obj, api_id):
    """Deploy API configuration"""
    api_client = obj['api_client']
    api_client.deploy(api_id)
    click.echo("API {} is deployed".format(api_id))