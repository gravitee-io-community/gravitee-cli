from graviteeio_cli.graviteeio.utils import is_uri_valid

def test_url_valid():
    url_1='https://gravitee.io/'
    url_2='http://gravitee.io/'
    url_3='http://gravitee.io'
    url_4='http://gravitee.io:80'

    assert is_uri_valid(url_1)
    assert is_uri_valid(url_2)
    assert is_uri_valid(url_3)
    assert is_uri_valid(url_4)

def test_url_not_valid():
    url_1='gravitee.io'
    url_2='http:/gravitee.io/'
    # url_3='http://gravitee'
    url_4='gravitee.io:80'

    assert not is_uri_valid(url_1)
    assert not is_uri_valid(url_2)
    # assert not is_uri_valid(url_3)
    assert not is_uri_valid(url_4)
