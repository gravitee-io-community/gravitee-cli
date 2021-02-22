import logging
import os
import enum

from jinja2 import (Environment, FileSystemLoader, TemplateNotFound)

from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.extensions.jinja_filters import filter_loader
from graviteeio_cli.commands.apim.apis.utils import update_dic_with_set
from graviteeio_cli.core.file_format import File_Format_Enum

from graviteeio_cli import environments as env
from . import init_templates as init_tpl

logger = logging.getLogger("class-config_resolver")

CONFIG_FORMATS = [File_Format_Enum.JSON, File_Format_Enum.YAML]


class Config_Type(enum.Enum):
    API = {
        "conf_file_name": env.API_CONFIG_FILE_NAME,
        "init_config": init_tpl.templates_api
    }

    APP = {
        "conf_file_name": env.APP_CONFIG_FILE_NAME,
        "init_config": init_tpl.templates_app
    }

    def __init__(self, values):
        self.conf_file_name = values['conf_file_name']
        self.init_config = values['init_config']


class ConfigResolver:

    def __init__(self, resources_folder, value_file_path=None):
        self.folders = {}
        self.files = {}
        self.loaded_configs = {}
        resources_folder = resources_folder.strip()
        self.folders["templates_folder"] = "{}/{}".format(resources_folder, env.GIO_TEMPLATES_FOLDER)
        self.folders["settings_folder"] = "{}/{}".format(resources_folder, env.GIO_SETTING_FOLDER)

        if not value_file_path or len(value_file_path) == 0:
            value_file_path = '{}/{}'.format(
                resources_folder,
                env.GIO_VALUE_FILE_NAME
            )

        self.files["value_file_path"] = value_file_path
        self.templates = {}

    def get_data(self, config_type: Config_Type, debug=None, set_values=[]):
        self._load_conf_directories()

        if config_type.name not in self.templates:
            self._load_template(config_type)

        api_data_rendered = None

        for set_value in set_values:
            self.vars["Values"] = update_dic_with_set(set_value, self.vars["Values"])

        api_data_rendered = self.templates[config_type.name].render(self.vars)

        if debug:
            print("Render:")
            print(api_data_rendered)

        api_data_dic = self.config_format.load(api_data_rendered)

        if 'version' in api_data_dic:
            api_data_dic['version'] = str(api_data_dic['version'])

        return api_data_dic

    def get_value(self, name):
        if "Values" not in self.vars:
            self._load_conf_directories()

        if self.vars["Values"] and name in self.vars["Values"]:
            return self.vars["Values"][name]
        else:
            return None

    def _load_template(self, config_type: Config_Type):
        full_conf_file_name = None

        conf_file_name = config_type.conf_file_name
        conf_file_path = f"{self.folders['templates_folder']}/{conf_file_name}"
        # root_template_path_file = self.files["root_template_path_file"]

        for (data_format, extention) in ((data_format, extention) for data_format in CONFIG_FORMATS for extention in data_format.extentions):
            if not full_conf_file_name and os.path.exists(conf_file_path.format(extention)):
                self.config_format = data_format
                full_conf_file_name = conf_file_name.format(extention)

            if full_conf_file_name:
                break

        if not full_conf_file_name:
            raise GraviteeioError("Missing file {} or {}".format(
                conf_file_name.format(".yml"),
                conf_file_name.format(".json"))
            )

        self.templates[config_type.name] = self._get_template(full_conf_file_name, self.folders["templates_folder"])

    def _get_template(self, full_config_file_name, templates_folder):
        j2_env = Environment(loader=FileSystemLoader(templates_folder), trim_blocks=False, autoescape=False)
        filter_loader(j2_env)

        try:
            template = j2_env.get_template(full_config_file_name)
        except TemplateNotFound:
            raise GraviteeioError("Template not found, try to load {}".format(full_config_file_name))

        return template

    def _load_conf_directories(self):
        for key in self.folders:
            if not os.path.exists(self.folders[key]):
                raise GraviteeioError("Missing folder {}".format(self.folders[key]))

        value_file_path = None
        value_file_format: File_Format_Enum = None

        if os.path.exists(self.files["value_file_path"]):
            value_file_path = self.files["value_file_path"]

        for (data_format, extention) in ((data_format, extention) for data_format in CONFIG_FORMATS for extention in data_format.extentions):

            file = self.files["value_file_path"].format(extention)
            if not value_file_path and os.path.exists(file):
                value_file_format = data_format
                value_file_path = file

            if value_file_path:
                break

        if not value_file_path:
            raise GraviteeioError("Missing file {} or {}".format(
                env.GIO_VALUE_FILE_NAME.format(".yml"),
                env.GIO_VALUE_FILE_NAME.format(".json"))
            )

        self.vars = self._get_vars_for_template(value_file_path, value_file_format)

    def _get_values_string(self, value_file):
        values_string = None
        try:
            with open(value_file, 'r') as f:
                # api_value_string = f.read()
                values_string = f.read()
        except OSError:
            raise GraviteeioError("Cannot open file {}".format(value_file))

        return values_string

    def _get_vars_for_template(self, value_file_path, value_file_format: File_Format_Enum):
        template_vars = {}

        value_string = self._get_values_string(value_file_path)
        template_vars["Values"] = value_file_format.load(value_string)

        settings_folder = self.folders["settings_folder"]
        for file in os.listdir(settings_folder):
            if not file.startswith(('_', ".")):
                try:
                    with open("/".join([settings_folder, file]), 'r') as f:
                        config_string = f.read()
                except OSError:
                    raise GraviteeioError("Cannot open {}".format(file))

                filename, file_extension = os.path.splitext(file)
                file_format = File_Format_Enum.find(file_extension)

                if file_format:
                    template_vars[filename] = file_format.load(config_string)

        return template_vars

    def generate_init(self, config_type: Config_Type, format=File_Format_Enum.YAML, config_values=None, debug=False):
        for key in self.folders:
            if debug:
                print("mkdir {}".format(self.folders[key]))
            else:
                try:
                    os.mkdir(self.folders[key])
                except OSError:
                    print("Creation folder [%s] failed" % self.folders[key])
                else:
                    print("Successfully created directory %s " % self.folders[key])

        conf_file_path = f"{self.folders['templates_folder']}/{config_type.conf_file_name}"

        if not config_values:
            tpl = config_type.init_config[format.name.lower()]["template"]
            values = config_type.init_config[format.name.lower()]["value_file"]
        else:
            tpl = format.dump(config_values)
            values = ""

        write_files = {
            conf_file_path.format(format.extention): tpl,
        }

        setting_files = config_type.init_config[format.name.lower()]["setting_files"]
        for file, tpl_value in setting_files.items():
            path = "{}/{}".format(self.folders["settings_folder"], file.format(format.extention))
            write_files[path] = tpl_value

        for key in write_files:
            if debug:
                print("write file {}".format(key))
            else:
                try:
                    with open(key, 'x') as f:
                        f.write(write_files[key])
                except OSError:
                    print("Creation of the file %s failed" % key)
                else:
                    print("Successfully created file %s " % key)

        # write values file
        values_file_path = self.files["value_file_path"].format(format.extention)
        if os.path.exists(values_file_path):
            values = '\n' + values
        try:
            with open(values_file_path, 'a') as f:
                f.write(values)
        except OSError:
            print("Creation of the file %s failed" % key)
        else:
            print("Successfully created file %s " % key)


    # def _api_def_to_template(self, api_def, format):
    #     values = {}

    #     values["version"] = api_def["version"]
    #     values["name"] = api_def["name"]
    #     values["description"] = api_def["description"]

    #     api_def["version"] = "{{ Values.version}}"
    #     api_def["name"] = "{{ Values.name}}"
    #     api_def["description"] = "{{ Values.description}}"

    #     write_files = {
    #         self.files["root_template_path_file"].format(format.extentions[0]): format.dump(api_def),
    #         self.files["value_file"].format(format.extentions[0]): format.dump(values),
    #         "{}/{}".format(self.folders["settings_folder"], "Http{}".format(format.extentions[0])): ""
    #     }

    #     return write_files