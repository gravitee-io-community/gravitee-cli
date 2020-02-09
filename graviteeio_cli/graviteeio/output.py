import enum
import functools as ft
import json
import logging
from functools import reduce

import click
import yaml
from termgraph import termgraph as tg
from terminaltables import AsciiTable

# class gio:


class FormatType (enum.IntEnum):
    table = 1
    json = 2
    yaml = 3
    tsv = 4
    hbar = 5

    @staticmethod
    def list_name():
        formatType = list (map (lambda c: c.name, FormatType))
        formatType.remove("hbar")
        return formatType

    @staticmethod
    def extended_list_name():
        return list (map (lambda c: c.name, FormatType))

    @staticmethod
    def value_of(value):
        for formatType in FormatType:
            if formatType.name == value:
                return formatType

class OutputFormat:
    type: FormatType

    def __init__(self, formatType):
        self.type = formatType
    
    def echo(self, data):
        print("OutputFormat")

    @staticmethod
    def value_of(value):
        if value == "table":
            return TableOutputFormat(FormatType.value_of(value))
        elif value == "hbar":
            return HBarOutputFormat(FormatType.value_of(value))
        elif value == "tsv":
            return TsvOutputFormat(FormatType.value_of(value))
        elif value == "json":
            return JsonOutputFormat(FormatType.value_of(value))
        elif value == "yaml":
            return YamlOutputFormat(FormatType.value_of(value))
        else:
            return OutputFormat(FormatType.value_of(value))

class TableOutputFormat(OutputFormat):
    style: tuple = None

    def __init__(self, formatType, style = None):
        super().__init__(formatType)
        self.style = style
    
    def echo(self, data):
        table = AsciiTable (data)
        table.inner_footing_row_border = False
        table.inner_row_border = False
        table.inner_column_border = False
        table.outer_border = False

        if not self.style is None:
            table.justify_columns = self.style

        click.echo(table.table)

class HBarOutputFormat(OutputFormat):

    def __init__(self, formatType):
        super().__init__(formatType)
    
    def echo(self, data):
        
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
        colors = [91, 93, 90, 92,90]
        args = {'filename': 'data/ex4.dat', 'title': None, 'width': 50,
            'format': '{:<5.2f}', 'suffix': '', 'no_labels': False,
            'color': None, 'vertical': False, 'stacked': False,
            'different_scale': False, 'calendar': False,
            'start_dt': None, 'custom_tick': '', 'delim': '',
            'verbose': False, 'version': False}
        # print("{}".format(data[0]))

        if len(data) > 0:
            tg.print_categories(categories, colors)
            tg.chart(colors, values, args, labels)


class TsvOutputFormat(OutputFormat):

    def __init__(self, formatType):
        super().__init__(formatType)

    def echo(self, obj_list):
        data = []
        for obj in obj_list:
            items = []
            for item in obj:
                items.append ("{}".format(item))
            data.append(items)

        click.echo("\n".join(['\t'.join (item) for item in data]))

class JsonOutputFormat(OutputFormat):

    def __init__(self, formatType):
        super().__init__(formatType)

    def echo(self, obj):
        click.echo(json.dumps(obj))

class YamlOutputFormat(OutputFormat):

    def __init__(self, formatType):
        super().__init__(formatType)

    def echo(self, obj):
        click.echo(yaml.dump(obj))

class gio:

    @staticmethod
    def echo(obj, format: OutputFormat, header=None):
        # print("" + format)
        # print("{}".format(format == OutputFormat.json))
        # print("{}".format(type(obj)))
        # print("{}".format(type(obj[0])))
        # print("{}".format(obj))
        # print("debug {}".format(format))
        logging.debug("gio echo obj: {} format {} header {}".format(obj, format, header))
        to_print = obj

        if format.type == FormatType.table or format.type == FormatType.tsv:
            data = []

            if not header:
                header = []
                for x in range(2):
                    header.append("")

            data.append (header)

            # print("{}".format(obj))
            if type(obj) is dict:
                data.extend(obj.items())
            elif obj and type(obj) is list and not type(obj[0]) is list and not type(obj[0]) is dict:
                data.extend(list(map(lambda c: [c], obj)))
            elif obj and type(obj) is list and type(obj[0]) is dict:
                data.extend(map(lambda api: api.values(), obj))
            else:
                data.extend(obj)

            to_print = data
        
        if format.type == FormatType.hbar:
            # print("{}".format(obj))
            data = []
            categories = []
            labels = []

            for value in obj:

                for num,key in enumerate(value.keys()):
                    if num == 0 and not value[key] in categories:
                        categories.append(value[key])
                    
                    if num > 0:
                        if len(data) == 0:
                            data.append([])

                        data[num - 1].append(value[key])


            if not header:
                header = []
                for x in range(2):
                    header.append("")
            labels=list(header)[1:]

            to_print = []
            to_print.append(categories)
            to_print.append(labels)
            to_print.append(data)

        format.echo(to_print)
