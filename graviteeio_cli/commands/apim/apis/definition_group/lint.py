import logging

import click
from graviteeio_cli.core.output import OutputFormatType
from graviteeio_cli.lint.gio_linter import DiagSeverity, Gio_linter
from graviteeio_cli.lint.types.document import Document, DocumentType
# from graviteeio_cli.graviteeio.utils import filter_api_values
from graviteeio_cli.resolvers.api_conf_resolver import ApiConfigResolver

# from graviteeio_cli.http_client.apim.api import ApiClient


logger = logging.getLogger("command-apim-def-lint")


@click.command(short_help="Check format of api definition configuration generated.")
@click.option(
    '--def-path', 'config_path', default=".",
    type=click.Path(exists=False),
    required=False,
    help="Path where api definition is generated. The default value is the current directory"
)
@click.option(
    '--file', '-f',
    type=click.Path(exists=True), required=False,
    help="Value file"
)
@click.option(
    '--set', '-s', multiple=True,
    help="Overload the value(s) of value file eg: `--set proxy.groups[0].name=mynewtest`"
)
@click.pass_obj
def lint(obj, config_path, file, set):
    """This command allow to run a serie of tests to verify that api definition configuration is correctly formed."""

    api_resolver = ApiConfigResolver(config_path, file)
    api_def_config = api_resolver.get_api_data(debug=False, set_values=set)

    document = Document(api_def_config, DocumentType.gio_apim)

    linter = Gio_linter()
    diagResults = linter.run(document)

    display_diag_severity = {
        DiagSeverity.Error: click.style('Error', fg='red'),
        DiagSeverity.Warn: click.style('Warning', fg='yellow'),
        DiagSeverity.Info: click.style('Info', fg='blue'),
        DiagSeverity.Hint: click.style('Hint', fg='magenta')
    }

    results = []
    nb_errors = 0
    nb_warning = 0
    nb_infos = 0
    for error in diagResults:
        line_result = []
        line_result.append(display_diag_severity.get(error.severity))
        line_result.append(error.rule_name)
        line_result.append(error.message)
        # line_result.append(error.path)

        results.append(line_result)

        if error.severity == DiagSeverity.Error:
            nb_errors = nb_errors + 1
        elif error.severity == DiagSeverity.Warn:
            nb_warning = nb_warning + 1
        elif error.severity == DiagSeverity.Info:
            nb_infos = nb_infos + 1

    OutputFormatType.TABLE.echo(results, inner_heading_row_border=False)

    click.echo(click.style("\n Summary: errors({}), warnings({}), infos({})".format(nb_errors, nb_warning, nb_infos), fg="green"))
