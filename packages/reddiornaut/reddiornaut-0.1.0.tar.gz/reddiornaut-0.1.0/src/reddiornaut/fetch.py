import asyncio
import aiohttp
import json

from .objects import RedditPost, SubredditListing


UA_STRING = "".join("""
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36
(KHTML, like Gecko)
Chrome/51.0.2704.103 Safari/537.36
""".split('\n')).strip()


async def send_request(uri, datatype='bytes'):
    global UA_STRING
    if not (datatype == 'bytes' or datatype == 'text' or datatype == 'json'):
        raise Exception
    headers = {'User-Agent': UA_STRING}
    async with aiohttp.ClientSession() as session:
        async with session.get(uri, headers=headers) as response:
            if datatype == 'json':
                return await response.json()
            elif datatype == 'text':
                return (await response.read()).decode()
            else:
                return await response.read()


async def get_post_json(post_link):
    """
    Both permalinks and post ids are supported
    """
    uri = "https://reddit.com/%s.json"
    if "reddit.com" in post_link:
        # assume permalink
        response = (await send_request(post_link, datatype='json'))
        post = RedditPost(response[0]['data']['children'][0])
    else:
        # assume id/shortlink
        response = (await send_request(uri % post_link, datatype='json'))
        post = RedditPost(response[0]['data']['children'][0])
    return post


async def get_sub_json(sub, sort=None, time=None):
    if sort is None:
        query = f"https://reddit.com/r/{sub}.json"
    elif sort == 'top' or sort == 'controversial':
        if time is None:
            query = f"https://reddit.com/r/{sub}/{sort}.json"
        else:
            query = f"https://reddit.com/r/{sub}/{sort}.json?t={time}"
    else:
        query = f"https://reddit.com/r/{sub}/{sort}.json"
    return await send_request(query, datatype='json')


async def get_posts(subreddit, n=5, sort=None, time=None):
    listing = SubredditListing(await get_sub_json(subreddit, sort, time))
    return listing.posts[:n]


async def get_random_post(subreddit):
    uri = "https://reddit.com/r/%s/random.json"
    response = (await send_request(uri % subreddit, datatype='json'))
    return RedditPost(response[0]['data']['children'][0])


if __name__ == "__main__":
    async def main():
        posts = await get_posts('aww', n=6, sort='top', time='all')
        for post in posts:
            print(post)
        print(await get_post_json('e279vx'))
        print(await get_random_post('awww'))
    asyncio.run(main())
