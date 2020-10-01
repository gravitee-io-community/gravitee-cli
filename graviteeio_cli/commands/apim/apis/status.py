import logging

import click
import jmespath
from jmespath import exceptions
from pytimeparse import parse

from graviteeio_cli.http_client.apim.api import ApiClient
from graviteeio_cli.extensions.jmespath_functions import \
    GioFunctions
from graviteeio_cli.core.output import OutputFormatType

from ....exeptions import GraviteeioError

colors = {"1xx": "white", "2xx": "green", "3xx": "white", "4xx": "yellow", "5xx": "red"}


@click.command()
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.option('--output', '-o',
              default="table",
              help='Set the format for printing command output resources.',
              show_default=True,
              type=click.Choice(
                  OutputFormatType.extended_list_name(), case_sensitive=False)
              )
@click.option('-q', '--query',
              default="reverse(@)[].{Status: status, Hits: hits, Percent: percent}",
              help='Execute JMESPath query. Default: `reverse(@)[].{Status: status, Hits: hits, Percent: percent}` eg: filtered on 5xx status `[?status==`5xx`].{Status: status, Hits: hits, Percent: percent}`')
@click.option('-tf', '--time-frame',
              default="5m",
              help="Timeframe between now and the vale. m -> minute, h -> hour, d -> days", show_default=True)
@click.pass_obj
def status(obj, output, query, time_frame, api_id):
    """
Displays status of API.

\b
Status Field:
- `status`: string
- `hits`: numerate
- `percent`: string
    """
    api_client: ApiClient = obj['api_client']

    try:
        status_values = api_client.status(api_id, parse(time_frame))['values']
    except TypeError:
        raise GraviteeioError("Unsupported type for time frame")

    to_return = []
    total = 0
    for key, value in status_values.items():
        status_str = "{}xx".format(key[0:1])
        to_return.append(
            {
                "status": status_str,
                "hits": value,
                "percent": value * 100
            }
        )
        total += value

    if total > 0:
        for status in to_return:
            status["percent"] = round(status["percent"] / total, 2)

    if format == "hbar":
        query = "reverse(@)[].{Status: status, Percent: percent}"
    # start_time = time.time()
    try:
        status_filtered = jmespath.search(query, to_return, jmespath.Options(custom_functions=GioFunctions()))

        header = None
        if len(status_filtered) > 0 and type(status_filtered[0]) is dict:
            header = status_filtered[0].keys()

        OutputFormatType.value_of(output).echo(status_filtered, header=header)

    except exceptions.JMESPathError as jmespatherr:
        logging.exception("STATUS JMESPathError exception")
        raise GraviteeioError(str(jmespatherr))
    except Exception:
        logging.exception("STATUS Exception")
        raise GraviteeioError("to print {} with the format {}.".format(status_filtered, format))
