import click, yaml, json, os, time

from dictdiffer import diff as jsondiff

from click.exceptions import ClickException
from ..client.api import api_client
from .api_schema import api_schema
from ....exeptions import GraviteeioRequestError, GraviteeioError
from .... import environments
from .utils import display_dictdiffer, filter_api_values

@click.command()
@click.argument('api_id', required = True, metavar='[API ID]')
@click.option('--file','-f', required = False , 
                help = "Path to values file.")
@click.option('--set','-s',multiple = True, 
                help = "overload the value(s) of value file")
@click.option('--debug','-d', is_flag=True, 
                help = "Do not perform any changes. Show the datas genereted" )
@click.option('--diff','-df', is_flag=True, 
                help = "Compare the configuration values with api on the server" )
@click.argument('templates_folder', type=click.Path(exists=True), required = False , metavar='[PATH FOLDER]')
@click.pass_obj
def update(obj, api_id, file, set, debug, diff, templates_folder):
        """update api configuration
        
        Values file:
        This object provides access to values passed to the template.
        The value can be sourced from:

        - the values file defined with ``--file``

        - the values file ``apim_api_value.yml`` is passed in PATH FOLDER with the templates

        - individual parameters can be overload with ``--set`` (such as graviteeio apis update 25b75df2-f6bb-4aaf-b75d-f2f6bbdaaf61 --set proxy.groups[0].name=mynewtest)
        
        """
        api_client = obj['api_client']
        value_file = None
        
        if not templates_folder:
                templates_folder = "./{}".format(environments.GRAVITEEIO_TEMPLATES_FOLDER)

        if not file:
                if not os.path.exists(templates_folder):
                        raise GraviteeioError("Not folder {} found".format(templates_folder))
                for files_list in os.listdir(templates_folder):
                        if files_list == environments.APIM_API_VALUE_FILE_NAME:
                                value_file = "{}/{}".format(templates_folder,file)
        else:
                value_file = file
        
        if not value_file:
                raise GraviteeioError("No Value file found")

        api_sch = api_schema(templates_folder, value_file)
        api_data = api_sch.get_api_data(debug= debug, set_values= set)

        if debug:
                click.echo("JSON")
                click.echo(json.dumps(api_data))
        elif diff:
                api_server = api_client.get_api(api_id).json()
                
                filter_api_values(api_server)
                
                diff_result = jsondiff(api_server, api_data)
                display_dictdiffer(diff_result)
        else:
                resp = api_client.update_api(api_id, json.dumps(api_data))
                click.echo("API {} is updated".format(api_id))