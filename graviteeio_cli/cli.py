from .__version__ import __version__ as VERSION
import click, click_completion

from .graviteeio.config import config
from .graviteeio.apim.api.api_command import apis


# Enable shell completion.
click_completion.init()

@click.group()
@click.version_option(prog_name=click.style('graviteeio-cli', fg='blue', bold=True), version=VERSION)
def main():
        """Graviteeio cli"""
        pass

main.add_command(config)
main.add_command(apis)

if __name__ == '__main__':
    main()