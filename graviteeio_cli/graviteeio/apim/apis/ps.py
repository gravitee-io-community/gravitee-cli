import click
import jmespath
import asyncio
import aiohttp
from jmespath import functions
from graviteeio_cli.graviteeio.output import OutputFormat, gio, FormatType
from terminaltables import AsciiTable
from graviteeio_cli.graviteeio.apim.client.api_async import ApiClientAsync
from ....exeptions import GraviteeioError


@click.command()
#@click.option('--deploy-state', help='show if API configuration is synchronized', is_flag=True)
@click.option('--format',
              default="table",
              help='Set the format for printing command output resources. The supported formats are: `table`, `json`, `yaml`, `tsv`. Default is: `table`',
              type=click.Choice(FormatType.list_name(), case_sensitive=False))
@click.option('--query',
               help='Execute JMESPath query. Some function styles are available for the format `table. `style_synchronized()` for value `is_synchronized`, `style_state()` for value `state`, `style_workflow_state()` for value `workflow_state`' )
@click.pass_obj
def ps(obj, format, query):
    """
This command displays the list of APIs

API Field:

- `id`: string 

- `name`: string

- `version`: string

- `description`: string

- `visibility`: enum `public`, `private``

- `state`: enum `initialized`, `stopped`, `started`, `closed`

- `labels`: string array

- `manageable`: boolean

- `numberOfRatings`: num

- `tags:string array

- `created_at`: unix time

- `updated_at:` unix time

- `owner`:

    - `id`: string

    - `displayName`: string

- `picture_url`: string url

- `virtual_hosts`: array
    - `host`: string

    - `path`: string

    - `overrideEntrypoint`: boolean

- `lifecycle_state`: enum `created`, `published`, unpublished`, `deprecated`, archived`

- `workflow_state`: enum `draft`, ìn_review`, `request_for_changes`, `review_ok`

- `is_synchronized`: boolean
    
    """

    resp = 'test'
    if not resp:
        click.echo("No Api(s) found ")
    else:

        async def get_apis():
            client =  ApiClientAsync(obj['config'])
            apis = await client.get_apis_with_state()
            return apis
            
        apis = asyncio.run(get_apis())

        if not query:
            if FormatType.table == FormatType.value_of(format):
                query="[].{Id: id, Name: name, Tags: style_tags(tags), Synchronized: style_synchronized(is_synchronized), Status: style_state(state), Workflow: style_workflow_state(workflow_state)}"
            else:
                query="[].{Id: id, Name: name, Tags: tags, Synchronized: is_synchronized, Status: state, Workflow: workflow_state}"
           
        class CustomFunctions(functions.Functions):
        #options= jmespath.Options()
            @functions.signature({'types': ['string']})
            def _func_style_state(self, state):
                state_color = 'red';
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
        
            if len(apis) > 0:
                header = apis_filtered[0].keys()

            # print("{}".format(apis))
            
            # TODO: Dynamic table style
            justify_columns = {3: 'center', 4: 'center', 5: 'center'}
                
            outputFormat = OutputFormat.value_of(format)
            outputFormat.style = justify_columns
            #print("{}".format(apis_filtered))
            gio.echo(apis_filtered, outputFormat, header)
        except Exception as err:
            raise GraviteeioError(err.msg)

        
