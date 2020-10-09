import click

from graviteeio_cli.http_client.apim.api import ApiClient
from graviteeio_cli.core.output import OutputFormatType


@click.command(short_help="Get page documentation.")
@click.option('--page', '-p', 'page_id',
              help='Page id',
              required=True)
@click.option('--api', 'api_id',
              help='API id',
              required=False)
@click.pass_obj
def get(obj, page_id, api_id):
    """Get page documentation of api or portal."""
    page_client: ApiClient = obj['page_client']

    page_data = page_client.get(page_id, api_id)
    del page_data['order']
    del page_data['lastContributor']
    del page_data['lastModificationDate']
    del page_data['contentType']

    if len(page_data['content']) > 30:
        page_data['content'] = page_data['content'][0:30] + " ..."

    OutputFormatType.TABLE.echo(page_data, header=["Page"])
