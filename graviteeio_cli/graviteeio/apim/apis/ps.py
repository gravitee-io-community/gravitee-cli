import click
from terminaltables import AsciiTable

@click.command()
@click.option('--deploy-state', help='show if API configuration is synchronized', is_flag=True)
@click.pass_obj
def ps(obj, deploy_state):
        """APIs list"""
        api_client = obj['api_client']
        resp =  api_client.get_apis()
        if not resp:
                click.echo("No Api(s) found ")
        else:

                data = []

                if deploy_state:
                        data.append(['id', 'Name', 'Tags', 'Synchronized', 'Status'])
                else:
                        data.append(['id', 'Name', 'Tags', 'Status'])


                for api_item in resp.json():
                        if api_item['state'] == 'started':
                                state_color = 'green'
                        else:
                                state_color = 'red'

                        if 'workflow_state' in api_item:
                                state = click.style(api_item['workflow_state'].upper(), fg='blue')  + "-" + click.style(api_item['state'].upper(), fg=state_color)
                        else:
                                state = click.style(api_item['state'].upper(), fg=state_color)
                        
                        tags = "-"
                        if 'tags' in api_item:
                                tags = ', '.join(api_item['tags'])
                        if not tags:
                                tags = "<none>"

                        if deploy_state:
                                response_state = api_client.state_api(api_item['id'])
                                synchronized = click.style("X", fg='yellow')
                                if response_state.json()["is_synchronized"]:
                                        synchronized = click.style("V", fg='green')
                                
                                data.append([api_item['id'], api_item['name'], tags, synchronized, state])
                        else:

                                if api_item['state'] == 'started':
                                        color = 'green'
                                else:
                                        color = 'red'
                                data.append([api_item['id'], api_item['name'], tags, state])

                table = AsciiTable(data)
                table.inner_footing_row_border = False
                table.inner_row_border = False
                table.inner_column_border  = False
                table.outer_border = False
                if deploy_state:
                        table.justify_columns[3] = 'center'
                        table.justify_columns[4] = 'right'
                else:
                        table.justify_columns[3] = 'right'
                click.echo(table.table)