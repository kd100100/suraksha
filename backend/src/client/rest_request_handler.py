import aiohttp
from typing import Dict, Any


async def make_request(method: str, url: str, body: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, json=body, headers=headers) as response:
            return {
                "status_code": response.status,
                "text": await response.text(),
                "headers": dict(response.headers)
            }
