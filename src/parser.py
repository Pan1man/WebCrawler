from fastapi import Depends

from src.urlfrontier import Frontier, url_frontier
import aiohttp


class Parser:
    @staticmethod
    async def fetch(frontier: Frontier = url_frontier):
        async with aiohttp.ClientSession() as session:
            async with session.get(frontier.remove_url()) as response:
                return await response.text()
