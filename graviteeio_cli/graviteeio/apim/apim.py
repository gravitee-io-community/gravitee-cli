import click

from .apis.apis import apis

@click.group()
def apim():
    "Api Management commands"
    pass


apim.add_command(apis)
