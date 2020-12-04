import asyncio
import concurrent.futures
from graviteeio_cli.core.config import GraviteeioConfig
from ..gio_resources import APIM_Client

APIS_CONTEXT = "/management/{}apis/"


class ApiClientAsync:

    def __init__(self, config: GraviteeioConfig = None, debug=False):
        self.config = config
        self.timeout = 10

    async def get_apis_with_state(self):
        self.api_client = APIM_Client.API.http(self.config)

        api_list = self.api_client.get()

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(
                    executor,
                    self.complete_state,
                    api
                )
                for api in api_list
            ]
            asyncio.gather(*futures)

        return api_list

    async def complete_state(self, api):
        api2 = api
        id = api["id"]
        deploy_state = await self.api_client.state(id)
        api2["is_synchronized"] = deploy_state["is_synchronized"]
        return api2
