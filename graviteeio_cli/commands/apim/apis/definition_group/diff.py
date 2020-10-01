import os

import click
from dictdiffer import diff as jsondiff

from graviteeio_cli.http_client.apim.api import ApiClient

from graviteeio_cli.exeptions import GraviteeioError
from ..utils import display_dict_differ, filter_api_values
from graviteeio_cli.resolvers.api_conf_resolver import ApiConfigResolver


@click.command(short_help="Compare local with remote api definition.")
@click.option(
    '--api', 'api_id',
    help='API id',
    required=True
)
@click.option(
    '--file', '-f',
    type=click.Path(exists=True), required=False,
    help="Value file"
)
@click.option(
    '--set', '-s', multiple=True,
    help="Overload the value(s) of value file eg: `--set proxy.groups[0].name=mynewtest`"
)
@click.option(
    '--def-path', 'config_path',
    type=click.Path(exists=True),
    required=False, default="/",
    help="Config folder"
)
@click.pass_obj
def diff(obj, api_id, file, set, config_path):
    """
    This commande compare the api definition configuration developed on local machine with the configuration on the remote server.
    """
    api_client: ApiClient = obj['api_client']

    if not config_path:
        config_path = "./"

    if not os.path.exists(config_path):
        raise GraviteeioError("No resources folder {} found.".format(config_path))

    api_resolver = ApiConfigResolver(config_path, file)
    api_data = api_resolver.get_api_data(set_values=set)

    api_server = api_client.get_export(api_id, filter_api_values)

    diff_result = jsondiff(api_server, api_data)
    display_dict_differ(diff_result)
