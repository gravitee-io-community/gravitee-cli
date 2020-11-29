from graviteeio_cli.lint.functions.starts_with import starts_with


def test_start_with():
    functionResult = starts_with("https://www.test.com", str="https")
    assert len(functionResult) == 0

    functionResult = starts_with("http://www.test.com", str="https")
    assert len(functionResult) == 1
