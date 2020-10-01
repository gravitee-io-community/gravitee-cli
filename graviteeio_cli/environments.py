import os


def string_to_bool(value):
    return value.lower() in ("yes", "true", "t", "1")


DEFAULT_APIM_ADDRESS_URL = os.getenv("GIO_APIM_URL", "https://demo.gravitee.io")
DEFAULT_AM_ADDRESS_URL = os.getenv("GIO_AM_URL", "https://auth.gravitee.io")

DEFAULT_APIM_TOKEN = os.getenv("GIO_APIM_TOKEN", None)
DEFAULT_AM_TOKEN = os.getenv("GIO_AM_TOKEN", None)

DEFAULT_APIM_ORG = os.getenv("GIO_APIM_ORG", None)
DEFAULT_APIM_ENV = os.getenv("GIO_APIM_ENV", None)

# GRAVITEEIO_RESOURCES_FOLDER="gio"
APIM_ENV_FILE_NAME = "apim_env.yml"
# APIM_API_VALUE_FILE_NAME = "_values.yml"
APIM_API_VALUE_FILE_NAME = "apim_values{}"
APIM_API_SETTING_FOLDER = "settings"
APIM_API_TEMPLATES_FOLDER = "templates"
APIM_API_TEMPLATE_FILE = "apim_config{}.j2"
APIM_API_URL_GITHUB_TEMPLATE_FOLDER = "https://raw.githubusercontent.com/gravitee-io/graviteeio-cli/master/templates/"
APIM_API_TEMPLATE_VERSION_FILE = "versions"

GRAVITEEIO_CONF_FILE = os.getenv("GRAVITEEIO_CONF_FILE", os.path.expanduser("~") + "/.graviteeio")

APIM_HTTP_CONNECTION_TIMEOUT = int(os.getenv("APIM_HTTP_CONNECTION_TIMEOUT", 5000))
APIM_HTTP_IDLE_TIMEOUT = int(os.getenv("APIM_HTTP_IDLE_TIMEOUT", 60000))
APIM_HTTP_KEEP_ALIVE = string_to_bool(os.getenv("APIM_HTTP_KEEP_ALIVE", "True"))
APIM_HTTP_READ_TIMEOUT = int(os.getenv("APIM_HTTP_READ_TIMEOUT", 10000))
APIM_HTTP_PIPELINING = string_to_bool(os.getenv("APIM_HTTP_PIPELINING", "False"))
APIM_HTTP_MAX_CONCURRENT_CONNECTION = int(os.getenv("APIM_HTTP_MAX_CONCURRENT_CONNECTION", 100))
APIM_HTTP_USE_COMPRESSION = string_to_bool(os.getenv("APIM_HTTP_MAX_CONCURRENT_CONNECTION", "True"))
APIM_HTTP_FOLLOW_REDIRECTS = string_to_bool(os.getenv("APIM_HTTP_MAX_CONCURRENT_CONNECTION", "False"))
