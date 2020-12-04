import logging
from os import read
import tempfile
import click
import requests
import os
import time

from graviteeio_cli.core import file_format
from graviteeio_cli.core.output import OutputFormatType
from graviteeio_cli.lint.gio_linter import DiagSeverity, Gio_linter
from graviteeio_cli.lint.types.document import Document, DocumentType

logger = logging.getLogger("lint-service")


def validate_from_file(file_path: str, spec_string: str, document_type: DocumentType):
    spec = file_format.load_file(file_path.split("/")[-1], spec_string)

    return validate(spec, document_type)


def validate(spec, document_type: DocumentType):
    has_errors = False

    document = Document(spec, document_type)

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

    if has_errors > 0:
        has_errors = True

    return has_errors
