import logging
import json

from graviteeio_cli.http_client.http_client import HttpClient
from graviteeio_cli.core.config import GraviteeioConfig_apim
from graviteeio_cli.exeptions import GraviteeioError

logger = logging.getLogger("client.app_client")


class AppClient:

    def __init__(self, config: GraviteeioConfig_apim, debug=False):
        self.httpClient = HttpClient("/management/{}applications/", config)

    def get(self, id=None, response_filter=None):
        json_body = self.httpClient.get("{}".format(id) if id else "").json()

        if response_filter:
            response_filter(json_body)
        return json_body

    def create(self, app_data):
        return self.httpClient.post("", data=json.dumps(app_data)).json()

    def update(self, id, app_data):
        return self.httpClient.put(f"{id}", data=json.dumps(app_data)).json()

    def get_export(self, id, response_filter=None):
        json_body = self.httpClient.get("{}".format(id) if id else "").json()
        metadata = self.get_metadata(id)
        json_body["metadata"] = metadata

        if response_filter:
            response_filter(json_body)
        return json_body

    def create_import(self, app_data):
        local_app_data, metadata = self._split_app_data(app_data)

        app = self.create(local_app_data)
        if metadata and len(metadata) > 0:
            new_metadata = []
            for data in metadata:
                try:
                    meta = self.httpClient.post(f"{app['id']}/metadata", data=json.dumps(data)).json()
                    new_metadata.append(meta)
                except Exception:
                    logger.error(f"Exception to create metadata [{data}]")

            if app:
                app["metadata"] = new_metadata

        return app

    def update_import(self, id, app_data: dict):
        local_app_data, metadata = self._split_app_data(app_data)

        app = self.update(id, local_app_data)
        if metadata and len(metadata) > 0:
            new_metadata = self.create_update_metadata(id, metadata)

            if app:
                app["metadata"] = new_metadata

        return app

    def _split_app_data(self, app_data):
        metadata = None
        local_app_data = app_data.copy()
        if "metadata" in app_data:
            metadata = app_data["metadata"]
            del local_app_data["metadata"]

        return (local_app_data, metadata)

    def get_metadata(self, app_id, metadata_key=""):
        return self.httpClient.get(f"{app_id}/metadata/{metadata_key}").json()

    def create_update_metadata(self, app_id, metadata: list):
        if not metadata or len(metadata) < 1:
            return []

        metadata_conf_dic = {}

        for m_conf in metadata:
            if "name" in m_conf and m_conf["name"] not in metadata_conf_dic:
                metadata_conf_dic[m_conf["name"]] = m_conf
            else:
                raise GraviteeioError("metadata name must be unique")

        metadata_server = self.get_metadata(app_id)

        metadata_to_update = []
        for m_serve in metadata_server:
            if "name" in m_serve and m_serve["name"] in metadata_conf_dic:
                metadata_conf_value = metadata_conf_dic[m_serve["name"]]

                metadata_conf_value["key"] = m_serve["key"]
                is_diff = False
                for key, value in metadata_conf_value.items():
                    if value != m_serve[key]:
                        is_diff = True

                if is_diff:
                    metadata_to_update.append(metadata_conf_value)

                del metadata_conf_dic[m_serve["name"]]

        metadata_to_save = metadata_conf_dic.values()

        metadata_to_return = []

        for data in metadata_to_save:
            try:
                meta = self.httpClient.post(f"{app_id}/metadata", data=json.dumps(data)).json()
                metadata_to_return.append(meta)
            except Exception as e:
                print(e)
                logger.error(f"Exception to create metadata [{data}]")

        for data in metadata_to_update:
            try:
                meta = self.httpClient.put(f"{app_id}/metadata/{data['key']}", data=json.dumps(data)).json()
                metadata_to_return.append(meta)
            except Exception:
                logger.error(f"Exception to update metadata [{data}]")

        return metadata_to_return
