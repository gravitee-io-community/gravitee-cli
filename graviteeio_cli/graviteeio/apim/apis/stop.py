import click

@click.command()
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.pass_obj
def stop(obj, api_id):
    """This command allow to stop an API"""
    api_client = obj['api_client']
    api_client.stop(api_id)
    click.echo("API {} is stopped".format(api_id))