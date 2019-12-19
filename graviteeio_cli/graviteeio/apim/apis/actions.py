# import click


# @click.command()
# @click.argument('api_id', required=True)
# @click.pass_obj
# def start(obj, api_id):
#     """start api"""
#     api_client = obj['api_client']
#     resp = api_client.start_api(api_id)
#     click.echo("API {} is started".format(api_id))


# @click.command()
# @click.argument('api_id', required=True)
# @click.pass_obj
# def stop(obj, api_id):
#     """stop api"""
#     api_client = obj['api_client']
#     resp = api_client.stop_api(api_id)
#     click.echo("API {} is stopped".format(api_id))


# @click.command()
# @click.argument('api_id', required=True)
# @click.pass_obj
# def deploy(obj, api_id):
#     """deploy api configuration"""
#     api_client = obj['api_client']
#     resp = api_client.deploy_api(api_id)
#     click.echo("API {} is deployed".format(api_id))
