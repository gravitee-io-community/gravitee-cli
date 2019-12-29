import click

from .update import update


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
    """this command allow to create api configuration"""
    ctx.invoke(update, api_id=None, file=file, set=set, debug=debug, diff=False, templates_folder=templates_folder)
