import os

def string_to_bool(value):
     return value.lower() in ("yes", "true", "t", "1")

DEFAULT_USER="admin"
DEFAULT_PASSWORD="admin"
DEFAULT_ADDRESS_URL="https://demo.gravitee.io"

GRAVITEEIO_TEMPLATES_FOLDER="graviteeio"
APIM_API_VALUE_FILE_NAME="apim_api_value.yml"
APIM_API_TEMPLATE_FILE="apim_api_template.yml.j2"
APIM_API_URL_GITHUB_TEMPLATE_FOLDER="https://raw.githubusercontent.com/gravitee-io/graviteeio-cli/master/templates/"
APIM_API_TEMPLATE_VERSION_FILE="versions"
APIM_API_TEMPLATE_MODEL="apim_api_template_{}.yml.j2"

GRAVITEEIO_CONF_FILE = os.getenv("GRAVITEEIO_CONF_FILE", os.path.expanduser("~") + "/.graviteeio")

APIM_HTTP_CONNECTION_TIMEOUT = int(os.getenv("APIM_HTTP_CONNECTION_TIMEOUT", 5000))
APIM_HTTP_IDLE_TIMEOUT = int(os.getenv("APIM_HTTP_IDLE_TIMEOUT", 60000))
APIM_HTTP_KEEP_ALIVE = string_to_bool(os.getenv("APIM_HTTP_KEEP_ALIVE", "True"))
APIM_HTTP_READ_TIMEOUT = int(os.getenv("APIM_HTTP_READ_TIMEOUT", 10000))
APIM_HTTP_PIPELINING = string_to_bool(os.getenv("APIM_HTTP_PIPELINING", "False"))
APIM_HTTP_MAX_CONCURRENT_CONNECTION = int(os.getenv("APIM_HTTP_MAX_CONCURRENT_CONNECTION", 100))
APIM_HTTP_USE_COMPRESSION = string_to_bool(os.getenv("APIM_HTTP_MAX_CONCURRENT_CONNECTION", "True"))
APIM_HTTP_FOLLOW_REDIRECTS = string_to_bool(os.getenv("APIM_HTTP_MAX_CONCURRENT_CONNECTION", "False"))
