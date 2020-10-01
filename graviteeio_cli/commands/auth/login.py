import click
import logging

from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.commands.auth.logout import logout
from graviteeio_cli.core.config import Auth_Type, GraviteeioConfig_apim

logger = logging.getLogger("command-auth-login")


def get_username(ctx, param, value):
    if not value and click.get_text_stream('stdin').isatty():
        return click.prompt('Username')

    return value


def get_password(ctx, param, value):
    if not value and click.get_text_stream('stdin').isatty():
        return click.prompt('Password', hide_input=True)

    return value


@click.command(short_help="sign in with username/password")
@click.option('--username', help="username for login", callback=get_username)
@click.option('--password', help="password for login", callback=get_password)
@click.pass_context
def login(ctx, username, password):
    """
    Sign in with username/password
    """
    config: GraviteeioConfig_apim = ctx.obj['config'].getGraviteeioConfig(ctx.obj['module'])
    auth_client = ctx.obj['auth_client']

    if not click.get_text_stream('stdin').isatty():
        stdin_stream = click.get_text_stream('stdin').read().strip()

        if not username and not password:
            username_pwd = stdin_stream.split(":")
            if len(username_pwd) < 2:
                raise GraviteeioError("No username or password found. username and password have to split with ':' character")
            else:
                username = username_pwd[0]
                password = username_pwd[1]
        else:
            password = stdin_stream

    bearer = auth_client.login(username, password)

    try:
        if config.is_logged_in():
            ctx.invoke(logout)
    except Exception:
        logger.exception("invoke logout")

    config.save_active_auth(username, Auth_Type.CREDENTIAL, bearer)

    click.echo("You are now logged in as [{}].".format(username))
    click.echo("Your current profile is [{}]".format(ctx.obj['config'].profile))
