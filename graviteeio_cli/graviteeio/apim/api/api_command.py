import click, terminaltables, yaml, json, os
#import logging

from click.exceptions import ClickException
from terminaltables import AsciiTable
from .api_resources import apim_api
from .api_data import api
from ....exeptions import GraviteeioRequestError, GraviteeioError
from ...utils import convert_proxy_config, clean_api
from .... import environments
import requests

#logging.basicConfig(level=logging.DEBUG)

@click.group()
@click.pass_context
def apis(ctx):
        ctx.obj = apim_api()

@click.command()
@click.option('--deploy-state', help='show if API configuration is synchronized', is_flag=True)
@click.pass_obj
def ps(apim_api, deploy_state):
        """APIs list"""
        resp =  apim_api.get_apis()
        
        if not resp:
                click.echo("No Api(s) found ")
        else:

                data = []

                if deploy_state:
                        data.append(['id', 'Name', 'Tags', 'Synchronized', 'Status'])
                else:
                        data.append(['id', 'Name', 'Tags', 'Status'])


                for api_item in resp.json():
                        if api_item['state'] == 'started':
                                state_color = 'green'
                        else:
                                state_color = 'red'

                        if 'workflow_state' in api_item:
                                state = click.style(api_item['workflow_state'].upper(), fg='blue')  + "-" + click.style(api_item['state'].upper(), fg=state_color)
                        else:
                                state = click.style(api_item['state'].upper(), fg=state_color)
                        
                        tags = "-"
                        if 'tags' in api_item:
                                tags = ', '.join(api_item['tags'])
                        if not tags:
                                tags = "<none>"

                        if deploy_state:
                                response_state = apim_api.state_api(api_item['id'])
                                synchronized = click.style("X", fg='yellow')
                                if response_state.json()["is_synchronized"]:
                                        synchronized = click.style("V", fg='green')
                                
                                data.append([api_item['id'], api_item['name'], tags, synchronized, state])
                        else:

                                if api_item['state'] == 'started':
                                        color = 'green'
                                else:
                                        color = 'red'
                                data.append([api_item['id'], api_item['name'], tags, state])

                table = AsciiTable(data)
                table.inner_footing_row_border = False
                table.inner_row_border = False
                table.inner_column_border  = False
                table.outer_border = False
                if deploy_state:
                        table.justify_columns[3] = 'center'
                        table.justify_columns[4] = 'right'
                else:
                        table.justify_columns[3] = 'right'
                click.echo(table.table)

@click.command()
@click.argument('api_id', required = True)
@click.pass_obj
def start(apim_api, api_id):
        """start api"""
        resp = apim_api.start_api(api_id)
        click.echo("API {} is started".format(api_id))

@click.command()
@click.argument('api_id', required = True)
@click.pass_obj
def stop(apim_api, api_id):
        """stop api"""
        resp = apim_api.stop_api(api_id)
        click.echo("API {} is stopped".format(api_id))

@click.command()
@click.argument('api_id', required = True)
@click.pass_obj
def deploy(apim_api, api_id):
        """deploy api configuration"""
        resp = apim_api.deploy_api(api_id)
        click.echo("API {} is deployed".format(api_id))

@click.command()
@click.argument('folder', type=click.Path(exists=True), required = False)
@click.pass_obj
def init(apim_api, folder):
        """download init template for api"""
        r = requests.get(environments.APIM_API_URL_GITHUB, stream=True)

        if r.status_code != requests.codes.ok:
                print('Unable to connect {0}'.format(environments.APIM_API_URL_GITHUB))
                r.raise_for_status()
        total_size = int(r.headers.get('Content-Length'))

        if not os.path.exists(environments.GRAVITEEIO_TEMPLATES_FOLDER):
                os.mkdir(environments.GRAVITEEIO_TEMPLATES_FOLDER)

        template_file_path = "{}/{}".format(environments.GRAVITEEIO_TEMPLATES_FOLDER, environments.APIM_API_TEMPLATE_FILE)
        if not os.path.exists(template_file_path):
                click.echo("Init api:")
                with click.progressbar(r.iter_content(1024), length=total_size) as bar, open(template_file_path, 'wb') as file:
                        for chunk in bar:
                                file.write(chunk)
                                bar.update(len(chunk))
        else:
                click.echo("Init file already exists")

@click.command()
@click.argument('api_id', required = True, metavar='[API ID]')
@click.option('--file','-f', required = False , help = "values file")
@click.option('--set','-s',multiple = True, help = "override the value(s) of value file")
@click.option('--debug','-s', is_flag=True, help = "debug mode" )
@click.argument('templates_folder', type=click.Path(exists=True), required = False , metavar='[PATH FOLDER]')
@click.pass_obj
def update(apim_api, api_id, file, set, debug, templates_folder):
        """update api configuration
        
        Values file:
        This object provides access to values passed to the template.
        The value can be sourced from:

        - the values file defined with ``--file``

        - the values file ``apim_api_value.yml`` is passed in PATH FOLDER with the templates

        - individual parameters can be overload with ``--set`` (such as graviteeio apis update 25b75df2-f6bb-4aaf-b75d-f2f6bbdaaf61 --set proxy.groups[0].name=mynewtest)
        
        """
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

        api_obj = api(templates_folder, value_file)
        api_json_data = api_obj.get_api_data(debug= debug, set_values= set)

        if not debug:
                resp = apim_api.update_api(api_id, api_json_data)
                click.echo("API {} is updated".format(api_id))
        else:
                click.echo("JSON")
                click.echo(api_json_data)
        
apis.add_command(ps)
apis.add_command(start)
apis.add_command(stop)
apis.add_command(init)
apis.add_command(deploy)
apis.add_command(update)

