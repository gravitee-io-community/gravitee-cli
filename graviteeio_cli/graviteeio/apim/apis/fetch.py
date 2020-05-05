import click

@click.command()
@click.argument('api_id', required=True)
@click.pass_obj
def fetch(obj, api_id):
    """Fetch API documentation"""
    api_client = obj['api_client']
    api_client.pages_fetch(api_id)
    click.echo("API Documentation is uptodate")