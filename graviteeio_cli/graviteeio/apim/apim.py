import click

from graviteeio_cli.graviteeio.config import GraviteeioConfiguration, GraviteeioModule, config
from .apis.apis import apis


@click.group()
@click.pass_context
def apim(ctx):
    ctx.obj['config'] = GraviteeioConfiguration(module=GraviteeioModule.APIM)


apim.add_command(apis)
apim.add_command(config)
