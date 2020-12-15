from graviteeio_cli.exeptions import GraviteeioError
import logging
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


def _load_ruleset_from_path(ruleset_path, linter):
    ruleset_str = None

    logger.info("Loading ruleset [{}]".format(ruleset_path.split("/")[-1]))
    try:
        with open(ruleset_path, "r") as file_obj:
            ruleset_str = file_obj.read()
    except Exception:
        click.echo(click.style("Warning: error to get ruleset with path [{}]".format(ruleset_path), fg="green"))

    if ruleset_str:
        ruleset = file_format.load_file(ruleset_path.split("/")[-1], ruleset_str)
        linter.setRuleset(ruleset)


def _load_ruleset_from_url(ruleset_url, ttl, linter):
    tempdir = tempfile.gettempdir()

    file_name = ruleset_url.split("/")[-1]
    temp_path = "{}/{}".format(tempdir, file_name)

    load_ruleset = True

    if os.path.isfile(temp_path):
        delta_time = time.time() - os.path.getmtime(temp_path)

        with open(temp_path, "r") as file_obj:
            ruleset_str = file_obj.read()

        if delta_time < ttl * 60:
            load_ruleset = False

    ruleset_str = None
    if load_ruleset:
        logger.info("Loading ruleset [{}]".format(ruleset_url.split("/")[-1]))
        try:
            ruleset_str = requests.get(ruleset_url).text
            with open(temp_path, "wt") as file_obj:
                file_obj.write(ruleset_str)
        except Exception:
            click.echo(click.style("Warning: error to get ruleset with url [{}]".format(ruleset_url), fg="green"))

    if ruleset_str:
        ruleset = file_format.load_file(ruleset_url.split("/")[-1], ruleset_str)
        try:
            linter.setRuleset(ruleset)
        except Exception as e:
            os.remove(temp_path)
            raise GraviteeioError(e.message)


def load_ruleset(linter, ruleset_files, ttl):
    if not ruleset_files:
        return

    for ruleset_file in ruleset_files:
        if ruleset_file.startswith("http://") or ruleset_file.startswith("https://"):
            _load_ruleset_from_url(ruleset_file, ttl, linter)
        else:
            _load_ruleset_from_path(ruleset_file, linter)


def validate_from_file(file_path: str, spec_string: str, document_type: DocumentType, linter_conf=None):
    spec = file_format.load_file(file_path.split("/")[-1], spec_string)

    return validate(spec, document_type, linter_conf)


def validate(spec, document_type: DocumentType, linter_conf=None, display_summary=False):
    is_valide = True

    document = Document(spec, document_type)

    linter = Gio_linter()
    if linter_conf:
        ruleset_files = linter_conf["ruleset_files"]
        ruleset_ttl = linter_conf["ruleset_ttl"]
        if ruleset_files and len(ruleset_files) > 0:
            load_ruleset(linter, ruleset_files, ruleset_ttl)

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

    if results:
        OutputFormatType.TABLE.echo(results, inner_heading_row_border=False)

    if display_summary:
        click.echo(click.style("\n Summary: errors({}), warnings({}), infos({})".format(nb_errors, nb_warning, nb_infos), fg="green"))

    if nb_errors > 0:
        is_valide = False

    return is_valide
