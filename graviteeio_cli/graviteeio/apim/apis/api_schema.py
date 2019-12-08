import yaml
from jinja2 import TemplateNotFound, Environment, FileSystemLoader
from graviteeio_cli.exeptions import GraviteeioError
from .... import environments
from . import utils


class ApiSchema:

    def __init__(self, folder_path, value_file):
        self.j2_env = Environment(loader=FileSystemLoader(folder_path), trim_blocks=False)
        try:
            with open(value_file, 'r') as f:
                api_value_string = f.read()
        except FileNotFoundError:
            raise GraviteeioError("No such file {}".format(value_file))

        self.api_value_data = yaml.load(api_value_string, Loader=yaml.SafeLoader)

    def get_api_data(self, debug, set_values):

        try:
            template = self.j2_env.get_template(environments.APIM_API_TEMPLATE_FILE)
        except TemplateNotFound:
            raise GraviteeioError("Template {} not found".format(environments.APIM_API_TEMPLATE_FILE))

        for set_value in set_values:
            self.api_value_data = utils.update_dic_with_set(set_value, self.api_value_data)

        api_data_yaml = template.render(api=self.api_value_data, config={})

        if debug:
            print("YAML:")
            print(api_data_yaml)

        api_data_dic = yaml.load(api_data_yaml, Loader=yaml.SafeLoader)

        if 'version' in api_data_dic:
            api_data_dic['version'] = str(api_data_dic['version'])

        return api_data_dic
