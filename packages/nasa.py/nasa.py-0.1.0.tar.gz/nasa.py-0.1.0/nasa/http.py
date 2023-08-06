import aiohttp
import asyncio
from .errors import *

class Route:
    BASE = "https://api.nasa.gov"
    def __init__(self, endpoint : str, params : dict = {}, method : str = "GET"):
        self.endpoint = endpoint
        self._method = method
        self._params = params

    def __repr__(self):
        return f"<Route method={self._method} path={self.path} params={self.params}>"
    
    @property
    def method(self):
        return self._method
    
    @property
    def path(self) -> str:
        return self.BASE + self.endpoint
    
    @property
    def params(self) -> dict:
        return self._params

    @params.setter
    def params(self, value : dict):
        self._params = value

class HTTPClient:
    def __init__(self, *args, **kwargs):
        self.session = aiohttp.ClientSession(*args, **kwargs)

    async def request(self, route : Route) -> aiohttp.ClientResponse:
        response = await self.session.request(route.method, route.path, params = route.params)
        return response

    async def read(self, url : str):
        response = await self.session.get(url)
        return await response.read()

    async def __try_key__(self, key : str):
        async with aiohttp.ClientSession(raise_for_status = False) as temp_session:
            response = await temp_session.get("https://api.nasa.gov/planetary/apod?api_key={}".format(key)) #just trying the key on one of the endpoints before using the api key on all the other endpoints
            if response.status == 403:
                raise InvalidAPIKey("Invalid API Key has been passed")


    def login(self, key : str):
        asyncio.get_event_loop().run_until_complete(self.__try_key__(key))