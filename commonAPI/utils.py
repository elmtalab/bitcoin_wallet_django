import asyncio


import aiohttp as aiohttp


async def fetch(session, url):
    """Execute an http call async
    Args:
        session: contexte for making the http call
        url: URL to call
    Return:
        responses: A dict like object containing http response
    """
    async with session.get(url) as response:
        resp = await response.json()
        return resp

async def fetch_all(url_list):
    """ Gather many HTTP call made async
    Args:
        url_list: a list of string
    Return:
        responses: A list of dict like object containing http response
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in url_list:
            tasks.append(
                fetch(
                    session,
                    url,
                )
            )
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses



def run_all_fetches(url_list):
    responses = asyncio.run(fetch_all(url_list))
    return responses