# Imports
import asyncio
from .Message import Message
import aiohttp
import json
from . import Errors

web_url = "https://python-bot-4.herokuapp.com"

class Client:
    def event(self, coro):
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('Event registered must be a coroutine function')

        setattr(self, coro.__name__, coro)
        # print('%s has successfully been registered as an event', coro.__name__)
        return coro

    async def received_status(self, status_code):
        if status_code == 200:
            try:
                await self.on_ready()
            except AttributeError:
                pass
        else:
            raise Errors.ApiError

    async def received_message(self, content, msg_id):
        try:
            await self.on_message(Message(content, msg_id))
        except AttributeError:
            pass

    def run(self):
        async def runner():
            async with aiohttp.ClientSession() as session:
                check = await session.get(web_url + "/api/messages")
                await self.received_status(check.status)

                previous = await check.text()

                while True:
                    async with session.get(web_url + "/api/messages") as resp:
                        text = await resp.text()
                        if text not in ["{}", previous]:
                            previous = text
                            message = json.loads(text)
                            content = message.get("content")
                            if content is not None:
                                await self.received_message(content, int(message.get("id")))

        asyncio.run(runner())
