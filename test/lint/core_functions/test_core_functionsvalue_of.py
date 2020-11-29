from graviteeio_cli.lint.functions.value_of import value_of


def test_value_of():
    functionResult = value_of("foo", values=['foo', 2])
    assert len(functionResult) == 0

    functionResult = value_of(2, values=['foo', 2])
    assert len(functionResult) == 0

    functionResult = value_of("hello", values=['foo', 2])
    assert len(functionResult) == 1
