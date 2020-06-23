import logging

import click
import click_completion

from .__version__ import __version__ as VERSION
from .environments import GRAVITEEIO_CONF_FILE
from .graviteeio.apim.apim import apim
from .graviteeio.am.am import am
from .graviteeio.profiles import profiles
from .graviteeio.config import GraviteeioConfig
from graviteeio_cli.graviteeio.modules import GraviteeioModule

# Enable shell completion.
click_completion.init()

# \nEnv: GRAVITEEIO_CONF_FILE'
@click.option(
    '--config', help='Path for configuration file.',
    type=click.Path(), default=GRAVITEEIO_CONF_FILE, show_default=True
)
@click.option('--log', help='Display detailed information.', is_flag=True)
@click.option('--log-level', help='Display detailed information.', default= logging._levelToName[logging.INFO],
type=click.Choice(['CRITICAL','ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'], case_sensitive=False))
#@click.option('--username', help='HTTP Basic Authentication username', type=str)
#@click.option('--password', help='HTTP Basic Authentication password', type=str)
#@click.option('--timeout', help='Connection timeout in seconds.', type=int)
@click.group()
@click.version_option(prog_name=click.style('graviteeio-cli', fg='blue', bold=True), version=VERSION)
@click.pass_context
def main(ctx, config, log, log_level):
        """Graviteeio cli"""
        ctx.obj = {}
        
        log_level = logging._nameToLevel[log_level.upper()]
        if not log:
            logging.disable(logging.ERROR)

        logging.basicConfig(format='%(name)s-%(levelname)s: %(message)s', level=log_level)
        ctx.obj['config'] = GraviteeioConfig(config)
        ctx.obj['path-config'] = config


main.add_command(apim)
main.add_command(am)
main.add_command(profiles)

if __name__ == '__main__':
    main()
