from jsonpath_ng import Fields, Child
from jsonpath_ng.jsonpath import Index


def printPath(path, pointer="."):
    return pointer.join(path)


def convert_to_path_array(current_path):

    def inner_convert(current_path, path_array=[]):
        if type(current_path.right) is Fields:
            path_array.append(current_path.right.fields[0])

        if type(current_path.left) is Child:
            inner_convert(current_path.left, path_array)
        elif type(current_path.left) is Fields and type(current_path.right) is Index:
            path_array.append("{}[{}]".format(current_path.left.fields[0], str(current_path.right.index)))
        elif type(current_path.left) is Fields:
            path_array.append(current_path.left.fields[0])

        return path_array

    toReturn = inner_convert(current_path, [])
    toReturn.reverse()
    return toReturn
