import click

from .apply import apply


@click.command(short_help="Create API definition.")
@click.option(
    '--file', '-f', type=click.Path(exists=True), required=False,
    help="Path of value file. By default `apim_values` is loaded in the current directory either with the extension `.json`or `.yaml` or `.yml` depending on the format of the data."
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
    '--def-path', 'config_path', type=click.Path(exists=True),
    required=False, default=".",
    help="Path of all configuration foldes and setting files. The default value is the current directory"
)
@click.option(
    '--with-start', is_flag=True, required=False,
    help="Deploy and start api after creation"
)
@click.pass_context
def create(ctx, file, set, debug, config_path, with_start):
    """
    This command allow to create api definition.
    """
    ctx.invoke(
        apply,
        api_id=None,
        file=file,
        set=set,
        debug=debug,
        config_path=config_path,
        with_deploy=with_start
    )
