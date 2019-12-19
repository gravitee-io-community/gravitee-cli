import click, os, requests, time

from .... import environments


@click.command()
@click.option('--folder', help='Path to folder of templates', type=click.Path(exists=True), required=False)
@click.option('--upgrade', help='Upgrade api template', is_flag=False)
@click.argument('version')
@click.pass_obj
def init(folder, version, upgrade):
    """init api template according to api management version"""
    if upgrade:
        upgrade_exec()

    versions = requests.get(
        environments.APIM_API_URL_GITHUB_TEMPLATE_FOLDER + environments.APIM_API_TEMPLATE_VERSION_FILE)

    template_version = None
    versions_obj = versions.json()
    for version_r in versions_obj:
        version_split = version.split(".")
        if version_r == version_split[0] + "." + version_split[1]:
            template_version = versions_obj[version_r]
        if version_r == version:
            template_version = versions_obj[version_r]

    if not template_version:
        click.echo("Version {} is not managed".format(version))
        return

    r = requests.get(environments.APIM_API_URL_GITHUB_TEMPLATE_FOLDER + environments.APIM_API_TEMPLATE_MODEL.format(
        template_version), stream=True)

    if r.status_code != requests.codes.ok:
        click.echo('Unable to connect {0}'.format(
            environments.APIM_API_URL_GITHUB_TEMPLATE_FOLDER + environments.APIM_API_TEMPLATE_MODEL.format(
                template_version)))
        r.raise_for_status()
    total_size = int(r.headers.get('Content-Length'))

    if not folder:
        folder = environments.GRAVITEEIO_TEMPLATES_FOLDER

    if not os.path.exists(folder):
        os.mkdir(environments.GRAVITEEIO_TEMPLATES_FOLDER)

    template_file_path = "{}/{}".format(folder, environments.APIM_API_TEMPLATE_FILE)
    if not os.path.exists(template_file_path):
        if not upgrade:
            click.echo("Init api:")
        with click.progressbar(r.iter_content(1024), length=total_size) as bar, open(template_file_path, 'wb') as file:
            for chunk in bar:
                file.write(chunk)
                bar.update(len(chunk))
        click.echo(" - load template api {}".format(template_version))
    else:
        click.echo("Init file already exists")


def upgrade_exec(ctx, folder, version):
    """upgrade api template according to api management version"""
    if not folder: folder = environments.GRAVITEEIO_TEMPLATES_FOLDER

    template_file_path = "{}/{}".format(folder, environments.APIM_API_TEMPLATE_FILE)

    if not os.path.exists(template_file_path):
        click.echo("Not template api found")
        return
    click.echo("Upgraded template api:")
    os.rename(template_file_path, "{}/{}".format(folder, environments.APIM_API_TEMPLATE_MODEL.format(time.time())))
    click.echo(" - Rename old template api")
    # ctx.invoke(init, folder=folder, version=version, upgrade=True)