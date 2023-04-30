import aiohttp


async def get_response(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


async def post_response(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            return await resp.json()


async def put_response(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.put(url, data=data) as resp:
            return await resp.json()
