import click

from .apply import apply


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True), required=False,
              help="Value file")
@click.option('--set', '-s', multiple=True,
              help="Overload the value(s) of value file eg: `--set proxy.groups[0].name=mynewtest`")
@click.option('--debug', '-d', is_flag=True,
              help="Do not perform any changes. Show the datas genereted")
@click.option('--config-path', type=click.Path(exists=True), required=False, default="./",
              help="Config folder")
@click.option('--with-start', is_flag=True, required=False,
              help="Deploy and start api after creation")
@click.pass_context
def create(ctx, file, set, debug, config_path, with_start):
    """This command allow to create api"""
    ctx.invoke(apply, api_id=None, file=file, set=set, debug=debug, config_path=config_path, with_deploy=with_start)
