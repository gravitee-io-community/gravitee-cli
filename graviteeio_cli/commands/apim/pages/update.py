import click

from graviteeio_cli.http_client.apim.api import ApiClient


@click.command(short_help="Update content for page documentation.")
@click.option('--page', '-p', 'page_id',
              help='Page id',
              required=True)
@click.option('--api', 'api_id',
              help='API id',
              required=False)
@click.option('--file', '-f', type=click.Path(exists=True), required=True,
              help="Document file")
@click.pass_obj
def update_content(obj, page, api_id, file):
    """Update content for page documentation."""
    page_client: ApiClient = obj['page_client']
    print(page_client.get(page, api_id))

    page_client.update(page, api_id)

    click.echo("API [{}] Documentation is uptodate.".format(api_id))
