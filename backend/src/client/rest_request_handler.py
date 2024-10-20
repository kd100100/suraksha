import aiohttp
import time
from typing import Dict, Any


async def make_request(method: str, url: str, data: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        async with session.request(method, url, json=data, headers=headers) as response:
            response_data = await response.text()
            try:
                response_data = await response.json()
            except:
                pass  # Keep response_data as text if it's not JSON
            status_code = response.status
            response_headers = dict(response.headers)

        end_time = time.time()
        execution_time = end_time - start_time

        return {
            "status_code": status_code,
            "headers": response_headers,
            "body": response_data,
            "execution_time": execution_time
        }
