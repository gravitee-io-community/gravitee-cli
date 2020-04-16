import click

from .apis.apis import apis

@click.group(invoke_without_command=True)
def apim():
    "Api Management action"
    pass


apim.add_command(apis)
