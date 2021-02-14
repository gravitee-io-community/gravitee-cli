import os


def string_to_bool(value):
    return value.lower() in ("yes", "true", "t", "1")


DEFAULT_APIM_ADDRESS_URL = os.getenv("GIO_APIM_URL", "https://nightly.gravitee.io")
DEFAULT_AM_ADDRESS_URL = os.getenv("GIO_AM_URL", "https://auth.gravitee.io")

DEFAULT_APIM_TOKEN = os.getenv("GIO_APIM_TOKEN", None)
DEFAULT_AM_TOKEN = os.getenv("GIO_AM_TOKEN", None)

DEFAULT_APIM_ORG = os.getenv("GIO_APIM_ORG", "DEFAULT")
DEFAULT_APIM_ENV = os.getenv("GIO_APIM_ENV", "DEFAULT")

DEFAULT_LINTER_RULESET_FILES = os.getenv("GIO_RULESET_FILE", None)
DEFAULT_LINTER_RULESET_TTL = os.getenv("GIO_TTL_RULESET", 5)

# GRAVITEEIO_RESOURCES_FOLDER="gio"
APIM_ENV_FILE_NAME = "apim_env.yml"
# APIM_API_VALUE_FILE_NAME = "_values.yml"
GIO_VALUE_FILE_NAME = "Graviteeio{}"
GIO_SETTING_FOLDER = "settings"
GIO_TEMPLATES_FOLDER = "templates"
API_CONFIG_FILE_NAME = "api_config{}.j2"
APP_CONFIG_FILE_NAME = "app_config{}.j2"
APIM_API_TEMPLATE_VERSION_FILE = "versions"

GRAVITEEIO_CONF_FILE = os.getenv("GRAVITEEIO_CONF_FILE", os.path.expanduser("~") + "/.graviteeio")
