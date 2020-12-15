import json

import click

from graviteeio_cli.http_client.apim.api import ApiClient

from graviteeio_cli.commands.apim.apis.deploy import deploy
from graviteeio_cli.commands.apim.apis.start import start
from graviteeio_cli.resolvers.api_conf_resolver import ApiConfigResolver
from graviteeio_cli.services import lint_service
from graviteeio_cli.lint.types.document import DocumentType
from graviteeio_cli.core.config import GraviteeioConfig


@click.command(short_help="Update API definition.")
@click.option(
    '--api', 'api_id',
    help='API id',
    required=True
)
@click.option(
    '--file', '-f',
    type=click.Path(exists=True), required=False,
    help="Path of value file. By default `Graviteeio` is loaded in the current directory either with the extension `.json` or `.yaml` or `.yml` depending on the format of the data."
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
    gio_config: GraviteeioConfig = ctx.obj['config']

    api_resolver = ApiConfigResolver(config_path, file)
    api_data = api_resolver.get_api_data(debug=debug, set_values=set)

    # Lint
    valid = lint_service.validate(api_data, DocumentType.gio_apim, gio_config.linter_conf)
    if not valid:
        click.echo(click.style(" API definition has not been applied", fg="red"))
        return

    if debug:
        click.echo("Data sent.")
        click.echo(json.dumps(api_data))
    else:
        if api_id:
            click.echo(f"Starting to apply API: [{api_id}] '{api_data['name']}'.")
            resp = api_client.update_import(api_id, api_data)
            click.echo(f"API [{api_id}] is updated")

            if with_deploy:
                ctx.invoke(deploy, api_id=api_id)

        else:
            click.echo(f"Starting to create API [{api_data['name']}].")
            resp = api_client.create_import(api_data)
            api_id = resp["id"]
            click.echo(f"API has been created with id [{api_id}].")

            if with_deploy:
                ctx.invoke(start, api_id=api_id)
                ctx.invoke(deploy, api_id=api_id)
