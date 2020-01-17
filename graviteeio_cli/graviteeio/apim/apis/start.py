import click

@click.command()
@click.argument('api_id', required=True)
@click.pass_obj
def start(obj, api_id):
    """This command allow to start an API"""
    api_client = obj['api_client']
    api_client.start(api_id)
    click.echo("API {} is started".format(api_id))