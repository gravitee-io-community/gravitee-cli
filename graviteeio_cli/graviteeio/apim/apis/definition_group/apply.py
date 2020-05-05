import json
import os

import click
from dictdiffer import diff as jsondiff

from ..... import environments
from .....exeptions import GraviteeioError
from .api_schema import ApiSchema
from ..utils import display_dict_differ, filter_api_values
from ..deploy import deploy
from ..start import start


@click.command()
@click.argument('api_id', required=True, metavar='[API ID]')
@click.option('--file', '-f', type=click.Path(exists=True), required=False,
              help="Value file")
@click.option('--set', '-s', multiple=True,
              help="Overload the value(s) of value file eg: `--set proxy.groups[0].name=mynewtest`")
@click.option('--debug', '-d', is_flag=True,
              help="Do not perform any changes. Show the datas genereted")
@click.option('--config-path', type=click.Path(exists=True), required=False, default="./",
              help="Config folder")
@click.option('--with-deploy', is_flag=True, required=False,
              help="Deploy api after applying")
@click.pass_context
def apply(ctx, api_id, file, set, debug, config_path, with_deploy):
    """
    This command allow to create/update an API
    the API definition is managed with the template engine.
    API values are defined in plain YAML files.

    By default: the values file and template are in the folder `./graviteeio` where the commande is executed
    template file: `apim_api_template.yml.j2`
    value file: `apim_api_value.yml`
    """
    api_client = ctx.obj['api_client']

        # resources_folder = "./{}".format(environments.GRAVITEEIO_RESOURCES_FOLDER)

    # if not os.path.exists(resources_folder):
    #     raise GraviteeioError("No resources folder {} found".format(resources_folder))

    api_sch = ApiSchema(config_path, file)
    api_data = api_sch.get_api_data(debug=debug, set_values=set)

    if debug:
        click.echo("Data sent")
        click.echo(json.dumps(api_data))
    else:
        if api_id:
            click.echo("Starting to apply API: {} '{}'".format(api_id, api_data["name"]))
            resp = api_client.update_import(api_id, api_data)
            click.echo("API {} is updated".format(api_id))

            try:
                ctx.invoke(deploy, api_id=api_id)
            except GraviteeioError:
                click.echo("Error: " + click.style("API could not be deployed", fg="red"))
        else:
            click.echo("Starting to create API: '{}'".format(api_data["name"]))
            resp = api_client.create_import(api_data)
            api_id = resp["id"]
            click.echo("API has been created with id {}".format(api_id))

            if with_deploy:
                try:
                    ctx.invoke(start, api_id=api_id)
                except GraviteeioError:
                    click.echo("Error: " + click.style("API could not be started", fg="red"))





