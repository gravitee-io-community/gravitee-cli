import json

import click

from graviteeio_cli.http_client.apim.app import AppClient

from graviteeio_cli.resolvers.conf_resolver import ConfigResolver, Config_Type
from graviteeio_cli.services import lint_service
from graviteeio_cli.lint.types.document import DocumentType
from graviteeio_cli.core.config import GraviteeioConfig
from graviteeio_cli.exeptions import GraviteeioError


@click.command(short_help="Update APP configuration.")
@click.option(
    '--app', 'app_id',
    help='APP id'
)
@click.option(
    '--debug', '-d', is_flag=True,
    help="Do not perform any changes. Display the datas generated"
)
@click.option(
    '--values', '-fv', 'values_file',
    type=click.Path(exists=True), required=False,
    help="Path of values file. By default `app_config` is loaded in the current directory either with the extension `.json` or `.yaml` or `.yml` depending on the format of the data."
)
@click.option(
    '--set', '-s', multiple=True,
    help="Overload the value(s) of values file eg: `--set name=new_name`"
)
@click.option(
    '--def-path', 'config_path',
    type=click.Path(exists=True), required=False, default=".",
    help="Path of all configuration folders and setting files for app configuration. The default value is the current directory"
)
@click.pass_context
def apply(ctx, app_id, values_file, set, debug, config_path):
    """
    This command allow to apply an APP configuration.
    If app id is not filled, api definition will be created. 
    app id can be passed in option of command line, with a pipe (i.e echo $APP_ID | gio apply ...) or in the values file with app-id param
    The APP is managed with the template engine (jinja).
    APP propetries are defined in plain YAML or JSON files.
    """
    app_client: AppClient = ctx.obj['app_client']
    # gio_config: GraviteeioConfig = ctx.obj['config']

    app_resolver = ConfigResolver(config_path, values_file)
    app_data = app_resolver.get_data(
            Config_Type.APP,
            set_values=set,
            debug=debug
    )

    if debug:
        click.echo("Data sent.")
        click.echo(json.dumps(app_data))
    else:

        if not click.get_text_stream('stdin').isatty() and not app_id:
            stdin_stream = click.get_text_stream('stdin').read().strip()
            app_id = stdin_stream

        if not app_id:
            app_id = app_resolver.get_value("app_id")

        if app_id:
            click.echo(f"Starting to apply APP: [{app_id}] '{app_data['name']}'.")
            resp = app_client.update_import(app_id, app_data)
            click.echo(f"APP [{app_id}] is updated")
        else:
            click.echo(f"Starting to create APP [{app_data['name']}].")
            resp = app_client.create_import(app_data)
            app_id = resp["id"]
            click.echo(f"APP has been created with id [{app_id}].")
