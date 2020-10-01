import os
from graviteeio_cli.core.config import GraviteeioConfig
from graviteeio_cli.modules.gio_module import GioModule
from graviteeio_cli.environments import DEFAULT_APIM_ADDRESS_URL

FILE = "graviteeio.ini"


def test_init_config_file(tmpdir):
    d = tmpdir.mkdir("config")

    config_file = os.path.join(d.dirname, FILE)
    # apim = Graviteeio_Config_apim(config_file)
    gio_config = GraviteeioConfig(config_file)

    apim_config = gio_config.getGraviteeioConfig(GioModule.APIM)
    # user = apim_config.get_authn_name()
    address_url = apim_config["address_url"]

    assert 'default' == gio_config.profile
    assert DEFAULT_APIM_ADDRESS_URL == address_url
    assert not os.path.isfile(config_file)


def test_save(tmpdir):
    d = tmpdir.mkdir("config")

    config_file = os.path.join(d.dirname, FILE)
    gio_config = GraviteeioConfig(config_file)

    gio_config.save("test_profile", GioModule.APIM.name, user="test", password="test")

    p = tmpdir.join(FILE)
    new_profile = p.readlines()[7]
    new_value = p.readlines()[8]
    assert new_profile == '[test_profile]\n'
    assert new_value == 'apim = {"user": "test", "password": "test"}\n'


def test_save_and_change_value(tmpdir):
    d = tmpdir.mkdir("config")

    config_file = os.path.join(d.dirname, FILE)
    gio_config = GraviteeioConfig(config_file)

    gio_config.save("test_profile", GioModule.APIM.name, user="test", password="test")
    gio_config.save("test_profile", GioModule.APIM.name, user="testtest", password="test", toto="toto")

    p = tmpdir.join(FILE)
    new_profile = p.readlines()[7]
    new_value = p.readlines()[8]
    assert new_profile == '[test_profile]\n'
    assert new_value == 'apim = {"user": "testtest", "password": "test", "toto": "toto"}\n'


def test_save_and_load(tmpdir):
    d = tmpdir.mkdir("config")

    config_file = os.path.join(d.dirname, FILE)
    gio_config = GraviteeioConfig(config_file)

    gio_config.save("test_profile", GioModule.APIM.name, user="test", password="test", address_url="https://demo.gravitee.io")
    gio_config.load("test_profile")

    apim = gio_config.getGraviteeioConfigData(GioModule.APIM)
    assert 'test_profile' == gio_config.profile
    assert 'test' == apim['user']
