import click

from .apis.apis import apis
from .auth.auth import auth

@click.group()
def apim():
    "Api Management commands"
    pass


apim.add_command(apis)
apim.add_command(auth)
