import asyncio
from typing import Callable
from httpx import AsyncClient
from types import SimpleNamespace
import json
from bot import Bot


class Updater:
    __token: str

    def __init__(self, token: str, base_url: str = "https://tapi.bale.ai/bot"):
        self.__token = token
        self.__offset = 0
        self.bot = Bot(self.__token, base_url)
        self.base_url = base_url
        self.callback = self.on_response
        
    async def on_response(self, message):
        pass

    async def __poll(self):
        async with AsyncClient() as client:
            client: AsyncClient
            request = await client.get(
                f"{self.base_url}{self.__token}/getUpdates",
                headers={'Connection': 'keep-alive'}
            )
            response = json.loads(request.text, object_hook=lambda d: SimpleNamespace(**d))

            if len(response.result) > 0:
                self.__offset = response.result[-1].update_id
            
            else:
                await self.__poll()

        async with AsyncClient() as client:
            client: AsyncClient
            request = await client.get(
                f"{self.base_url}{self.__token}/getUpdates?offset={self.__offset}",
                headers={'Connection': 'keep-alive'}
            )
            response = json.loads(request.text, object_hook=lambda d: SimpleNamespace(**d))

            if len(response.result) > 0:
                self.__offset += 1

                for message in response.result:
                    await self.callback(message.message)
            await self.__poll()

    def start_polling(self, *args):
        for arg in args:
            if isinstance(arg, Callable):
                self.callback = arg
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.__poll())