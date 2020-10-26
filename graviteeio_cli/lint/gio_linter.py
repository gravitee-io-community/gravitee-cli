import logging

import jmespath
from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.lint.functions.CoreFunctions import CoreFunctions
from graviteeio_cli.lint.rulesets.default_rules import oas_rules
from graviteeio_cli.lint.rulesets.gio_apim.gio_apim_rules import gio_apim_rules
from graviteeio_cli.lint.rulesets.oas.oas_rules import oas_rules
from graviteeio_cli.lint.types.document import Document
from graviteeio_cli.lint.types.enums import DiagSeverity
from graviteeio_cli.lint.types.rule import Rule

logger = logging.getLogger("lint.gio_linter")


class DiagResult:

    def __init__(self, severity: DiagSeverity, path: str, message: str, rule_name: str):
        super().__init__()
        self.position = None
        self.severity = severity
        self.path = path
        self.message = message
        self.rule_name= rule_name


class Gio_linter:

    def __init__(self):

        ruleSets = [oas_rules, gio_apim_rules]

        self.functions = {}
        self.rules = {}

        self.setValidators(CoreFunctions)
        self.setRulesets(ruleSets)

    # def loadRuleset():
    #     pass
    def setValidators(self, functions):
        for function in functions:
            self.setValidator(function)

    def setValidator(self, function):
        self.functions[function.__name__] = function

    def setRuleset(self, ruleSet):
        if "functions" in ruleSet:
            self.setValidators(ruleSet["functions"])

        for name, rule in ruleSet["rules"].items():
            logger.info("Load ruleSet {}".format(name))

            if "validator" not in rule:
                raise GraviteeioError("Error loading rulset. No [validator] found for rule [{}]".format(name))

            if "severity" not in rule:
                raise GraviteeioError("Error loading rulset. No [severity] found for rule [{}]".format(name))

            if "formats" not in rule:
                raise GraviteeioError("Error loading rulset. No [formats] found for rule [{}]".format(name))

            if "message" not in rule:
                raise GraviteeioError("Error loading rulset. No [message] found for rule [{}]".format(name))

            selector = None
            if "selector" in rule:
                selector = rule["selector"]

            validator_args = None
            if "validator_args" in rule:
                validator_args = rule["validator_args"]

            description = None
            if "description" in rule:
                description = rule["description"]

            if not rule["validator"] in self.functions:
                logger.warning("Rule {} is not applied. Not validator [{}] found.".format(name, rule["validator"]))
                continue

            self.rules[name] = Rule(
                name,
                description,
                rule["message"],
                DiagSeverity.value_of(rule["severity"]),
                rule["formats"],
                selector,
                self.functions[rule["validator"]],
                validator_args
            )

    def setRulesets(self, ruleSets):
        for ruleSet in ruleSets:
            self.setRuleset(ruleSet)

    def run(self, document: Document):
        toReturn = []

        # sort rule by selector
        for rule in self.rules.values():
            selector = None
            if not rule.selector:
                selector = document.values
            else:
                selector = jmespath.search(selector, document.values)
            # selector = rule.selector
            if document.is_format_in(rule.formats):
                errors = rule.validator(selector, **rule.args)
                toReturn = self.processTargetResults(errors, rule)

        return toReturn

    def processTargetResults(self, errors, rule):
        toReturn = []

        for error in errors:
            message = rule.message.format(error=error.message, path=error.printPath())

            toReturn.append(
                DiagResult(
                    rule.severity, error.printPath(), message, rule.name
                )
            )

        return toReturn
