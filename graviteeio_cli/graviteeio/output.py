from terminaltables import AsciiTable
import enum
import click
import yaml
import json
import functools as ft
from functools import reduce


# class gio:


class FormatType (enum.IntEnum):
    table = 1
    json = 2
    yaml = 3
    tsv = 4

    @staticmethod
    def list_name():
        return list (map (lambda c: c.name, FormatType))

    @staticmethod
    def value_of(value):
        for formatType in FormatType:
            if formatType.name == value:
                return formatType


class OutputFormat:
    type: FormatType
    style: tuple = None

    def __init__(self, formatType):
        self.type = formatType

    @staticmethod
    def value_of(value):
        return OutputFormat(FormatType.value_of (value))


class gio:
    @staticmethod
    def tsv(obj_list):
        data = []
        for obj in obj_list:
            items = []
            for item in obj:
                items.append ("{}".format(item))
            data.append(items)

        return "\n".join(['\t'.join (item) for item in data])

    @staticmethod
    def table(data, justify_columns=None):
        table = AsciiTable (data)
        table.inner_footing_row_border = False
        table.inner_row_border = False
        table.inner_column_border = False
        table.outer_border = False

        # print("{}".format(justify_columns))
        if not justify_columns is None:
            table.justify_columns = justify_columns

        return table.table

    @staticmethod
    def echo(obj, format: OutputFormat, header=None):
        # print("" + format)
        # print("{}".format(format == OutputFormat.json))
        # print("{}".format(type(obj)))
        # print("{}".format(type(obj[0])))
        # print("{}".format(obj))
        # print("debug {}".format(format))

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

            if format.type == FormatType.table:
                click.echo (gio.table(data, format.style))
            else:
                click.echo(gio.tsv(data))

        elif format.type == FormatType.json:
            click.echo(json.dumps(obj))
        elif format.type == FormatType.yaml:
            click.echo(yaml.dump(obj))
