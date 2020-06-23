import click

from graviteeio_cli.graviteeio.modules import GraviteeioModule
from graviteeio_cli.graviteeio.config import GraviteeioConfig_apim

@click.command()
@click.pass_obj
def logout(obj):
    """
    Logout.
    """

    config : GraviteeioConfig_apim = obj['config'].getGraviteeioConfig(obj['module'])
    auth = config.get_active_auth()
    auth_client = obj['auth_client']
    bearer = auth_client.logout()

    config.remove_active_auth()

    click.echo("[{}] is now logged out.".format(auth["username"]))