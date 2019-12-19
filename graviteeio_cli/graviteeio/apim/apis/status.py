import click
from graviteeio_cli.graviteeio.output import OutputFormat, gio, FormatType

@click.command()
@click.argument('api_id', required=True)
@click.option('--format',
              default="table",
              help='Set the format for printing command output resources. The supported formats are: `table`, `json`, `yaml`, `tsv`. Default is: `table`',
              type=click.Choice(FormatType.list_name(), case_sensitive=False))
@click.pass_obj
def status(obj, format, api_id):
    """This command displays API status"""
    api_client = obj['api_client']
    status_values = api_client.status(api_id).json()['values']

    status_100_200 = status_values['100.0-200.0']
    status_200_300 = status_values['200.0-300.0']
    status_300_400 = status_values['300.0-400.0']
    status_400_500 = status_values['400.0-500.0']
    status_500_600 = status_values['500.0-600.0']

    total = status_100_200 + status_200_300 + status_300_400 + status_400_500 + status_500_600
    if total == 0:
        total = 1

    to_return =[
        {
            "status": "1xx",
            "hits": status_100_200,
            "percent": round((status_100_200 * 100) / total, 2)
        },
        {
            "status": "2xx",
            "hits": status_200_300,
            "percent": round((status_200_300 * 100) / total, 2)
        },
        {
            "status": "3xx",
            "hits": status_300_400,
            "percent": round((status_300_400 * 100) / total, 2)
        },
        {
            "status": "4xx",
            "hits": status_400_500,
            "percent": round((status_400_500 * 100) / total, 2)
        },
        {
            "status": "5xx",
            "hits": status_500_600,
            "percent": round((status_500_600 * 100) / total, 2)
        }
    ]

    outputFormat = OutputFormat.value_of(format)
    gio.echo(to_return, outputFormat, ["Status","Hits", "Percent"])