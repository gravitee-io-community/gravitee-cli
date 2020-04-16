import os
from graviteeio_cli.graviteeio.profile import GraviteeioConfig
from graviteeio_cli.environments import GraviteeioModule

FILE = "graviteeio.ini"

def test_init_config_file(tmpdir):
    d = tmpdir.mkdir("config")

    config_file = os.path.join( d.dirname, FILE )
    # apim = Graviteeio_Config_apim(config_file)
    gio_config = GraviteeioConfig(config_file)

    p = tmpdir.join(FILE)
    current_profile = p.readlines()[1]
    apim_data = p.readlines()[4]

    apim = gio_config.getGraviteeioConfigData(GraviteeioModule.APIM)
    user = apim["user"]
    password = apim["password"]
    address_url = apim["address_url"]
    # current_profile = demo
    assert current_profile == 'current_profile = {}\n'.format(gio_config.profile)
    assert apim_data == 'apim = {"user": "%s", "password": "%s", "address_url": "%s"}\n' % (user, password, address_url)

def test_load_config_file(tmpdir):
    d = tmpdir.mkdir("config")

    config_file = os.path.join( d.dirname, FILE )
    # apim = Graviteeio_Config_apim(config_file)
    gio_config = GraviteeioConfig(config_file)
    gio_config2 = GraviteeioConfig(config_file)

    p = tmpdir.join(FILE)
    current_profile = p.readlines()[1]
    apim_data = p.readlines()[4]

    apim = gio_config2.getGraviteeioConfigData(GraviteeioModule.APIM)
    user = apim["user"]
    password = apim["password"]
    address_url = apim["address_url"]
    # current_profile = demo
    assert current_profile == 'current_profile = {}\n'.format(gio_config.profile)
    assert apim_data == 'apim = {"user": "%s", "password": "%s", "address_url": "%s"}\n' % (user, password, address_url)

def test_save(tmpdir):
    d = tmpdir.mkdir("config")

    config_file = os.path.join( d.dirname, FILE )
    gio_config = GraviteeioConfig(config_file)

    gio_config.save("test_profile", GraviteeioModule.APIM.name , user = "test", password = "test")

    p = tmpdir.join(FILE)
    new_profile = p.readlines()[6]
    new_value = p.readlines()[7]
    assert new_profile == '[test_profile]\n'
    assert new_value == 'apim = {"user": "test", "password": "test"}\n'

def test_save_and_change_value(tmpdir):
    d = tmpdir.mkdir("config")

    config_file = os.path.join( d.dirname, FILE )
    gio_config = GraviteeioConfig(config_file)

    gio_config.save("test_profile", GraviteeioModule.APIM.name , user = "test", password = "test")
    gio_config.save("test_profile", GraviteeioModule.APIM.name , user = "testtest", password = "test", toto = "toto")

    p = tmpdir.join(FILE)
    new_profile = p.readlines()[6]
    new_value = p.readlines()[7]
    assert new_profile == '[test_profile]\n'
    assert new_value == 'apim = {"user": "testtest", "password": "test", "toto": "toto"}\n'

def test_save_and_load(tmpdir):
    d = tmpdir.mkdir("config")

    config_file = os.path.join( d.dirname, FILE )
    gio_config = GraviteeioConfig(config_file)

    gio_config.save("test_profile", GraviteeioModule.APIM.name, user = "test", password = "test", address_url = "https://demo.gravitee.io")
    gio_config.load("test_profile")

    apim = gio_config.getGraviteeioConfigData(GraviteeioModule.APIM)
    assert 'test_profile' == gio_config.profile
    assert 'test' == apim['user']
