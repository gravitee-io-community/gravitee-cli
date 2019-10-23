import click, terminaltables, yaml, json, os, requests, time

from .ps import ps
from .actions import start, stop, deploy
from .update import update
from .load_template import init, upgrade
from dictdiffer import diff as jsondiff
#import logging

from click.exceptions import ClickException
from ..client.api import api_client
from .api_schema import api_schema
from ....exeptions import GraviteeioRequestError, GraviteeioError
from ...utils import convert_proxy_config, clean_api
from .... import environments

@click.group()
@click.pass_context
def apis(ctx):
        ctx.obj['api_client'] = api_client(config = ctx.obj['config'])
        
        
apis.add_command(ps)
apis.add_command(start)
apis.add_command(stop)
apis.add_command(deploy)
apis.add_command(init)
apis.add_command(upgrade)
apis.add_command(update)

