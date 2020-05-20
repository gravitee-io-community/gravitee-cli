import asyncio
import os
import time
import concurrent.futures
from graviteeio_cli.exeptions import GraviteeioRequestError
from graviteeio_cli.graviteeio.config import GraviteeioConfig
from requests import RequestException
from ..gio_resources import APIM_Client

APIS_CONTEXT = "/management/{}apis/"

# class RestApi:

#     # class __OnlyOne:
#     #     def __init__(self, arg):
#     #         self.val = arg
#     #     def __str__(self):
#     #         return repr(self) + self.val
       
#     def __init__(self):
#         async with httpx.Client() as client:
#             self.client = client

# import asyncio
# import concurrent.futures
# import requests

# async def main():

#     with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

#         loop = asyncio.get_event_loop()
#         futures = [
#             loop.run_in_executor(
#                 executor, 
#                 requests.get, 
#                 'http://example.org/'
#             )
#             for i in range(20)
#         ]
#         for response in await asyncio.gather(*futures):
#             pass


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
class ApiClientAsync:

    def __init__(self, config: GraviteeioConfig = None, debug=False):
        self.config = config
        self.timeout = 10

    async def get_apis_with_state(self):
        # self.http_client = GioClient.APIM(APIM_client_type.API, self.config)
        self.api_client = APIM_Client.API.http(self.config)

        api_list = self.api_client.get()

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(
                    executor, 
                    self.complete_state, 
                    api
                )
                for api in api_list
            ]
            await asyncio.gather(*futures)
            # for response in await asyncio.gather(*futures):
            #     pass
            
        return api_list
    
    def complete_state(self, api):
        # print("id {}".format(api["id"]))
        deploy_state = self.api_client.state(api["id"])
        # print("deploy_state {}".format(deploy_state))
        api["is_synchronized"] = deploy_state["is_synchronized"]


#         loop = asyncio.get_event_loop()
#         futures = [
#             loop.run_in_executor(
#                 executor, 
#                 requests.get, 
#                 'http://example.org/'
#             )
#             for i in range(20)
#         ]
#         for response in await asyncio.gather(*futures):
#             pass


    # async def get_apis_with_state2(self):

    #     timeout = aiohttp.ClientTimeout(total=self.timeout)

    #     headers = {}
    #     if self.config.get_bearer():
    #         headers=self.config.get_bearer_header()
        
    #     headers["accept"] = "application/json"
    #     x = 0
    #     async with aiohttp.ClientSession(headers = headers, timeout=timeout) as session:
    #         async with session.get(self.config.url(APIS_CONTEXT), ssl=False) as resp:
    #             apis = await resp.json();

    #             # await asyncio.gather(*[self.complete_state2(session, api) for api in apis])
    #             for api in apis:
    #                 async with session.get(self.config.url(APIS_CONTEXT + "{}/state".format(api["id"])), ssl=False) as resp:
    #                     deploy_state = await resp.json()
    #                     # if x == 0:
    #                     #     time.sleep(1)
    #                     #     x = x +1 
    #                     print("deploy_state {}".format(deploy_state))
    #                     api["is_synchronized"] = deploy_state["is_synchronized"]
                

    #             return apis

    # async def complete_state2(self,session, api):
    #     async with session.get(self.config.url(APIS_CONTEXT + "{}/state".format(api["id"])), ssl=False) as resp:
    #         deploy_state = await resp.json()
    #         # print("deploy_state {}".format(deploy_state))
    #         api["is_synchronized"] = deploy_state["is_synchronized"]
