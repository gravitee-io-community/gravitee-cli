import logging

import click
import jmespath
from jmespath import exceptions
from pytimeparse import parse

from graviteeio_cli.extensions.jmespath_functions import \
    GioFunctions
from graviteeio_cli.core.output import OutputFormatType

from ....exeptions import GraviteeioError

logger = logging.getLogger("command-apim-logs")


@click.command(short_help="Get API logs.")
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.option('--line', '-l',
              default=10,
              help='number of line. Default: `10`',
              )
# @click.option('--watch', is_flag=True)
@click.option('--output', '-o',
              default="table",
              help='Set the format for printing command output resources.',
              show_default=True,
              type=click.Choice(
                    OutputFormatType.list_name(),
                    case_sensitive=False)
              )
@click.pass_obj
def logs(obj, api_id, line, output):
    """
    Get API logs
    """
    api_client = obj['api_client']

    (logs, _, to_timestamp) = api_client.logs(api_id, line, time_frame_seconds=parse("1d"))

    query = "[].{Date: datetime(timestamp,'%d-%m-%Y %H:%M:%S %f'), App: application_name, verbe: upper(method), Status: status, Path: path, Latency: responseTime}"

    try:
        logs_filtered = jmespath.search(query, logs['logs'], jmespath.Options(custom_functions=GioFunctions()))

        if logs_filtered and len(logs_filtered) > 0:
            if type(logs_filtered) is list and type(logs_filtered[0]) is dict and len(logs_filtered) > 0:
                header = logs_filtered[0].keys()

            OutputFormatType.value_of(output).echo(logs_filtered, header=header)
        else:
            click.echo("No logs")
    except exceptions.JMESPathError as jmespatherr:
        logging.exception("LIST JMESPathError exception")
        raise GraviteeioError(str(jmespatherr))
