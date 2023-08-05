# Imports
import requests
import asyncio
from .Message import Message
import ast

url = "https://python-bot-4.herokuapp.com"

class Client:
    def event(self, coro):
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('event registered must be a coroutine function')

        setattr(self, coro.__name__, coro)
        # print('%s has successfully been registered as an event', coro.__name__)
        return coro

    async def receive(self, message):
        try:
            await self.on_message(message)
        except AttributeError:
            pass

    def run(self, rate=0.5):

        async def runner():
            try:
                r = ast.literal_eval(requests.get(url + "/messages").text)
            except SyntaxError:
                r = {}
            try:
                previous_id = list(r)[-1]
            except IndexError:
                previous_id = ""
            while True:
                try:
                    r = ast.literal_eval(requests.get(url + "/messages").text)
                except SyntaxError:
                    r = {}
                try:
                    msg_id = list(r)[-1]
                except IndexError:
                    msg_id = ""
                if msg_id != previous_id:
                    await self.receive(Message(r[msg_id], int(msg_id)))
                previous_id = msg_id
                await asyncio.sleep(rate)
        asyncio.run(runner())
