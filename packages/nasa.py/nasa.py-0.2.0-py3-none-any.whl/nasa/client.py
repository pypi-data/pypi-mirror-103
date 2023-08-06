from .http import *
from .models import *

class Client:
    def __init__(self, api_key : str = ""):
        self._key = api_key
        self.http = HTTPClient()
        self.auth_params = {"api_key" : api_key}
        self.http.login(api_key)

    async def apod(self) -> APODResult:
        route = Route("/planetary/apod")
        route.params = self.auth_params
        response = await self.http.request(route)
        apod_response = APODResult(await response.json())
        return apod_response

    async def close(self) -> None:
        return await self.http.session.close()
        
