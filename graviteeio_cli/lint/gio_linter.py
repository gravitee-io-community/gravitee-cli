import logging

import jsonpath_ng as jsonpath
from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.lint.functions.CoreFunctions import CoreFunctions
from graviteeio_cli.lint.rulesets.oas.oas_rules import oas_rules
from graviteeio_cli.lint.rulesets.gio_apim.gio_apim_rules import gio_apim_rules
from graviteeio_cli.lint.types.document import Document
from graviteeio_cli.lint.types.enums import DiagSeverity
from graviteeio_cli.lint.types.rule import Rule
from graviteeio_cli.lint.types.validator import Validator
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

        self.setFunctions(CoreFunctions)
        self.setRulesets(ruleSets)

    # def loadRuleset():
    #     pass
    def setFunctions(self, functions):
        for function in functions:
            self.setFunction(function)

    def setFunction(self, function):
        self.functions[function.__name__] = function

    def setRules(self, rules):
        for name, rule in rules.items():
            logger.info("Load ruleSet {}".format(name))

            if "validator" not in rule:
                raise GraviteeioError("Error loading ruleset. No [{}] found for rule [{}]".format("validator", name))
            elif "func" not in rule["validator"]:
                raise GraviteeioError("Error loading ruleset. No [{}] found for rule [{}]".format("validator.func", name))

            if not rule["validator"]["func"] in self.functions:
                logger.warning("Rule {} is not applied. Not validator [{}] found.".format(name, rule["validator"]["func"]))
                continue

            self.rules[name] = Rule(
                name,
                Validator(
                    self.functions[rule["validator"]["func"]],
                    rule["validator"]["args"] if "args" in rule["validator"] else None
                ),
                **rule
            )

    def setRuleset(self, ruleSet):
        if "functions" in ruleSet:
            self.setFunctions(ruleSet["functions"])

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
                    target_values = target["value"]
                    values = []

                    if rule.field and rule.field != '@key' and target_values and rule.field in target_values:
                        values.append(target_values[rule.field])
                    elif rule.field and rule.field == '@key':
                        values.extend(target_values.keys())
                    elif rule.field:
                        values.append(None)
                    else:
                        values.append(target_values)

                    for value in values:
                        if rule.validator.args:
                            results = rule.validator.func(value, **rule.validator.args)
                        else:
                            results = rule.validator.func(value)

                        if rule.field and rule.field == '@key':
                            field = value
                        else:
                            field = rule.field
                        toReturn.extend(self._processTargetResults(results, rule, target["path"], field))

        return toReturn

    def _processTargetResults(self, results, rule, target_path, field):
        toReturn = []
        if not results:
            return toReturn

        for result in results:
            path = result.path
            if not path:
                path = target_path
                if field and path:
                    newpath = []
                    newpath.extend(target_path)
                    if field:
                        newpath.append(field)
                    path = newpath

            result_message = None
            if result.message:
                if path and len(path) > 0:
                    result_message = result.message.replace("{", "{{").replace("}", "}}")
                    result_message = result_message.format(field="path[-1]")
                else:
                    result_message = result.message

            message = rule.message.format(
                error=result_message,
                path=printPath(path) if path else "",
                field=field)

            toReturn.append(
                DiagResult(
                    rule.severity, path, message, rule.name, rule.type
                )
            )

        return toReturn

    def _getLintTargets(self, value, rule):
        targets = []

        if not rule.query:
            targets.append({
                "path": [],
                "value": value
            })
        else:
            expression = jsonpath.parse(rule.query)
            values = expression.find(value)
            for value in values:
                targets.append({
                    "path": convert_to_path_array(value.full_path),
                    "value": value.value
                })

            if len(values) == 0:
                targets.append({
                    "path": [],
                    "value": None
                })

        return targets
