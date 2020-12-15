import click
import requests
import logging
import os

from graviteeio_cli.core.config import GraviteeioConfig
from graviteeio_cli.exeptions import GraviteeioError

# rulset_url = "https://raw.githubusercontent.com/GGui/graviteeio-lint-ruleset/main/ruleset.yml"

logger = logging.getLogger("command-pages-update")


@click.group()
def linter():
    """
    `profiles` command allow to config linter

    Configuration values are stored in file with structure of INI file. The config file is located `~/graviteeio`.

    Environment variables:

    * `GRAVITEEIO_CONF_FILE`: file of CLI conf. Default `~/graviteeio`.

    Default environment: `env`. To config the linter, you can use the following environment variables:
    * `GIO_RULESET`: Ruleset url. Default `None`.
    * `GIO_TTL_RULESET`: TTL in minute for ruleset cache . Default `5`.
    """
    pass


def display_list(list):
    display = ""
    if list and len(list) > 0:
        display = "\n  - " + "\n  - ".join(list)
    else:
        display = "-"

    return display


@click.command(short_help="Save config for linter.")
@click.option('--ruleset', '-r', "ruleset_files", help="Ruleset PATH or URL", type=click.STRING, required=False, multiple=True)
@click.option('--ttl', help='Ruleset ttl', type=click.INT, required=False)
@click.pass_obj
def set_(obj, ruleset_files, ttl):

    gio_config: GraviteeioConfig = obj['config']
    to_save = {}

    for file in ruleset_files:
        if file.startswith("http://") or file.startswith("https://"):
            try:
                requests.get(file)
            except Exception:
                raise GraviteeioError('Invalid value for "--file" / "-f": Call error for URL "{}".'.format(file))

        else:
            if not os.path.exists(file):
                raise GraviteeioError('Invalid value for "--file" / "-f": Path "{}" does not exist.'.format(file))

    ruleset_to_save = None
    if gio_config.linter_conf["ruleset_files"] and len(gio_config.linter_conf["ruleset_files"]) > 0:
        set_ = set(gio_config.linter_conf["ruleset_files"])
        set_.update(ruleset_files)
        ruleset_to_save = list(set_)
    else:
        ruleset_to_save = list(ruleset_files)

    if ruleset_files:
        to_save["ruleset_files"] = ruleset_to_save
    if ttl:
        to_save["ruleset_ttl"] = ttl

    gio_config.save_linter_conf(**to_save)
    click.echo("Linter data saved")


@click.command(short_help="Save config for linter.")
@click.option('--ruleset-index', '-ri', "ruleset_index", help="Ruleset index to remove", type=click.INT, required=True, multiple=True)
@click.pass_obj
def remove(obj, ruleset_index):
    gio_config: GraviteeioConfig = obj['config']

    ruleset_path_removed = []
    files = gio_config.linter_conf["ruleset_files"]

    for index in ruleset_index:
        if index < 1:
            raise GraviteeioError("ruleset-index must be greater than 1")

        if index > len(files):
            raise GraviteeioError("ruleset-index is too high. index max is [{}]".format(len(files)))

    for index in ruleset_index:
        ruleset_path_removed.append(files[index - 1])
        del(files[index - 1])

    gio_config.save_linter_conf(ruleset_files=files)
    click.echo("Linter file(s) removed: {}".format(display_list(ruleset_path_removed)))


@click.command(short_help="Display config for linter.")
@click.pass_obj
def config(obj):
    gio_config: GraviteeioConfig = obj['config']

    display_ruleset = "-"
    if "ruleset_files" in gio_config.linter_conf:
        display_ruleset = display_list(gio_config.linter_conf["ruleset_files"])

    click.echo("Configuration:\n Ruleset URL: {}\n Ruleset TTL: {}".format(display_ruleset, gio_config.linter_conf["ruleset_ttl"]))


linter.add_command(set_, "set")
linter.add_command(remove)
linter.add_command(config)
