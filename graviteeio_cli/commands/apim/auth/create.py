import click

from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.modules.gio_module import GioModule
from graviteeio_cli.core.config import Auth_Type, GraviteeioConfig_apim


@click.command()
@click.option('--user', help='authentication user', required=True)
@click.option(
    '--type', 'auth_type',
    help='authentication type', default="credential",
    show_default=True,
    type=click.Choice(Auth_Type.list_name(), case_sensitive=False)
)
@click.pass_obj
def create(obj, user, auth_type):
    """Create a new authentication user"""
    config: GraviteeioConfig_apim = obj['config'].getGraviteeioConfig(GioModule.APIM)
    auth_list = config.get_auth_list()

    for auth in auth_list:
        if auth["username"] == user and auth_type.upper() == auth["type"].upper():
            raise GraviteeioError("Username [{}] already exit for authentication type {}.".format(user, auth_type))

    auth_list.append({
        "username": user,
        "type": auth_type,
        "is_active": False
    })

    config.save(auth=auth_list)

    click.echo("User [{}] saved.".format(user))
