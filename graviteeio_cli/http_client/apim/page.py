import json
import logging

from graviteeio_cli.http_client.http_client import HttpClient
from graviteeio_cli.core.config import GraviteeioConfig_apim

logger = logging.getLogger("client.page_client")


class PageClient:

    def __init__(self, config: GraviteeioConfig_apim, debug=False):
        self.httpClient = HttpClient("/management/{}", config)

    def fetch(self, page_id=None, api_id=None):

        return self.httpClient.post(
            self._build_url(page_id, api_id, "_fetch")
        )

    def update(self, page_id, api_id, page_name, page_order, page_data, published=False, homepage=False):
        data = {
            "name": page_name,
            "order": page_order,
            "content": page_data,
            "published": published,
            "homepage": homepage
        }

        return self.httpClient.put(
            self._build_url(page_id, api_id),
            data=json.dumps(data)
        )

    def update_content(self, page_id, api_id, content):
        return self.httpClient.put(
            self._build_url(page_id, api_id, "content"),
            data=json.dumps(content)
        ).json()

    def get(self, page_id, api_id):
        return self.httpClient.get(
            self._build_url(page_id, api_id, None)
        ).json()

    def _build_url(self, page_id, api_id, action=None):
        path = ""

        if api_id:
            path = "apis/{}/pages".format(api_id)
        else:
            path = "portal/pages"

        if page_id:
            path = path + "/" + "{}".format(page_id)

        if action:
            path = path + "/" + action

        return path
