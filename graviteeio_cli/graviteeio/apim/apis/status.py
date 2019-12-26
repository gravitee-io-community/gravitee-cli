import click
import time
import jmespath
from graviteeio_cli.graviteeio.output import OutputFormat, gio, FormatType
from ....exeptions import GraviteeioError

colors = {"1xx":"white","2xx":"green","3xx":"white","4xx":"yellow","5xx":"red"}

@click.command()
@click.argument('api_id', required=True)
@click.option('--format',
              default="table",
              help='Set the format for printing command output resources. The supported formats are: `table`, `json`, `yaml`, `tsv`. Default is: `table`',
              type=click.Choice(FormatType.list_name(), case_sensitive=False))
@click.option('--query',
              default="[].{Status: status, Hits: hits, Percent: percent}",
              help='Execute JMESPath query. eg: filtered on 5xx status `[?status==`5xx`].{Status: status, Hits: hits, Percent: percent}`' )
@click.pass_obj
def status(obj, format, query, api_id):
    """
This command displays API status

\b
Status Field:
- `status`: string 
- `hits`: numerate
- `percent`: string
    """
    api_client = obj['api_client']
    status_values = api_client.status(api_id).json()['values']

    to_return = []
    total = 0
    for key,value in status_values.items():
        status_str = "{}xx".format(key[0:1])
        color = colors[status_str]
        to_return.append(
            {
                "status": status_str,
                "hits": value,
                "percent": value * 100,
            }
        )
        total += value
    # style()
    if total > 0:
        for status in to_return:
            status["percent"] = round(status["percent"] / total, 2)
 
    # start_time = time.time()
    try:
        status_filtered = jmespath.search(query, to_return)
    
        if len(to_return) > 0:
            header = status_filtered[0].keys()
            
        outputFormat = OutputFormat.value_of(format)
        gio.echo(status_filtered, outputFormat, header)

    except Exception as err:
        raise GraviteeioError(err.msg)

    # outputFormat = OutputFormat.value_of(format)
    # gio.echo(to_return, outputFormat, ["","",""])
    # print("Temps d execution : %s secondes ---" % (time.time() - start_time))

def style(value, format, color):
    if format is 'table':
        return click.style("{}".format(value), fg=color)
    else:
        return value