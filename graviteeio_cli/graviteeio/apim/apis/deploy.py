import click

@click.command()
@click.argument('api_id', required=True)
@click.pass_obj
def deploy(obj, api_id):
    """This command allow to deploy API configuration"""
    api_client = obj['api_client']
    api_client.deploy(api_id)
    click.echo("API {} is deployed".format(api_id))