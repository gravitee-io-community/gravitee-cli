import logging
import os

import click

from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.commands.auth.logout import logout
from graviteeio_cli.core.config import Auth_Type, GraviteeioConfig_apim

logger = logging.getLogger("command-auth-token")


def get_token(ctx, param, value):
    if not value and click.get_text_stream('stdin').isatty():
        return click.prompt('Personal access token')
    elif value.startswith("env:"):
        env_value = os.environ.get(value[4:])
        if not env_value:
            click.echo('No environement value found for [{}].'.format(value[4:]))
            return click.prompt('Personal access token')
        # else:
        #     return env_value

    return value


@click.command(short_help="sign in with token")
@click.argument('token', callback=get_token, required=False)
@click.option('--name', help="token name", required=False)
@click.pass_context
def token(ctx, token, name):
    """
    Sign in with personal access token

    if token start with `env:` the token will retrieve from environment variable. i.e: `env:TOKEN`.
    """
    config: GraviteeioConfig_apim = ctx.obj['config'].getGraviteeioConfig(ctx.obj['module'])
    auth_client = ctx.obj['auth_client']

    if not click.get_text_stream('stdin').isatty():
        token = click.get_text_stream('stdin').read().strip()

    if not name:
        name = "-"
    # print(token)
    try:
        if config.is_logged_in():
            ctx.invoke(logout)
    except Exception:
        logger.exception("invoke logout")

    config.save_active_auth(name, Auth_Type.PERSONAL_ACCESS_TOKEN, token)

    try:
        auth_client.tokens()
        click.echo("You are now logged with your personal token [{}].".format(name))
        click.echo("Your current profile is [{}]".format(ctx.obj['config'].profile))
    except Exception:
        config.remove_active_auth()
        raise GraviteeioError("No valid token.")
