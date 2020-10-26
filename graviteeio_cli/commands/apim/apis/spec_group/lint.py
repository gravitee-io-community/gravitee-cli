import logging
import click
from graviteeio_cli.core.output import OutputFormatType
from graviteeio_cli.lint.gio_linter import DiagSeverity, Gio_linter
from graviteeio_cli.lint.types.document import Document, DocumentType
from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.core.file_format import load_file
# from graviteeio_cli.http_client.apim.api import ApiClient


logger = logging.getLogger("command-apim-spec-lint")


@click.command(short_help="Check format of api definition configuration generated.")
@click.option('--api', 'api_id',
              help='API id',
              required=False)
@click.option('--file', '-f', type=click.Path(exists=True), required=True,
              help="Spec file (Swagger 2.0 / OAS 3.0)")
@click.pass_obj
def lint(obj, api_id, file):
    """This command allow to run a serie of tests to verify that api specification is correctly formed."""

    try:
        with open(file, 'r') as f:
            api_spec = f.read()
    except FileNotFoundError:
        raise GraviteeioError("Missing values file {}".format(file))

    oas = load_file(file.split("/")[-1], api_spec)

    document = Document(oas, DocumentType.oas)

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
        line_result.append(display_diag_severity.get(error.severity) + ":")
        line_result.append(error.rule_name)
        # line_result.append(error.path)
        line_result.append(error.message)

        results.append(line_result)

        if error.severity == DiagSeverity.Error:
            nb_errors = nb_errors + 1
        elif error.severity == DiagSeverity.Warn:
            nb_warning = nb_warning + 1
        elif error.severity == DiagSeverity.Info:
            nb_infos = nb_infos + 1

    OutputFormatType.TABLE.echo(results, inner_heading_row_border=False)

    click.echo(click.style("\n Summary: errors({}), warnings({}), infos({})".format(nb_errors, nb_warning, nb_infos), fg="green"))
