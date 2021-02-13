import json

import click

from graviteeio_cli.http_client.apim.api import ApiClient

from graviteeio_cli.commands.apim.apis.deploy import deploy
from graviteeio_cli.commands.apim.apis.start import start
from graviteeio_cli.resolvers.conf_resolver import ConfigResolver, Config_Type
from graviteeio_cli.services import lint_service
from graviteeio_cli.lint.types.document import DocumentType
from graviteeio_cli.core.config import GraviteeioConfig
from graviteeio_cli.exeptions import GraviteeioError


@click.command(short_help="Apply API definition.")
@click.option(
    '--api', 'api_id',
    help='API id'
)
@click.option(
    '--values', '-vf','values_file',
    type=click.Path(exists=True), required=False,
    help="Path of values file. By default `Graviteeio` is loaded in the current directory either with the extension `.json` or `.yaml` or `.yml` depending on the format of the data."
)
@click.option(
    '--set', '-s', multiple=True,
    help="Overload the value(s) of values file eg: `--set proxy.groups[0].name=mynewtest`"
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
def apply(ctx, api_id, values_file, set, debug, config_path, with_deploy):
    """
    This command allow to apply an API definition configuration.
    If api id is not filled, api definition will be created.
    api id can be passed in option of command line, with a pipe (i.e echo $API_ID | gio apply ...) or in the values file with api-id param
    The API definition is managed with the template engine (jinja).
    API propetries are defined in plain YAML or JSON files.
    """
    api_client: ApiClient = ctx.obj['api_client']
    gio_config: GraviteeioConfig = ctx.obj['config']

    api_resolver = ConfigResolver(config_path, values_file)
    api_data = api_resolver.get_data(
            Config_Type.API,
            debug=debug,
            set_values=set
    )

    # Lint
    valid = lint_service.validate(api_data, DocumentType.gio_apim, gio_config.linter_conf)
    if not valid:
        raise GraviteeioError("API definition has not been applied. Validation error")

    if debug:
        click.echo("Data sent.")
        click.echo(json.dumps(api_data))
    else:

        if not click.get_text_stream('stdin').isatty() and not api_id:
            stdin_stream = click.get_text_stream('stdin').read().strip()
            api_id = stdin_stream

        if not api_id:
            api_id = api_resolver.get_value("api_id")

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
