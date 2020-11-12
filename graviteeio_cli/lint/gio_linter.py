import logging

import jsonpath_ng as jsonpath
from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.lint.functions.CoreFunctions import CoreFunctions
from graviteeio_cli.lint.rulesets.oas.oas_rules import oas_rules
from graviteeio_cli.lint.rulesets.gio_apim.gio_apim_rules import gio_apim_rules
from graviteeio_cli.lint.types.document import Document
from graviteeio_cli.lint.types.enums import DiagSeverity
from graviteeio_cli.lint.types.rule import Rule
from graviteeio_cli.lint.utils.path import printPath, convert_to_path_array

logger = logging.getLogger("lint.gio_linter")


class DiagResult:

    def __init__(self, severity: DiagSeverity, path: str, message: str, rule_name: str, type=None):
        super().__init__()
        self.position = None
        self.severity = severity
        self.path = path
        self.message = message
        self.rule_name = rule_name
        self.type = None


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

    def setRules(self, rules):
        for name, rule in rules.items():
            logger.info("Load ruleSet {}".format(name))

            rule_params_required = ["validator", "severity", "formats", "description"]

            for param in rule_params_required:
                if param not in rule:
                    raise GraviteeioError("Error loading rulset. No [{}] found for rule [{}]".format(param, name))

            if not rule["validator"] in self.functions:
                logger.warning("Rule {} is not applied. Not validator [{}] found.".format(name, rule["validator"]))
                continue

            rule_params = ["selector", "validator", "validator_args", "formats", "description", "description", "type", "field", "message"]
            rule_params_values = {}

            for param in rule_params:
                rule_params_values[param] = None
                if param in rule:
                    rule_params_values[param] = rule[param]

            if "message" not in rule:
                rule_params_values["message"] = rule_params_values["description"]

            self.rules[name] = Rule(
                name,
                rule_params_values["description"],
                rule_params_values["type"],
                rule_params_values["message"],
                DiagSeverity.value_of(rule["severity"]),
                rule_params_values["formats"],
                rule_params_values["selector"],
                rule_params_values["field"],
                self.functions[rule_params_values["validator"]],
                rule_params_values["validator_args"]
            )

    def setRuleset(self, ruleSet):
        if "functions" in ruleSet:
            self.setValidators(ruleSet["functions"])

        self.setRules(ruleSet["rules"])

    def setRulesets(self, ruleSets):
        for ruleSet in ruleSets:
            self.setRuleset(ruleSet)

    def run(self, document: Document):
        toReturn = []

        # sort rule by selector
        for rule in self.rules.values():
            if document.is_format_in(rule.formats):
                targets = self._getLintTargets(document.values, rule)

                for target in targets:
                    value = target["value"]
                    if rule.field and rule.field in value:
                        value = value[rule.field]
                    elif rule.field:
                        value = None

                    results = rule.validator(value, **rule.args)
                    toReturn.extend(self._processTargetResults(results, rule, target["path"], rule.field))

        return toReturn

    def _processTargetResults(self, results, rule, target_path, field):
        toReturn = []

        for result in results:
            path = result.path
            if not path and field is not None:
                path = target_path
                if field and path:
                    newpath = []
                    newpath.extend(target_path)
                    newpath.append(field)
                    path = newpath

            message = rule.message.format(error=result.message, path=printPath(path))

            toReturn.append(
                DiagResult(
                    rule.severity, path, message, rule.name, rule.type
                )
            )

        return toReturn

    def _getLintTargets(self, value, rule):
        targets = []

        if not rule.selector:
            targets.append({
                "path": [],
                "value": value
            })
        else:
            expression = jsonpath.parse(rule.selector)
            values = expression.find(value)
            for value in values:
                targets.append({
                    "path": convert_to_path_array(value.full_path),
                    "value": value.value
                })

        return targets
