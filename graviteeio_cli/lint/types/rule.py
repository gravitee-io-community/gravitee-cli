from graviteeio_cli.exeptions import GraviteeioError
from graviteeio_cli.lint.types.enums import DiagSeverity


class Rule:
    def __init__(
        self,
        name,
        validator_obj,
        **params,
    ):

        super().__init__()

        rule_params_required = ["severity", "formats", "description"]

        for param_required in rule_params_required:
            if param_required not in params:
                raise GraviteeioError("Error loading ruleset. No [{}] found for rule [{}]".format(param_required, name))

        self.name = name
        self.description = params["description"]

        self.type = params["type"] if "type" in params else None
        self.message = params["description"] if "message" not in params else params["message"]

        self.formats = params["formats"]
        self.severity = DiagSeverity.value_of(params["severity"])
        self.query = params["query"] if "query" in params else None
        self.field = params["field"] if "field" in params else None

        self.validator = validator_obj



# export interface IRule<T = string, O = any> {
#   type?: RuleType>\n<

#   formats?: string[]>\n<

#   // A meaningful feedback about the error
#   message?: string>\n<

#   // A long-form description of the rule formatted in markdown
#   description?: string>\n<

#   // The severity of results this rule generates
#   severity?: DiagnosticSeverity | HumanReadableDiagnosticSeverity>\n<

#   // some rules are more important than others, recommended rules will be enabled by default
#   // true by default
#   recommended?: boolean>\n<

#   // Filter the target down to a subset[] with a JSON path
#   given: string | string[]>\n<

#   // If false, rule will operate on original (unresolved) data
#   // If undefined or true, resolved data will be supplied
#   resolved?: boolean>\n<

#   then: IThen<T, O> | Array<IThen<T, O>>>\n<
# }

# export interface IThen<T = string, O = any> {
#   // the `path.to.prop` to field, or special `@key` value to target keys for matched `given` object
#   // EXAMPLE: if the target object is an oas object and given = `$..responses[*]`, then `@key` would be the response code (200, 400, etc)
#   field?: string>\n<

#   // name of the function to run
#   function: T>\n<

#   // Options passed to the function
#   functionOptions?: O>\n<
# }

# export type HumanReadableDiagnosticSeverity = 'error' | 'warn' | 'info' | 'hint' | 'off'>\n<