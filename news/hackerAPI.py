import asyncio, requests, logging
from django.conf import settings
from .models import News
from asgiref.sync import sync_to_async
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


async def GetTopNewsID() -> list[int]:
    """ GetRecentNewsID returns the top 100 news from hacker news api. """

    URL = settings.HACKER_NEWS_URL+'/topstories.json'
    try:
        r = requests.get(URL)
        if r.status_code == 200:
            return r.json()[:settings.HACKER_NEWS_RANGE]
    except Exception as ex:
        print("An exception occured.", ex)
        return []



async def GetNewsDetailsByID(item_id) -> tuple():
    """ GetNewsDetailsByID returns the news detail by news ID from hacker news api. """

    news, kids = News(), []
    URL = settings.HACKER_NEWS_URL+'/item/{item_id}.json'.format(item_id=item_id)
    try:
        if item_id is not None:
            r = requests.get(URL, timeout=15)
            if r.status_code == 200:
                res = r.json()
                news.by = res.get('by') or ''
                news.descendants = res.get('descendants') or 0
                news.id = res.get('id')
                news.score = res.get('score') or 0
                news.time = res.get('time') or 0
                news.title = res.get('title')
                news.type = res.get('type')
                news.url = res.get('url') 
                news.deleted = res.get('deleted') or False
                news.dead = res.get('dead') or False
                news.text = res.get('text') 
                news.parent = res.get('parent')

                kids = res.get('kids') or []
                news.kids = ",". join([str(i) for i in kids])
                return (news, kids)
    except Exception as ex:
        print("An exception occured.", ex)
        return (None, None)


async def channel(ids: list[int]):
    if ids == None:
        return

    items = [asyncio.create_task(GetNewsDetailsByID(id)) for id in ids]
    completed, _ = await asyncio.wait(items)
    
    parent = [task.result()[0] for task in completed if task.result()[0] is not None]
    kids = [task.result()[1] for task in completed if task.result()[1] is not None]

    # Save list of News object
    sync_to_async(SaveNews(parent))
    
    if len(kids) > 0:
        # fetch kid items by id, recusively call channel till all child is completed
        items = [asyncio.create_task(sink(id)) for id in kids if id is not None]
        try:
            await asyncio.wait(items)
        except Exception as ex:
            print("An error occured", ex)



async def sink(ids: list[int]):
    if len(ids) > 0:
        await asyncio.create_task(channel(ids))



def SaveNews(news: list[News]):
    if type(news) is list:
        News.object.bulk_create(news,ignore_conflicts=True)


def GetHackerStories():
    loop = asyncio.new_event_loop()
    TopIDs = loop.run_until_complete(GetTopNewsID())
    try:
        if TopIDs:
            loop.run_until_complete(channel(TopIDs))
    finally:
        print('Get Hacker Stories Completed.....')
        loop.close()


def startScheduler():
    print("Scheduler start")
    interval = settings.HACKER_NEWS_SYNC
    scheduler.add_job(GetHackerStories)
    scheduler.add_job(GetHackerStories, 'interval', minutes=interval)
    scheduler.start()


def stopScheduler():
    print("Scheduler shutdown")
    scheduler.shutdown()
