import jsonpath_ng as jsonpath
from graviteeio_cli.lint.utils.path import convert_to_path_array


def test_convert_to_path_array():
    jsonpath_expr = jsonpath.parse('foo[*].baz')

    results = jsonpath_expr.find({'foo': [{'baz': 1}, {'baz': 2}]})

    validate = []
    for match in results:
        array = convert_to_path_array(match.full_path)
        print(array)
        validate.append(array)

    assert validate[0] == ['foo[0]', 'baz']
    assert validate[1] == ['foo[1]', 'baz']



def test_convert_to_path_array():
    jsonpath_expr = jsonpath.parse('foo.baz')

    results = jsonpath_expr.find({'foo': {'baz': 2}})

    validate = []
    for match in results:
        array = convert_to_path_array(match.full_path)
        print(array)
        validate.append(array)

    assert validate[0] == ['foo', 'baz']

# def test_jsonpath_ng():
#     jsonpath_expr = jsonpath.parse('foo[*].baz')

#     result = jsonpath_expr.find({'foo': [{'baz': 1}, {'baz': 2}]})

#     for match in result:
#         print("Result: ---")
#         print(match.value)
#         print("---")
#         print(match.full_path.left)
#         print("---")
#         print(match.full_path.right)
