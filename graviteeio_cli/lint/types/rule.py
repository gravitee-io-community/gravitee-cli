class Rule:
    def __init__(
        self,
        name,
        description,
        rule_type,
        message,
        severity,
        formats,
        selector,
        field,
        validator,
        args
    ):

        super().__init__()
        self.name = name
        self.description = description
        self.type = rule_type
        self.message = message

        self.formats = formats
        self.severity = severity
        self.selector = selector
        self.field = field
        self.validator = validator
        self.args = args



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