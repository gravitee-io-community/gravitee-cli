import enum
import re
from graviteeio_cli.lint.types.function_result import FunctionResult


class CasingType(enum.Enum):
    flat = '[a-z][a-z{__DIGITS__}]*'
    camel = '[a-z][a-z{__DIGITS__}]*(?:[A-Z{__DIGITS__}][a-z{__DIGITS__}]+)*'
    pascal = '[A-Z][a-z{__DIGITS__}]*(?:[A-Z{__DIGITS__}][a-z{__DIGITS__}]+)*'
    kebab = '[a-z][a-z{__DIGITS__}]*(?:-[a-z{__DIGITS__}]+)*'
    cobol = '[A-Z][A-Z{__DIGITS__}]*(?:-[A-Z{__DIGITS__}]+)*'
    snake = '[a-z][a-z{__DIGITS__}]*(?:_[a-z{__DIGITS__}]+)*'
    macro = '[A-Z][A-Z{__DIGITS__}]*(?:_[A-Z{__DIGITS__}]+)*'

    def __init__(self, value):
        self.pattern = value

    @staticmethod
    def value_of(value):
        for level in CasingType:
            if level.name == value:
                return level


def casing(value, **kwargs):
    results = []

    if value and (type(value) is not str or len(value) > 0) and "type" not in kwargs:
        return

    casingType = CasingType.value_of(kwargs["type"])

    if not casingType:
        return

    if not re.match(RegExp(casingType.pattern), value):
        results.append(FunctionResult("must be {} case".format(casingType)))

    return results


DIGITS_PATTERN = '0-9'


def RegExp(basePattern, disallowDigits=False):
    pattern = basePattern.replace("{__DIGITS__}", DIGITS_PATTERN if not disallowDigits else '')

    return "^{}$".format(pattern)


#   const separatorPattern = `[${escapeRegExp(overrides.separator.char)}]`;
#   const leadingSeparatorPattern = overrides.separator.allowLeading === true ? `${separatorPattern}?` : '';

#   return new RegExp(`^${leadingSeparatorPattern}${pattern}(?:${separatorPattern}${pattern})*$`);




#   if (
#     targetVal.length === 1 &&
#     opts.separator !== void 0 &&
#     opts.separator.allowLeading === true &&
#     targetVal === opts.separator.char
#   ) {
#     return;
#   }

#   const casingValidator = buildFrom(CASES[opts.type], opts);

#   if (casingValidator.test(targetVal)) {
#     return;
#   }

#   return [
#     {
#       message: `must be ${opts.type} case`,
#     },
#   ];
# };

