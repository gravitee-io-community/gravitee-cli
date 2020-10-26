import json
import yaml
import os
from enum import Enum
from io import StringIO


def load_yaml(stream):
    return yaml.load(stream, Loader=yaml.SafeLoader)


def load_json(stream):
    io = StringIO(stream)
    return json.load(io)


def dump_yaml(data):
    return yaml.dump(data)


def dump_json(data):
    io = StringIO()
    json.dump(data, io, indent=2)
    return io.getvalue()


class File_Format_Enum(Enum):
    YAML = {
        'num': 1,
        'extentions': ['.yml', '.yaml'],
        'load': load_yaml,
        'dump': dump_yaml
    }
    JSON = {
        'num': 2,
        'extentions': ['.json'],
        'load': load_json,
        'dump': dump_json
    }

    def __init__(self, values):
        self.num = values['num']
        self.extentions = values['extentions']
        self.load = values['load']
        self.dump = values['dump']

    @staticmethod
    def find(extention):
        for file_format in File_Format_Enum:
            if extention in file_format.extentions:
                return file_format
            else:
                return None

    @staticmethod
    def list_name():
        return list(map(lambda c: c.name, File_Format_Enum))

    @staticmethod
    def value_of(value):
        for data_type in File_Format_Enum:
            if data_type.name == value.upper():
                return data_type

    @staticmethod
    def extention_list():
        tuple_to_return = []

        for format in File_Format_Enum:
            if type(format.extentions) is tuple:
                for extention in format.extentions:
                    tuple_to_return.append(extention)
            else:
                tuple_to_return.append(format.extentions)

        return tuple(tuple_to_return)


def load_file(file_path, file_data):
    toReturn = None
    filename, file_extension = os.path.splitext(file_path)

    file_format = File_Format_Enum.find(file_extension)

    if file_format:
        toReturn = file_format.load(file_data)

    return toReturn



    # @staticmethod
    # def find(extention):
    #     to_return = None
    #     if extention in map_extention:
    #         to_return = map_extention[extention]
    #     return to_return

    # @staticmethod
    # def list_name():
    #     return list(map(lambda c: c.name, Data_Template_Format))

    # @staticmethod
    # def value_of(value):
    #     for data_type in Data_Template_Format:
    #         if data_type.name == value.upper():
    #             return data_type

    # @staticmethod
    # def extention_list():
    #     tuple_to_return = []

    #     for format in Data_Template_Format:
    #         if type(format.extentions) is tuple:
    #             for extention in format.extentions:
    #                 tuple_to_return.append(extention)
    #         else:
    #             tuple_to_return.append(format.extentions)

    #     return tuple(tuple_to_return)