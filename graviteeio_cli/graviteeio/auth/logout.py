import click

from graviteeio_cli.graviteeio.modules import GraviteeioModule
from graviteeio_cli.graviteeio.config import GraviteeioConfig_apim, Auth_Type

@click.command()
@click.pass_obj
def logout(obj):
    """
    Logout.
    """

    config : GraviteeioConfig_apim = obj['config'].getGraviteeioConfig(obj['module'])

    if config.is_logged_in:
        authn_name = config.get_authn_name()
        auth_client = obj['auth_client']
        bearer = auth_client.logout()

        config.remove_active_auth()
        click.echo("[{}] is now logged out.".format(authn_name))
    else :
        click.echo("No Authentication [{}] found.".format(Auth_Type.CREDENTIAL.name.lower()))