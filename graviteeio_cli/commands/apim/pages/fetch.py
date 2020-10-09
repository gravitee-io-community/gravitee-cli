import click

from graviteeio_cli.http_client.apim.api import ApiClient


@click.command(short_help="Fetch documentation.")
@click.option('--page', '-p', 'page_id',
              help='Page id',
              required=False)
@click.option('--api', 'api_id',
              help='API id',
              required=False)
@click.pass_obj
def fetch(obj, doc_id, api_id):
    """Fetch documentation of api or portal."""
    page_client: ApiClient = obj['page_client']
    response = page_client.fetch(api_id, doc_id)

    if api_id and doc_id:
        click.echo("Page [{}] for API [{}] is uptodate.".format(response.name, api_id))
    elif doc_id:
        click.echo("Page [{}] for portal is uptodate.".format(response.name))
    elif api_id:
        click.echo("All pages for API [{}] are uptodate.".format(api_id))
    else:
        click.echo("All pages for portal are uptodate.")
