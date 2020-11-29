import re
from re import RegexFlag

# p = re.compile('[a-z]+')
from graviteeio_cli.lint.types.function_result import FunctionResult

CACHE = {}


def findFlag(value):
    # if value in RegexFlag:
    try:
        return RegexFlag[value.upper()]
    except Exception:
        return None


def getFromCache(pattern: str, flag: RegexFlag = None):
    key = pattern if not flag else pattern + "_" + flag.name

    if key in CACHE:
        return CACHE[key]
    else:
        p = re.compile(pattern, flag) if flag else re.compile(pattern)
        CACHE[key] = p
        return p


def pattern(value, **kwargs):
    results = []
    match = None
    match_flag = None

    notMatch = None
    notMatch_flag = None

    if "match" in kwargs and type(kwargs["match"]) is str:
        match = kwargs["match"]
        if "match_flag" in kwargs:
            match_flag = findFlag(kwargs["match_flag"])

    if "notMatch" in kwargs and type(kwargs["notMatch"]) is str:
        notMatch = kwargs["notMatch"]
        if "notMatch_flag" in kwargs:
            notMatch_flag = findFlag(kwargs["notMatch_flag"])

    if match:
        p = getFromCache(match, match_flag)

        if not p.match(value):
            results.append(
                FunctionResult("must match the pattern {}".format(match))
            )

    if notMatch:
        p = getFromCache(notMatch, notMatch_flag)

        if p.match(value):
            results.append(
                FunctionResult("must not match the pattern {}".format(notMatch))
            )

    return results
