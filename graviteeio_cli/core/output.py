import enum
import json

import click
import yaml
from termgraph import termgraph as tg
from terminaltables import AsciiTable


class DataAdapter:
    @staticmethod
    def Table(obj, header, empty_header):
        data = []

        if not header and empty_header:
            header = []
            for _ in range(2):
                header.append("")

        if header:
            data.append(header)

        # print("{}".format(obj))
        if type(obj) is dict:
            data.extend(obj.items())
        elif obj and type(obj) is list and not type(obj[0]) is list and not type(obj[0]) is dict:
            data.extend(list(map(lambda c: [c], obj)))
        elif obj and type(obj) is list and type(obj[0]) is dict:
            data.extend(map(lambda api: api.values(), obj))
        elif type(obj) is object or type(obj) is list:
            data.extend(obj)
        else:
            data.append([obj])

        return data


class Output():

    def adapter(self, obj, header, empty_header):
        pass

    def print(self, obj, **kwargs):
        pass

    def echo(self, object, **kwargs):
        header = None
        if 'header' in kwargs:
            header = kwargs['header']

        empty_header = True
        if "inner_heading_row_border" in kwargs:
            empty_header = kwargs["inner_heading_row_border"]

        self.print(self.adapter(object, header, empty_header), **kwargs)


class TableOutput(Output):

    def adapter(self, obj, header, empty_header):
        return DataAdapter.Table(obj, header, empty_header)

    def print(self, data, **kwargs):
        table = AsciiTable(data)
        table.inner_footing_row_border = False
        table.inner_row_border = False
        table.inner_column_border = False
        table.outer_border = False
        if "inner_heading_row_border" in kwargs:
            table.inner_heading_row_border = kwargs["inner_heading_row_border"]

        if "style" in kwargs:
            table.justify_columns = kwargs["style"]

        click.echo(table.table)


class HBarOutput(Output):
    def adapter(self, obj, header, empty_header):
        data = []
        categories = []
        labels = []

        for value in obj:

            for num, key in enumerate(value.keys()):
                if num == 0 and not value[key] in categories:
                    categories.append(value[key])

                if num > 0:
                    # if len(data) == 0:
                    #     data.append([])
                    if len(data) == num - 1:
                        data.append([])

                    data[num - 1].append(value[key])

        if not header:
            header = []
            for _ in range(2):
                header.append("")
        labels = list(header)[1:]

        to_print = []
        to_print.append(categories)
        to_print.append(labels)
        to_print.append(data)

        return to_print

    def print(self, data, **kwargs):
        categories = data[0]
        labels = data[1]
        values = data[2]

        # AVAILABLE_COLORS = {
        #     'red': 91,
        #     'blue': 94,
        #     'green': 92,
        #     'magenta': 95,
        #     'yellow': 93,
        #     'black': 90,
        #     'cyan': 96
        # }
        colors = [91, 93, 90, 92, 90]
        args = {
            'filename': 'data/ex4.dat', 'title': None, 'width': 50,
            'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
            'color': None, 'vertical': False, 'stacked': False,
            'different_scale': False, 'calendar': False,
            'start_dt': None, 'custom_tick': '', 'delim': '',
            'verbose': False, 'version': False
        }
        # print("{}".format(data[0]))

        if len(data) > 0:
            tg.print_categories(categories, colors)
            tg.chart(colors, values, args, labels)


class TsvOutput(Output):

    def adapter(self, obj, header, empty_header):
        return DataAdapter.Table(obj, header, False)

    def print(self, obj_list, **kwargs):
        data = []
        for obj in obj_list:
            items = []
            for item in obj:
                items.appends("{}".format(item))
            data.append(items)

        click.echo("\n".join(['\t'.join(item) for item in data]))


class JsonOutput(Output):
    def adapter(self, obj, header, empty_header):
        return obj

    def print(self, data, **kwargs):
        click.echo(json.dumps(data, indent=2))


class YamlOutput(Output):
    def adapter(self, obj, header, empty_header):
        return obj

    def print(self, data, **kwargs):
        click.echo(yaml.dump(data, sort_keys=False))


class OutputFormatType(enum.Enum):
    TABLE = {
        'num': 1,
        'echo': TableOutput().echo
    }

    JSON = {
        'num': 2,
        'echo': JsonOutput().echo
    }

    YAML = {
        'num': 3,
        'echo': YamlOutput().echo
    }

    TSV = {
        'num': 4,
        'echo': TsvOutput().echo
    }

    HBAR = {
        'num': 5,
        'echo': HBarOutput().echo
    }

    def __init__(self, values):
        self.num = values['num']
        self.echo = values['echo']

    @staticmethod
    def list_name():
        formatType = list(map(lambda c: c.name.lower(), OutputFormatType))
        formatType.remove("hbar")
        return formatType

    @staticmethod
    def extended_list_name():
        return list(map(lambda c: c.name, OutputFormatType))

    @staticmethod
    def value_of(value):
        for output in OutputFormatType:
            if output.name == value.upper():
                return output
