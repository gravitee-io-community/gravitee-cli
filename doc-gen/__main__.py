import os

import click

from graviteeio_cli.__version__ import __version__ as VERSION
from graviteeio_cli.cli import main
from graviteeio_cli.graviteeio.apim.apis.apis import PluginCommand

from .doc_page import DocPage


def generate_page(name, ctx, version=None):
    doc_page = DocPage(name, ctx, version)
    return str(doc_page)

# def write_man_pages(name, cli, parent_ctx=None, version=None, target_dir=None):
def write_pages(name, cli, version, parent_ctx = None, target_dir = None):

    ctx =  click.Context(cli, info_name=name, parent=parent_ctx)
    doc_page = generate_page(name, ctx, version)


    path = '{0}.adoc'.format(ctx.command_path.replace(' ', '_'))
    if target_dir:
        path = os.path.join(target_dir, path)

    if not isinstance(ctx.command, click.Group):
        print("Write page {}".format(path))
        with open(path, 'w+') as f:
            f.write(doc_page)

    if hasattr(cli, 'list_commands'):
        commands_name = cli.list_commands(ctx)
        for name in commands_name:
            write_pages(name, cli.get_command(ctx, name), parent_ctx=ctx, version=version, target_dir=target_dir)


def cli():
    # graviteeio_cli = "../graviteeio_cli/cli.py"
    source_path = 'docs/command_reference'
    path = os.path.join(os.getcwd(), source_path, VERSION)

    if not os.path.exists(path):
        print(path)
        os.mkdir(path)
    # if os.path.exists("./docs/command_reference")

    write_pages("gio", main, VERSION, target_dir = path)


if __name__ == '__main__':
    cli()
