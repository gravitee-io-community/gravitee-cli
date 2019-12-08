import click, os
import pytest
from click.testing import CliRunner
from graviteeio_cli.cli import main
import graviteeio_cli.environments as env
from graviteeio_cli.graviteeio.config import GraviteeioConfiguration, GraviteeioModule


def test_create_config_file():
    runner = CliRunner()

    with runner.isolated_filesystem():

        result = runner.invoke(main, ['config','--user','test'])

        with open(env.GRAVITEEIO_CONF_FILE) as file:
            lineUser = file.readlines()[1]

        assert result.exit_code == 0
        assert lineUser == "user = test\n"
        assert os.path.isfile(env.GRAVITEEIO_CONF_FILE)

def test_create_env_config():
    runner = CliRunner()

    with runner.isolated_filesystem():

        result = runner.invoke(main, ['config','--user','testenv', "--env", "QLF"])

        with open(env.GRAVITEEIO_CONF_FILE) as file:
            lineUser = file.readlines()[7]

        assert result.exit_code == 0
        assert os.path.isfile(env.GRAVITEEIO_CONF_FILE)
        assert lineUser == "user = testenv\n"

def test_create_env_config():
    runner = CliRunner()

    with runner.isolated_filesystem():

        result = runner.invoke(main, ['config','--user','testenv', "--env", "QLF", "--load", "QLF"])

        with open(env.GRAVITEEIO_CONF_FILE) as file:
            config = GraviteeioConfiguration()
            user = config.user

        assert result.exit_code == 0
        assert os.path.isfile(env.GRAVITEEIO_CONF_FILE)
        assert user == "testenv"

