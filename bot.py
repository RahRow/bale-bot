import json

from httpx import AsyncClient, Response
from types import SimpleNamespace


class Bot:
    token: str

    def __init__(self, token: str, base_url: str):
        self.__token = token
        self.base_url = base_url

    async def __request(self, method: str, action: str, data: dict) -> object:
        async with AsyncClient() as client:
            request = await client.request(method, f"{self.base_url}{self.__token}/{action}", data=data)
            return json.loads(request.text, object_hook=lambda x: SimpleNamespace(**x))

    async def send_message(self, chat_id: int, text: str):
        await self.__request('POST', 'sendMessage', data={
            'chat_id': chat_id,
            'text': text
        })