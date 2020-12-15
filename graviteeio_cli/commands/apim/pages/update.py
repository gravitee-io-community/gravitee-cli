import click
import os
import logging
import requests

from graviteeio_cli.http_client.apim.page import PageClient
from graviteeio_cli.exeptions import GraviteeioError

logger = logging.getLogger("command-pages-update")

@click.command(short_help="Update content for page documentation.")
@click.option('--page', '-p', 'page_id',
              help='Page id',
              required=True)
@click.option('--api', 'api_id',
              help='API id',
              required=False)
@click.option('--file', '-f', required=True,
              help="Document file. It can be a PATH or URL")
@click.pass_obj
def update_content(obj, page_id, api_id, file):
    """Update content for page documentation."""
    page_content = None

    if file.startswith("http://") or file.startswith("https://"):
        try:
            page_content = requests.get(file).text
        except Exception:
            raise GraviteeioError(f'Invalid value for "--file" / "-f": Call error for URL "{file}".')

    else:
        if os.path.exists(file):
            with open(file, "r") as reader:
                page_content = reader.read()
        else:
            raise GraviteeioError(f'Invalid value for "--file" / "-f": Path "{file}" does not exist.')

    page_client: PageClient = obj['page_client']
    page_client.update_content(page_id, api_id, page_content)

    if api_id:
        click.echo(f"API [{api_id}] Documentation is uptodate.")
    else:
        click.echo("Documentation is uptodate.")
