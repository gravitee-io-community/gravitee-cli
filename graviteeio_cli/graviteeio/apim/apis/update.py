import click
import json
import os
from dictdiffer import diff as jsondiff

from .api_schema import ApiSchema
from .utils import display_dict_differ, filter_api_values
from .... import environments
from ....exeptions import GraviteeioError


@click.command()
@click.argument('api_id', required=True, metavar='[API ID]')
@click.option('--file', '-f', required=False,
              help="Path to values file.")
@click.option('--set', '-s', multiple=True,
              help="overload the value(s) of value file")
@click.option('--debug', '-d', is_flag=True,
              help="Do not perform any changes. Show the datas genereted")
@click.option('--diff', '-df', is_flag=True,
              help="Compare the configuration values with api on the server")
@click.argument('templates_folder', type=click.Path(exists=True), required=False, metavar='[PATH FOLDER]')
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
        api_server = api_client.get_api(api_id).json()

        filter_api_values(api_server)

        diff_result = jsondiff(api_server, api_data)
        display_dict_differ(diff_result)
    else:
        if api_id:
            resp = api_client.update_api(api_id, json.dumps(api_data))
            click.echo("API {} is updated".format(api_id))
        else:
            click.echo("Start Create")
            resp = api_client.create_api(json.dumps(api_data))
            click.echo("API {} has been created".format(resp.json()["id"]))


@click.command()
@click.option('--file', '-f', required=False,
              help="Path to values file.")
@click.option('--set', '-s', multiple=True,
              help="overload the value(s) of value file")
@click.option('--debug', '-d', is_flag=True,
              help="Do not perform any changes. Show the datas genereted")
@click.argument('templates_folder', type=click.Path(exists=True), required=False, metavar='[PATH FOLDER]')
@click.pass_context
def create(ctx, file, set, debug, templates_folder):
    ctx.invoke(update, api_id=None, file=file, set=set, debug=debug, diff=False, templates_folder=templates_folder)

# curl 'https://demo.gravitee.io/management/apis/import' -H 'sec-fetch-mode: cors' -H 'origin: https://demo.gravitee.io' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7' -H 'x-requested-with: XMLHttpRequest' -H 'cookie: _ga=GA1.2.1715653817.1508833929; Auth-Graviteeio-APIM=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxODI2YTZjNS1iMmU2LTQ0NDEtYTZhNi1jNWIyZTY2NDQxMWEiLCJmaXJzdG5hbWUiOm51bGwsInBlcm1pc3Npb25zIjpbeyJhdXRob3JpdHkiOiJQT1JUQUw6QURNSU4ifSx7ImF1dGhvcml0eSI6Ik1BTkFHRU1FTlQ6QURNSU4ifV0sImlzcyI6ImdyYXZpdGVlLW1hbmFnZW1lbnQtYXV0aCIsImV4cCI6MTU3MjQyNTI3MCwiaWF0IjoxNTcxODIwNDcwLCJlbWFpbCI6bnVsbCwianRpIjoiYmEzNDhmYTItM2ZhNy00YTI5LWIzNjUtMzk0NWMwNDM4ODRkIiwibGFzdG5hbWUiOm51bGx9.KkHgjEe-2_or3MpzyiMOyHnXCaBzYbC0bU-v7P6wWgQ' -H 'pragma: no-cache' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36' -H 'content-type: application/json;charset=UTF-8' -H 'accept: application/json, text/plain, */*' -H 'cache-control: no-cache' -H 'authority: demo.gravitee.io' -H 'referer: https://demo.gravitee.io/' -H 'sec-fetch-site: same-origin' --data-binary '{"proxy":{"endpoints":[{"name":"default","target":"http://test.com","inherit":true}],"context_path":"/testest"},"pages":[],"plans":[],"tags":[],"name":"test","version":"1.0","description":"tesf"}' --compressed
