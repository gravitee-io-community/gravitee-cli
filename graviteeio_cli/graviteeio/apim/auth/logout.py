import click

from graviteeio_cli.graviteeio.modules import GraviteeioModule

@click.command()
@click.pass_obj
def logout(obj):

    config = obj['config'].getGraviteeioConfig(GraviteeioModule.APIM)
    auth = config.get_active_auth()
    auth_client = obj['auth_client']
    bearer = auth_client.logout()

    config.save(bearer = None)

    click.echo("You are now logged out.")