import logging

import click
import jmespath
from jmespath import exceptions
from graviteeio_cli.http_client.apim.app import AppClient

from graviteeio_cli.core.output import OutputFormatType

from ....exeptions import GraviteeioError

logger = logging.getLogger("command-apim-app-list")


@click.command(short_help="Displays API list.")
@click.option(
    '--output', '-o',
    default="table",
    help='Set the format for printing command output resources.',
    show_default=True,
    type=click.Choice(OutputFormatType.list_name(), case_sensitive=False)
)
# @click.option(
#     '-q', '--query',
#     help='Execute JMESPath query. Some function styles are available for the output format `table`. `style_synchronized()` for value `is_synchronized`, `style_state()` for value `state`, `style_workflow_state()` for value `workflow_state`. This function allows to add color according to the value.',
#     default="[]"
# )
@click.pass_obj
def ls(obj, output):
    """
This command lists all Application available on Api management platform.

Default query with output `table`: `[].{Id: id, Name: name, Tags: style_tags(tags), Synchronized: style_synchronized(is_synchronized), Status: style_state(state), Workflow: style_workflow_state(workflow_state)}`
    """

    app_client: AppClient = obj['app_client']
    apps = app_client.get()
    outputFormatType = OutputFormatType.value_of(output)

    if outputFormatType.TABLE == outputFormatType:
        query = "[].{Id: id, Name: name, Type: type, Owner: owner.displayName}"

    try:
        apps_filtered = jmespath.search(query, apps)

        logging.debug("apps_filtered: {}".format(apps_filtered))
        if not apps_filtered:
            click.echo("No result")
            return

        header = None
        if type(apps_filtered) is list and type(apps_filtered[0]) is dict and len(apps_filtered) > 0:
            header = apps_filtered[0].keys()

        outputFormatType.echo(apps_filtered, header=header)

    except exceptions.JMESPathError as jmespatherr:
        logging.exception("LIST JMESPathError exception")
        raise GraviteeioError(str(jmespatherr))
