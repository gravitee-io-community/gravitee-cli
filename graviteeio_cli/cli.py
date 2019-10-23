from .__version__ import __version__ as VERSION
from .environments import GRAVITEEIO_CONF_FILE
import click, click_completion

from .graviteeio.config import config, Graviteeio_configuration
from .graviteeio.apim.apis.api_commands import apis


# Enable shell completion.
click_completion.init()

@click.option(
    '--config', help='Path to configuration file. Default: ' + GRAVITEEIO_CONF_FILE,
    type=click.Path(), default=GRAVITEEIO_CONF_FILE
)
@click.option('--username', help='HTTP Basic Authentication username', type=str)
@click.option('--password', help='HTTP Basic Authentication password', type=str)
@click.option('--timeout', help='Connection timeout in seconds.', type=int)
@click.group()
@click.version_option(prog_name=click.style('graviteeio-cli', fg='blue', bold=True), version=VERSION)
@click.pass_context
def main(ctx, config, username, password, timeout):
        """Graviteeio cli"""
        ctx.obj = {}
        ctx.obj['config'] = Graviteeio_configuration(config)

main.add_command(config)
main.add_command(apis)

if __name__ == '__main__':
    main()