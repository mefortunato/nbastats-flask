import grequests
import asyncio
from aiohttp import ClientSession

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36', 'x-nba-stats-origin': 'stats', 'x-nba-stats-token': 'true'}

#urls = ['https://stats.nba.com/stats/boxscoresummaryv2?GameID=00{}'.format(g) for g in range(21700001, 21701231)]
urls = ['https://stats.nba.com/stats/boxscoresummaryv2?GameID=00{}'.format(g) for g in range(21700001, 21700101)]
rs = (grequests.get(u, headers=HEADERS) for u in urls)
resps = grequests.map(rs)

print(resps)
exit()

async def go():
    async with ClientSession() as session:
        async with session.get('https://stats.nba.com/stats/boxscoresummaryv2?GameID=0021700001', headers=HEADERS) as resp:
            print(resp.status)
            print(await resp.text())
            
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(go())
loop.run_until_complete(future)
exit()

async def fetch(url, session):
    async with session.get(url, headers=HEADERS, timeout=10) as response:
        return await response.text()
    
async def run(r):
    url = "https://stats.nba.com/stats/boxscoresummaryv2?GameID=00{}"
    #url ="https://google.com"
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for i in range(21700001, 21700001+r):
            print(url.format(i))
            task = asyncio.ensure_future(fetch(url.format(i), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        print(responses[0])
        
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(1))
loop.run_until_complete(future)
