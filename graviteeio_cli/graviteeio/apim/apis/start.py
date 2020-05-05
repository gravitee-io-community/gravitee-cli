import click

@click.command()
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.pass_obj
def start(obj, api_id):
    """Start an API"""
    api_client = obj['api_client']
    api_client.start(api_id)
    click.echo("API {} is started".format(api_id))