import json
import os

import click
from dictdiffer import diff as jsondiff

from graviteeio_cli.graviteeio.client.apim.api import ApiClient

from ..... import environments
from .....exeptions import GraviteeioError
from ..utils import display_dict_differ, filter_api_values
from .api_schema import ApiSchema


@click.command(short_help="Compare local and remote api definition.")
@click.option('--api', 'api_id',
              help='API id',
              required=True)
@click.option('--file', '-f', type=click.Path(exists=True), required=False,
              help="Value file")
@click.option('--set', '-s', multiple=True,
              help="Overload the value(s) of value file eg: `--set proxy.groups[0].name=mynewtest`")
@click.option('--diff', '-df', is_flag=True,
              help="Compare the configuration values with api on the server")
@click.option('--config-path', type=click.Path(exists=True), required=False, default="./",
              help="Config folder")
@click.pass_obj
def diff(obj, api_id, file, set, diff, config_path):
    """
    This commande compare the api definition developed on local machine with api configured on the remote server.
    """
    api_client : ApiClient = obj['api_client']

    if not config_path:
        config_path = "./"

    if not os.path.exists(config_path):
        raise GraviteeioError("No resources folder {} found.".format(config_path))

    api_sch = ApiSchema(config_path, file)
    api_data = api_sch.get_api_data(set_values=set)

    api_server = api_client.get_export(api_id, filter_api_values)

    diff_result = jsondiff(api_server, api_data)
    display_dict_differ(diff_result)
