import click

from graviteeio_cli.modules.gio_module import GioModule


@click.command()
@click.argument('user', required=True)
@click.pass_obj
def load(obj, user):
    """
    Load current profile
    """
    config = obj['config'].getGraviteeioConfig(GioModule.APIM)
    # auth_list = config.get_auth_list()

    old_username = config.get_active_auth()["username"]
    config.load_auth(user)

    click.echo("Switch authentication from [{}] to [{}].".format(old_username, user))
