def isOpenApiv2(document):
    result = False
    if type(document) is dict and 'swagger' in document:
        version = document["swagger"].split('.')
        if len(version) > 2:
            result = int(version[0]) == 2 and int(version[1]) == 0
        else:
            result = int(version[0]) == 2

    return result


def isOpenApiv3(document):
    result = False
    if type(document) is dict and 'openapi' in document:
        version = document["openapi"].split('.')
        if len(version) > 2:
            result = int(version[0]) == 3 and int(version[1]) == 0
        else:
            result = int(version[0]) == 3

    return result


def isOpenApiv3_1(document):
    result = False
    if type(document) is dict and 'openapi' in document:
        version = document["openapi"].split('.')
        if len(version) >= 2:
            result = int(version[0]) == 3 and int(version[1]) == 1

    return result
