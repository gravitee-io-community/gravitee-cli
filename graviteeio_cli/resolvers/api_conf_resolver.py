import logging
import os

from jinja2 import (Environment, FileSystemLoader, TemplateNotFound)

from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.extensions.jinja_filters import filter_loader
from graviteeio_cli.commands.apim.apis.utils import update_dic_with_set
from graviteeio_cli.core.file_format import File_Format_Enum

from graviteeio_cli import environments
from . import init_template as init_tpl

logger = logging.getLogger("class-ApiConfigResolver")

TEMPLATE_FORMAT = [File_Format_Enum.JSON, File_Format_Enum.YAML]


class ApiConfigResolver:

    def __init__(self, resources_folder, value_file=None):
        self.folders = {}
        self.files = {}
        self.loaded_schema = False

        self.folders["templates_folder"] = "{}/{}".format(resources_folder, environments.APIM_API_TEMPLATES_FOLDER)
        self.folders["settings_folder"] = "{}/{}".format(resources_folder, environments.APIM_API_SETTING_FOLDER)

        self.files["root_template_path_file"] = "{}/{}".format(self.folders["templates_folder"], environments.APIM_API_TEMPLATE_FILE)

        if not value_file or len(value_file) == 0:
            value_file = '{}/{}'.format(
                resources_folder,
                environments.APIM_API_VALUE_FILE_NAME
            )

        self.files["value_file"] = value_file

    def generate_init(self, format=File_Format_Enum.YAML, api_def=None, debug=False):
        for key in self.folders:
            if debug:
                print("mkdir {}".format(self.folders[key]))
            else:
                try:
                    os.mkdir(self.folders[key])
                except OSError:
                    print("Creation of the file %s failed" % self.folders[key])
                else:
                    print("Successfully created directory %s " % self.folders[key])

        write_files = {
            self.files["root_template_path_file"].format(format.extentions[0]): init_tpl.templates[format.name.lower()]["template"],
            self.files["value_file"].format(format.extentions[0]): init_tpl.templates[format.name.lower()]["value_file"],
            "{}/{}".format(self.folders["settings_folder"], "Http{}".format(format.extentions[0])): init_tpl.templates[format.name.lower()]["setting_http"]
        }

        if api_def:
            write_files = self._api_def_to_template(api_def, format)

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

    def _api_def_to_template(self, api_def, format):
        values = {}

        values["version"] = api_def["version"]
        values["name"] = api_def["name"]
        values["description"] = api_def["description"]

        api_def["version"] = "{{ Values.version}}"
        api_def["name"] = "{{ Values.name}}"
        api_def["description"] = "{{ Values.description}}"

        write_files = {
            self.files["root_template_path_file"].format(format.extentions[0]): format.dump(api_def),
            self.files["value_file"].format(format.extentions[0]): format.dump(values),
            "{}/{}".format(self.folders["settings_folder"], "Http{}".format(format.extentions[0])): ""
        }

        return write_files

    def get_api_data(self, debug=None, set_values=[]):
        if not self.loaded_schema:
            self._load_api_conf_directories()

        api_data_rendered = None

        for set_value in set_values:
            self.api_vars["Values"] = update_dic_with_set(set_value, self.api_vars["Values"])

        api_data_rendered = self.template.render(self.api_vars)

        if debug:
            print("Render:")
            print(api_data_rendered)

        api_data_dic = self.template_format.load(api_data_rendered)

        if 'version' in api_data_dic:
            api_data_dic['version'] = str(api_data_dic['version'])

        return api_data_dic

    def _load_api_conf_directories(self):
        for key in self.folders:
            if not os.path.exists(self.folders[key]):
                raise GraviteeioError("Missing folder {}".format(self.folders[key]))

        root_template_file = None
        value_file = None

        if os.path.exists(self.files["value_file"]):
            value_file = self.files["value_file"]

        root_template_path_file = self.files["root_template_path_file"]
        for (data_format, extention) in ((data_format, extention) for data_format in TEMPLATE_FORMAT for extention in data_format.extentions):
            if not root_template_file and os.path.exists(root_template_path_file.format(extention)):
                self.template_format = data_format
                root_template_file = environments.APIM_API_TEMPLATE_FILE.format(extention)

            file = self.files["value_file"].format(extention)
            if not value_file and os.path.exists(file):
                value_file_format = data_format
                value_file = file

            if root_template_file and value_file:
                break

        self.template = self._get_template(root_template_file, self.folders["templates_folder"])

        try:
            with open(value_file, 'r') as f:
                api_value_string = f.read()
        except OSError:
            raise GraviteeioError("Cannot open file {}".format(value_file))

        self.api_vars = {}
        self.api_vars["Values"] = value_file_format.load(api_value_string)

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
                    self.api_vars[filename] = file_format.load(config_string)

        self.loaded_schema = True

    def _get_template(self, root_template_file, templates_folder):
        j2_env = Environment(loader=FileSystemLoader(templates_folder), trim_blocks=False, autoescape=False)
        filter_loader(j2_env)

        try:
            template = j2_env.get_template(root_template_file)
        except TemplateNotFound:
            raise GraviteeioError("Template not found, try to load {}".format(root_template_file))

        return template
