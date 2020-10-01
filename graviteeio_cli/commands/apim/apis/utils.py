import click

EXCLUDED_API_VALUES = [
    'owner',
    'picture_url',
    'deployed_at',
    'created_at',
    'updated_at',
    'lifecycle_state',
    'id',
    'state',
    'entrypoints',
    'workflow_state',
    'picture'
]

EXLUDED_API_PLAN_VALUES = [
    'id',
    'apis',
    'created_at',
    'updated_at',
    'published_at'
]


def update_dic_with_set(set_value, dic):
    (key, value) = set_value.split('=')

    __update_dict(key, value, dic)

    return dic


def __update_dict(key, value, dic):
    keys = key.split('.', 1)
    new_key = keys[0]
    index_list = None

    if new_key.find('[') > 0 and new_key.find(']') > 0:
        index_list = int(new_key[new_key.find('[') + 1: new_key.find(']')])
        new_key = new_key[0:new_key.find('[')]

    if len(keys) == 1:
        if index_list is None:
            dic[new_key] = value
        else:
            if len(dic[new_key]) < index_list + 1:
                dic[new_key].append(value)
            else:
                dic[new_key][index_list] = value
    else:
        if index_list is None:
            __update_dict(keys[1], value, dic[new_key])
        else:
            __update_dict(keys[1], value, dic[new_key][index_list])


def filter_api_values(api_data):
    for key in EXCLUDED_API_VALUES:
        if key in api_data:
            del api_data[key]

    if 'plans' in api_data:
        for plan in api_data['plans']:
            for key in EXLUDED_API_PLAN_VALUES:
                if key in plan:
                    del plan[key]


def display_dict_differ(dict_differ):
    has_diff = False
    summary = {
        "created": 0,
        "updated": 0,
        "deleted": 0
    }
    for diff_tuple in dict_differ:
        has_diff = True
        if diff_tuple[0] == 'change':
            # click.echo(click.style('- {}: {}'.format(diff_tuple[1], diff_tuple[2][0]), fg='red') + " " + click.style('+ {}: {}'.format(diff_tuple[1], diff_tuple[2][1]), fg='green'))
            click.echo(click.style('- {}: {}'.format(format_key(diff_tuple[1]), diff_tuple[2][0]), fg='red'))
            click.echo(click.style('+ {}: {}'.format(format_key(diff_tuple[1]), diff_tuple[2][1]), fg='green'))
            click.echo()

            summary["updated"] = summary["updated"] + 1

        elif diff_tuple[0] == 'add' or diff_tuple[0] == 'remove':
            char_action = '+'
            color_action = 'green'

            if diff_tuple[0] == 'remove':
                char_action = '-'
                color_action = 'red'
                summary["deleted"] = summary["deleted"] + 1
            else:
                summary["created"] = summary["created"] + 1

            if len(diff_tuple[1]) > 0:
                click.echo(click.style('{} {}:'.format(char_action, format_key(diff_tuple[1])), fg=color_action))

            for add_value in diff_tuple[2]:
                # to_display = { 'message': 'diff_key {}', 'var':{'tuple':diff_tuple}}
                message = ''

                if isinstance(add_value[0], int):
                    message = '  {1} {0} {2}'

                elif isinstance(add_value[0], str) and len(diff_tuple[1]) > 0:
                    if isinstance(add_value[1], dict):
                        message = '  {0} {1}: \n    {2}'
                    else:
                        message = '  {0} {1}: {2}'

                elif isinstance(add_value[0], str):
                    message = '{0} {1}: {2}'

                click.echo(click.style(message.format(char_action, add_value[0], add_value[1]), fg=color_action))

            click.echo()
        else:
            click.echo("diff_key {}".format(diff_tuple))

    click.echo(click.style("--------", fg="green"))
    click.echo(click.style("Summary:", fg="green"))
    click.echo(click.style("- Created:{}".format(summary["created"]), fg="green"))
    click.echo(click.style("- Updated:{}".format(summary["updated"]), fg="green"))
    click.echo(click.style("- Deleted:{}".format(summary["deleted"]), fg="green"))

    if not has_diff:
        click.echo("No diff")


def format_key(key):
    def map_func(x):
        if isinstance(x, int):
            return '[' + str(x) + ']'
        else:
            return x

    if isinstance(key, list):
        return ".".join(map(map_func, key)).replace('.[', '[')
    else:
        return key
