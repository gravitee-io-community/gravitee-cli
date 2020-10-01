import logging

import click
import jmespath
from jmespath import exceptions

from graviteeio_cli.http_client.apim.api import ApiClient
from graviteeio_cli.extensions.jmespath_functions import \
    GioFunctions
from graviteeio_cli.core.output import OutputFormatType

from ....exeptions import GraviteeioError


@click.command(short_help="API health.")
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.option('--output', '-o',
              default="table",
              help='Set the format for printing command output resources.',
              show_default=True,
              type=click.Choice(OutputFormatType.list_name(), case_sensitive=False))
@click.option('-q', '--query',
              default="[].{Time: time, Percent: percent}",
              help='Execute JMESPath query. Default: `[].{Time: time, Percent: percent}` eg: filtered on 5xx status `[?status==`5xx`].{Status: status, Hits: hits, Percent: percent}`')
# @click.option('-tf','--time-frame',
#               default="5m",
#               help="timeframe between now and the vale. Default: `5m`. m -> minute, h -> hour, d -> days")
@click.pass_obj
def health(obj, output, query, api_id):
    """API health: return the lastest availability: minute, hour, day, week, month"""
    api_client: ApiClient = obj['api_client']

    health_values = None
    # health = api_client.health(api_id, time_frame_seconds = parse(time_frame))
    health = api_client.health(api_id)
    if 'global' in health:
        health_values = health['global']
    else:
        click.echo("No health data")
        return

    to_return = []
    for key, value in health_values.items():
        to_return.append(
            {
                "time": key,
                "percent": round(value, 2)
            }
        )

    try:
        health_filtered = jmespath.search(query, to_return, jmespath.Options(custom_functions=GioFunctions()))

        header = None
        if len(health_filtered) > 0 and type(health_filtered[0]) is dict:
            header = health_filtered[0].keys()

        outputFormat = OutputFormatType.value_of(output)
        outputFormat.echo(health_filtered, header=header)
    except exceptions.JMESPathError as jmespatherr:
        logging.exception("HEALTH JMESPathError exception")
        raise GraviteeioError(str(jmespatherr))
    except Exception:
        logging.exception("HEALTH Exception")
        raise GraviteeioError("to print {} with the format {}.".format(health_filtered, format))
