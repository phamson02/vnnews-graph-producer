import asyncio
import datetime
import ssl
from typing import Literal

import aiohttp
import feedparser
import pytz
from dateutil.parser import parse
from newspaper import Article as RawArticle
from newspaper import Config
from tenacity import retry, stop_after_attempt, wait_fixed
from tqdm.asyncio import tqdm

from vnnews_graph_producer.data_models.article import (
    Article,
    ArticleCategory,
    ArticleWithNoContent,
    Source,
)

from .sources import (
    EXCLUDED_SOURCES,
)
from .sources import (
    SOURCES as default_sources,
)
from .special_handlers import fix_thanhnien_title, open_vnanet_article

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0"
)

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 30


ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.options |= 0x4


async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url, ssl=ssl_context) as response:
        return await response.text()


def fetch_content_error_callback(retry_state) -> Literal[""]:
    print(f"Failed to fetch content: {retry_state.outcome.exception()}")
    return ""


@retry(
    wait=wait_fixed(10),
    stop=stop_after_attempt(3),
    reraise=False,
    retry_error_callback=fetch_content_error_callback,
)
async def scrape_article_content(
    session: aiohttp.ClientSession,
    article_link: str,
) -> str:
    """Scrape article content from article_link

    :param article_link: URL of the article
    :type article_link: :class:`str`

    :return: Article content
    :rtype: :class:`str`
    """
    article = RawArticle(article_link, config=config)
    html_text = await fetch(session, article_link)
    article.download(input_html=html_text)
    article.parse()
    return article.text


async def fetch_article_contents(
    session: aiohttp.ClientSession, articles: list[ArticleWithNoContent]
) -> list[Article]:
    tasks = [
        scrape_article_content(session, article.url)
        for article in articles
        if article.url
    ]
    contents = await tqdm.gather(*tasks, desc="Fetching article contents")

    articles_with_content: list[Article] = []
    for article, content in zip(articles, contents):
        articles_with_content.append(article.add_content(content))

    return articles_with_content


async def fetch_rss_feed(session: aiohttp.ClientSession, rss_link: str) -> list[dict]:
    html_text = await fetch(session, rss_link)
    rss = feedparser.parse(html_text)
    return rss["items"]


def process_rss_items(items, category: ArticleCategory) -> list[ArticleWithNoContent]:
    """Process RSS items to create Article objects

    :param items: List of RSS items
    :type items: :class:`list[dict]

    :param category: Category of the articles
    :type category: :class:`ArticleCategory`

    :return: List of ArticleWithNoContent objects
    :rtype: :class:`list[ArticleWithNoContent]`
    """
    articles: list[ArticleWithNoContent] = []
    for item in items:
        if any(excluded_source in item["link"] for excluded_source in EXCLUDED_SOURCES):
            continue

        # Special treatments for certain sources
        if "vnanet.vn" in item["link"]:
            article_url = open_vnanet_article(item["link"])
        else:
            article_url = item["link"]

        if "thanhnien.vn" in item["link"]:
            article_title = fix_thanhnien_title(item["title"])
        else:
            article_title = item["title"]

        article = ArticleWithNoContent(
            title=article_title,
            url=article_url,
            published_date=parse(item["published"]),
            category=category,
        )

        articles.append(article)

    return articles


async def get_articles_from_sources(
    session: aiohttp.ClientSession,
    rss_sources: list[Source],
    start_time: datetime.datetime,
    end_time: datetime.datetime,
) -> list[ArticleWithNoContent]:
    """Scrape articles from RSS sources published whithin a time range

    :param session: aiohttp ClientSession object
    :type session: :class:`aiohttp.ClientSession`

    :param rss_sources: List of Source objects
    :type rss_sources: :class:`list[Source]`

    :param start_time: Start time of the time range
    :type start_time: :class:`datetime.datetime`

    :param end_time: End time of the time range
    :type end_time: :class:`datetime.datetime`

    :return: List of ArticleWithNoContent objects
    :rtype: :class:`list[ArticleWithNoContent]`
    """
    all_articles: list[ArticleWithNoContent] = []
    tasks = []
    for source in rss_sources:
        tasks.append(fetch_rss_feed(session, source.rss_link))
    items_lists = await tqdm.gather(*tasks, desc="Fetching RSS feeds")

    for items, source in zip(items_lists, rss_sources):
        filtered_items = [
            item
            for item in items
            if start_time.strftime("%Y-%m-%d %H:%M:%S")
            <= parse(item["published"]).strftime("%Y-%m-%d %H:%M:%S")
            <= end_time.strftime("%Y-%m-%d %H:%M:%S")
        ]

        print(f"Found {len(filtered_items)} articles from {source.rss_link}")

        articles = process_rss_items(filtered_items, source.category)
        all_articles.extend(articles)

    return all_articles


async def async_get_last_24h_articles(
    rss_sources: list[Source] = default_sources,
    timezone: str = "Asia/Ho_Chi_Minh",
) -> list[Article]:
    """Scrape articles from RSS sources in the last 24 hours

    :param rss_sources: List of Source objects
    :type rss_sources: :class:`list[Source]`

    :param timezone: Timezone to filter articles by date, defaults to "Asia/Ho_Chi_Minh"
    :type timezone: :class:`str`

    :return: List of Article objects
    :rtype: :class:`list[Article]`
    """
    end_time = datetime.datetime.now(pytz.timezone(timezone))
    start_time = end_time - datetime.timedelta(days=1)

    print(f"Fetching articles from {start_time} to {end_time}")

    async with aiohttp.ClientSession() as session:
        articles_with_no_content = await get_articles_from_sources(
            session, rss_sources, start_time, end_time
        )
        print(f"Found {len(articles_with_no_content)} articles from RSS feeds.")
        articles = await fetch_article_contents(session, articles_with_no_content)
        print(f"Processed {len(articles)} articles.")

    return articles


def get_last_24h_articles(
    rss_sources: list[Source] = default_sources,
    timezone: str = "Asia/Ho_Chi_Minh",
) -> list[Article]:
    return asyncio.run(async_get_last_24h_articles(rss_sources, timezone))
