from asyncio import get_running_loop
from functools import partial

from aiohttp import ClientSession
from bs4 import BeautifulSoup

HLTV_HEADERS = {
    # Credit: @SocksPls
    "referer": "https://www.hltv.org/stats",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def f(result):
    return BeautifulSoup(result, "lxml")


async def fetch(url):
    async with ClientSession() as session:
        async with session.get(url, headers=HLTV_HEADERS) as response:
            result = await response.text()
            # Parse asynchronously with BeautifulSoup
            loop = get_running_loop()
            parsed = await loop.run_in_executor(None, partial(f, result))

            return parsed
