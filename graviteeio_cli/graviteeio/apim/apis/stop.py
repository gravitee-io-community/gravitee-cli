import click

@click.command()
@click.argument('api_id', required=True)
@click.pass_obj
def stop(obj, api_id):
    """This command allow to stop an API"""
    api_client = obj['api_client']
    resp = api_client.stop(api_id)
    click.echo("API {} is stopped".format(api_id))