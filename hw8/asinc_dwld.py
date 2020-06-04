import time
import asyncio
import aiohttp
import argparse
from http_helpers import HttpParser


# --------------------------------------------------------------------------------------------
async def my_request(client, url):
    if not url.startswith('http://') or not url.startswith('https://'):
        url = f'https://{url}'
    async with client.get(url, allow_redirects=True) as resp:
        obj = HttpParser(await resp.text())
        return url, obj.top(5)


# --------------------------------------------------------------------------------------------
def next_urls_pack(urls: list, size):
    for i in range(0, len(urls), size):
        yield urls[i: i + size]


# --------------------------------------------------------------------------------------------
async def main(n: int, urls: list):
    tasks = []
    results = []
    async with aiohttp.ClientSession() as client:
        packs = next_urls_pack(urls, n)
        for nn, pack in enumerate(packs, 1):
            print(f'Pack #{nn}')
            for url in pack:
                tasks.append(asyncio.create_task(my_request(client, url)))
            results.append(await asyncio.gather(*tasks))
    return results


# --------------------------------------------------------------------------------------------
def prepare_urls(url_file, limit=100):
    with open(url_file) as file:
        urls_list = [i.strip() for num, i in enumerate(file) if num < limit]
    return urls_list


# --------------------------------------------------------------------------------------------
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', dest='requests', type=int)
    parser.add_argument('-lim', dest='limit', type=int, default=20)
    parser.add_argument('-f', dest='urls_file', type=str)
    args = parser.parse_args()

    n = args.requests
    urls_file = args.urls_file
    lim = args.limit

    urls = prepare_urls(urls_file, limit=lim)
    t1 = time.time()
    results = asyncio.run(main(n, urls))
    t2 = time.time() - t1

    for pack in results:
        for item in pack:
            print(item)
    print(f'Total time for {n} {t2}')

