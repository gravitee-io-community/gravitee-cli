import json
import os

import click
from dictdiffer import diff as jsondiff

from .... import environments
from ....exeptions import GraviteeioError
from .api_schema import ApiSchema
from .utils import display_dict_differ, filter_api_values


@click.command()
@click.argument('api_id', required=True, metavar='[API ID]')
@click.option('--file', '-f', required=False,
              help="Values file")
@click.option('--set', '-s', multiple=True,
              help="Overload the value(s) of value file eg: `--set proxy.groups[0].name=mynewtest`")
@click.option('--debug', '-d', is_flag=True,
              help="Do not perform any changes. Show the datas genereted")
@click.option('--diff', '-df', is_flag=True,
              help="Compare the configuration values with api on the server")
@click.argument('templates_folder', type=click.Path(exists=True), required=False, metavar='[PATH FOLDER]')
@click.pass_obj
def update(obj, api_id, file, set, debug, diff, templates_folder):
    """
    Object to update the API are managed with the template engine.
    API values are defined in plain YAML files.

    By default: the values file and template are in the folder `./graviteeio` where the commande is executed
    template file: `apim_api_template.yml.j2`
    value file: `apim_api_value.yml`
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
                value_file = "{}/{}".format(templates_folder, file)
    else:
        value_file = file

    if not value_file:
        raise GraviteeioError("No Value file found")

    api_sch = ApiSchema(templates_folder, value_file)
    api_data = api_sch.get_api_data(debug=debug, set_values=set)

    if debug:
        click.echo("JSON")
        click.echo(json.dumps(api_data))
    elif diff:
        api_server = api_client.get(api_id).json()

        filter_api_values(api_server)

        diff_result = jsondiff(api_server, api_data)
        display_dict_differ(diff_result)
    else:
        if api_id:
            resp = api_client.update(api_id, json.dumps(api_data))
            click.echo("API {} is updated".format(api_id))
        else:
            click.echo("Start Create")
            resp = api_client.create(json.dumps(api_data))
            click.echo("API {} has been created".format(resp.json()["id"]))
