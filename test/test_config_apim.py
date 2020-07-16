import os
from graviteeio_cli.graviteeio.config import GraviteeioConfig, Auth_Type
from graviteeio_cli.graviteeio.modules import GraviteeioModule
from graviteeio_cli.environments import DEFAULT_APIM_ADDRESS_URL

FILE = "graviteeio.ini"

def test_init_config_file(tmpdir):
    d = tmpdir.mkdir("config")

    config_file = os.path.join( d.dirname, FILE )
    # apim = Graviteeio_Config_apim(config_file)
    gio_config = GraviteeioConfig(config_file)

    apim_config = gio_config.getGraviteeioConfig(GraviteeioModule.APIM)
    user = apim_config.get_authn_name()
    address_url = apim_config["address_url"]

    assert 'default' == gio_config.profile
    assert DEFAULT_APIM_ADDRESS_URL == address_url
    assert not os.path.isfile(config_file)
    # current_profile = demo
    # assert current_profile == 'current_profile = {}\n'.format(gio_config.profile)
    # assert apim_data == 'apim = {"address_url": "%s", authn_name": "%s", "authn_type": "%s"}\n' % (address_url, user, Auth_Type.CREDENTIAL.name.lower(), user, Auth_Type.CREDENTIAL.name.lower())


# def test_load_config_file(tmpdir):
#     d = tmpdir.mkdir("config")

#     config_file = os.path.join( d.dirname, FILE )
#     # apim = Graviteeio_Config_apim(config_file)
#     gio_config = GraviteeioConfig(config_file)
#     gio_config2 = GraviteeioConfig(config_file)

#     p = tmpdir.join(FILE)
#     current_profile = p.readlines()[1]
#     apim_data = p.readlines()[4]

#     apim_config = gio_config.getGraviteeioConfig(GraviteeioModule.APIM)
#     apim_config_data = gio_config.getGraviteeioConfigData(GraviteeioModule.APIM)
#     user = apim_config.get_authn_name()
#     address_url = apim_config_data["address_url"]
#     # current_profile = demo
#     assert current_profile == 'current_profile = {}\n'.format(gio_config.profile)
#     assert apim_data == 'apim = {"address_url": "%s", "active_auth": {"username": "%s", "type": "%s"}, "auth": [{"username": "%s", "type": "%s", "is_active": true}]}\n' % (address_url, user, Auth_Type.CREDENTIAL.name.lower(), user, Auth_Type.CREDENTIAL.name.lower())

def test_save(tmpdir):
    d = tmpdir.mkdir("config")

    config_file = os.path.join( d.dirname, FILE )
    gio_config = GraviteeioConfig(config_file)

    gio_config.save("test_profile", GraviteeioModule.APIM.name , user = "test", password = "test")

    p = tmpdir.join(FILE)
    new_profile = p.readlines()[7]
    new_value = p.readlines()[8]
    assert new_profile == '[test_profile]\n'
    assert new_value == 'apim = {"user": "test", "password": "test"}\n'

def test_save_and_change_value(tmpdir):
    d = tmpdir.mkdir("config")

    config_file = os.path.join( d.dirname, FILE )
    gio_config = GraviteeioConfig(config_file)

    gio_config.save("test_profile", GraviteeioModule.APIM.name , user = "test", password = "test")
    gio_config.save("test_profile", GraviteeioModule.APIM.name , user = "testtest", password = "test", toto = "toto")

    p = tmpdir.join(FILE)
    new_profile = p.readlines()[7]
    new_value = p.readlines()[8]
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

# def test_create_auth_load_auth(tmpdir):
#     d = tmpdir.mkdir("config")

#     config_file = os.path.join( d.dirname, FILE )
#     gio_config = GraviteeioConfig(config_file)


#     apim_config = gio_config.getGraviteeioConfig(GraviteeioModule.APIM)
#     auth_list = apim_config.get_auth_list()

#     user = "newuser"
    
#     auth_list.append({
#         "username": "newuser",
#         "type": Auth_Type.CREDENTIAL.name.lower(),
#         "is_active": False
#     })

#     apim_config.save(auth = auth_list)
#     print(apim_config.get_auth_list())

#     assert "[{'username': 'admin', 'type': 'credential', 'is_active': True}, {'username': 'newuser', 'type': 'credential', 'is_active': False}]" == "{}".format(apim_config.get_auth_list())

#     apim_config.load_auth("newuser")
#     active_user = apim_config.get_active_auth()["username"]
#     assert "[{'username': 'admin', 'type': 'credential', 'is_active': False, 'bearer': None}, {'username': 'newuser', 'type': 'credential', 'is_active': True}]" == "{}".format(apim_config.get_auth_list())
#     assert active_user == "newuser"

