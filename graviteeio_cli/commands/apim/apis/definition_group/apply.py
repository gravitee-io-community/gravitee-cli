import json

import click

from graviteeio_cli.http_client.apim.api import ApiClient

from graviteeio_cli.commands.apim.apis.deploy import deploy
from graviteeio_cli.commands.apim.apis.start import start
from graviteeio_cli.resolvers.api_conf_resolver import ApiConfigResolver


@click.command(short_help="Update API definition.")
@click.option(
    '--api', 'api_id',
    help='API id',
    required=True
)
@click.option(
    '--file', '-f',
    type=click.Path(exists=True), required=False,
    help="Path of value file. By default `apim_values` is loaded in the current directory either with the extension `.json` or `.yaml` or `.yml` depending on the format of the data."
)
@click.option(
    '--set', '-s', multiple=True,
    help="Overload the value(s) of value file eg: `--set proxy.groups[0].name=mynewtest`"
)
@click.option(
    '--debug', '-d', is_flag=True,
    help="Do not perform any changes. Display the datas generated"
)
@click.option(
    '--def-path', 'config_path',
    type=click.Path(exists=True), required=False, default=".",
    help="Path of all configuration folders and setting files for api definition. The default value is the current directory"
)
@click.option(
    '--with-deploy', is_flag=True,
    required=False,
    help="Deploy api after applying"
)
@click.pass_context
def apply(ctx, api_id, file, set, debug, config_path, with_deploy):
    """
    This command allow to update an API definition configuration.
    The API definition is managed with the template engine (jinja).
    API propetries are defined in plain YAML or JSON files.
    """
    api_client: ApiClient = ctx.obj['api_client']

    api_resolver = ApiConfigResolver(config_path, file)
    api_data = api_resolver.get_api_data(debug=debug, set_values=set)

    if debug:
        click.echo("Data sent.")
        click.echo(json.dumps(api_data))
    else:
        if api_id:
            click.echo("Starting to apply API: [{}] '{}'.".format(api_id, api_data["name"]))
            resp = api_client.update_import(api_id, api_data)
            click.echo("API [{}] is updated".format(api_id))

            if with_deploy:
                ctx.invoke(deploy, api_id=api_id)

        else:
            click.echo("Starting to create API [{}].".format(api_data["name"]))
            resp = api_client.create_import(api_data)
            api_id = resp["id"]
            click.echo("API has been created with id [{}].".format(api_id))

            if with_deploy:
                ctx.invoke(start, api_id=api_id)
                ctx.invoke(deploy, api_id=api_id)
