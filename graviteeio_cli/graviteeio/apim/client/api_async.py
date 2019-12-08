
import aiohttp
from graviteeio_cli.exeptions import GraviteeioRequestError
from requests import RequestException

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


# TODO Manage proxy https http
class ApiClientAsync:


    def __init__(self, config=None, debug=False):
        self.config = config
        self.timeout = 10


    # async def get_apis(self):
    #     # async with httpx.Client() as client:
    #     #     return await client.get(self.config.url(APIS_CONTEXT), auth = self.config.credential())
    #     client = httpx.Client()
    #     try:
    #         r = client.get(self.config.url(APIS_CONTEXT), auth = self.config.credential())
    #         return r
    #     finally:
    #         await client.close()

    async def get_apis_with_state(self):
        timeout = aiohttp.ClientTimeout(total=self.timeout)

        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth('admin', password='admin'), timeout=timeout) as session:
            async with session.get(self.config.url(APIS_CONTEXT), ssl=False) as resp:
                apis = await resp.json();
                for api in apis:
                    async with session.get(self.config.url(APIS_CONTEXT + "{}/state".format(api["id"])), ssl=False) as resp:
                        deploy_state = await resp.json()
                        api["is_synchronized"] = deploy_state["is_synchronized"]
                
                return apis
