import click

from graviteeio_cli.graviteeio.config import GraviteeioConfiguration, GraviteeioModule, config


@click.group()
@click.pass_context
def apim(ctx):
    ctx.obj['config'] = GraviteeioConfiguration(module=GraviteeioModule.AM)


apim.add_command(config)