import asyncio
import logging

import click
import jmespath
from jmespath import exceptions, functions

from graviteeio_cli.http_client.apim.api_async import ApiClientAsync
from graviteeio_cli.core.output import OutputFormatType
from graviteeio_cli.extensions.jmespath_functions import GioFunctions

from ....exeptions import GraviteeioError

logger = logging.getLogger("command-apim-list")


@click.command(short_help="Displays API list.")
@click.option(
    '--output', '-o',
    default="table",
    help='Set the format for printing command output resources.',
    show_default=True,
    type=click.Choice(OutputFormatType.list_name(), case_sensitive=False)
)
@click.option(
    '-q', '--query',
    help='Execute JMESPath query. Some function styles are available for the output format `table`. `style_synchronized()` for value `is_synchronized`, `style_state()` for value `state`, `style_workflow_state()` for value `workflow_state`. This function allows to add color according to the value.',
    default="[]"
)
@click.pass_obj
def ls(obj, output, query):
    """
This command lists all API available on Api management platform.

Default query with output `table`: `[].{Id: id, Name: name, Tags: style_tags(tags), Synchronized: style_synchronized(is_synchronized), Status: style_state(state), Workflow: style_workflow_state(workflow_state)}`
    """

    async def get_apis():
        client = ApiClientAsync(obj['config'])
        apis = await client.get_apis_with_state()
        return apis

    loop = asyncio.get_event_loop()
    apis = loop.run_until_complete(get_apis())

    logger.debug("apis response: {}".format(apis))

    if not apis and len(apis) <= 0:
        click.echo("No Api(s) found ")

    outputFormatType = OutputFormatType.value_of(output)
    if query == "[]":
        if outputFormatType.TABLE == outputFormatType:
            query = "[].{Id: id, Name: name, Tags: style_tags(tags), Synchronized: style_synchronized(is_synchronized), Status: style_state(state), Workflow: style_workflow_state(workflow_state)}"

    class CustomFunctions(GioFunctions):

        @functions.signature({'types': ['string']})
        def _func_style_state(self, state):
            state_color = 'red'
            if state == 'started':
                state_color = 'green'
            return click.style(state.upper(), fg=state_color)

        @functions.signature({'types': []})
        def _func_style_workflow_state(self, workflow_state):
            if workflow_state:
                return click.style(workflow_state.upper(), fg='blue')
            else:
                return '-'

        @functions.signature({'types': []})
        def _func_style_tags(self, tags):
            if tags:
                return ', '.join(tags)
            else:
                return "<none>"

        @functions.signature({'types': []})
        def _func_style_synchronized(self, state):
            if state:
                return click.style("V", fg='green')
            else:
                return click.style("X", fg='yellow')

    try:
        apis_filtered = jmespath.search(query, apis, jmespath.Options(custom_functions=CustomFunctions()))
        header = None

        logging.debug("apis_filtered: {}".format(apis_filtered))
        if not apis_filtered:
            click.echo("No result")
            return

        if type(apis_filtered) is list and type(apis_filtered[0]) is dict and len(apis_filtered) > 0:
            header = apis_filtered[0].keys()

        logging.debug("apis_filtered header: {}".format(header))

        justify_columns = {}
        if output == 'table' and header is not None:
            # TODO: Dynamic table style
            for x in range(2, len(header)):
                justify_columns[x] = 'center'
            # justify_columns = {3: 'center', 4: 'center', 5: 'center'}
            # outputFormat.style = justify_columns

        outputFormatType.echo(apis_filtered, header=header, style=justify_columns)

    except exceptions.JMESPathError as jmespatherr:
        logging.exception("LIST JMESPathError exception")
        raise GraviteeioError(str(jmespatherr))
    except Exception:
        logging.exception("LIST Exception")
        raise GraviteeioError("apis filtered {} and the query {}".format(apis_filtered, query))
