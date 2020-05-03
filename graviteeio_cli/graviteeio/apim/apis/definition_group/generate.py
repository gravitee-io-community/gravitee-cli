import logging
import os

import click

from ..utils import filter_api_values
from .api_schema import ApiSchema, Data_Template_Format

logger = logging.getLogger("command-generate")

@click.command()
@click.option('--config-path', type=click.Path(exists=False), required=False, default="./",
              help="Config folder")
@click.option('--format', 
              default="yaml",
              help='Generated format. Default: `yaml`',
              type=click.Choice(Data_Template_Format.list_name(), case_sensitive=False))
@click.option('--from-id', 
              help='generate skeleton from existing api', required=False)
@click.pass_obj
def generate(obj, config_path, output, from_id):
    """Generate skeleton template exemple to create or update api"""
    if not os.path.exists(config_path):
        os.mkdir(config_path)

    api_def_string = None
    if from_id:
        api_client = obj['api_client']
        api_def_string = api_client.get_export(from_id).json()
        filter_api_values(api_def_string)

    apischema = ApiSchema(config_path)
    apischema.generate_schema(format = Data_Template_Format.value_of(output), api_def = api_def_string)


# @click.command()
# @click.option('--template-folder', help='Path for folder of templates', type=click.Path(exists=False), required=False, default=environments.GRAVITEEIO_TEMPLATES_FOLDER)
# @click.option('--upgrade', help='Upgrade api template', is_flag=True)
# @click.option('--value-from', help='Generate value file from Id of existing API configuration')
# @click.argument('version')
# @click.pass_obj
# def init(obj, template_folder, upgrade, value_from, version):
#     """init api download a default template according to api management version"""

#     folder= template_folder

#     logger.debug("folder {}".format(os.path.abspath(folder)))

#     if not os.path.exists(folder):
#         os.mkdir(folder)
#     elif os.path.exists(folder) and os.path.isfile(folder):
#         raise GraviteeioError("{}: File exists".format(folder))

#     if upgrade:
#         upgrade_exec(folder)

#     template_version = get_template_version(version)

#     if not template_version:
#         click.echo("Version {} is not managed".format(version))
#         return

#     r = requests.get(environments.APIM_API_URL_GITHUB_TEMPLATE_FOLDER + environments.APIM_API_TEMPLATE_MODEL.format(
#         template_version), stream=True)

#     if r.status_code != requests.codes.ok:
#         raise GraviteeioRequestError(msg = 'Unable to connect {0}'.format(
#             environments.APIM_API_URL_GITHUB_TEMPLATE_FOLDER + environments.APIM_API_TEMPLATE_MODEL.format(
#                 template_version)), error_code = r.status_code )

#     total_size = int(r.headers.get('Content-Length'))

#     template_file_path = "{}/{}".format(folder, environments.APIM_API_TEMPLATE_FILE)
#     if not os.path.exists(template_file_path):
#         if not upgrade:
#             click.echo("Init template api:")
#         with click.progressbar(r.iter_content(1024), length=total_size) as bar, open(template_file_path, 'wb') as file:
#             for chunk in bar:
#                 file.write(chunk)
#                 bar.update(len(chunk))
#         click.echo(" - load template api {}".format(template_version))
#     else:
#         click.echo("Template file already exists")

#     if value_from:
#         value_file_path = "{}/{}".format(folder, environments.APIM_API_VALUE_FILE_NAME)
#         if not os.path.exists(value_file_path):
#             api_client = obj['api_client']
#             api_json = api_client.get(value_from).json()
#             filter_api_values(api_json)
#             filter_with_tempate_rule(api_json)
#             api_yaml= yaml.dump(api_json)
            
#             click.echo("Value file generated")
#             with open(value_file_path, 'w') as file:
#                 file.write(api_yaml)
#         else:
#             GraviteeioRequestError(msg = 'Value file {} already exists'.format(value_file_path))


# def upgrade_exec(folder):
#     """upgrade api template according to api management version"""

#     template_file_path = "{}/{}".format(folder, environments.APIM_API_TEMPLATE_FILE)

#     if not os.path.exists(template_file_path):
#         click.echo("Not template api found")
#         return
#     click.echo("Upgraded template api:")
#     os.rename(template_file_path, "{}/{}".format(folder, environments.APIM_API_TEMPLATE_MODEL.format(time.time())))
#     click.echo(" - Rename old template api")
#     # ctx.invoke(init, folder=folder, version=version, upgrade=True)

# def get_template_version(version):
#     versions = requests.get(
#             environments.APIM_API_URL_GITHUB_TEMPLATE_FOLDER + environments.APIM_API_TEMPLATE_VERSION_FILE)

#     logger.debug("text versions {}".format(versions.text))

#     template_version = None
#     versions_obj = versions.json()

#     logger.debug("json versions {}".format(versions_obj))

#     for version_r in versions_obj:
#         version_split = version.split(".")
#         if version_r == version_split[0] + "." + version_split[1]:
#             template_version = versions_obj[version_r]
#         if version_r == version:
#             template_version = versions_obj[version_r]
    
#     return template_version

# def filter_with_tempate_rule(yaml_dictionary):
#     for group in yaml_dictionary['proxy']['groups']:
#         if 'proxy' in group and not group['proxy']['enabled']:
#             del group['proxy']
