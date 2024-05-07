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
)

from .sources import (
    EXCLUDED_SOURCES,
)
from .sources import (
    category_to_sources as default_category_to_sources,
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
    stop=stop_after_attempt(5),
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
    category_to_sources: dict[ArticleCategory, list[str]],
    start_date: datetime.datetime,
    end_date: datetime.datetime,
) -> list[ArticleWithNoContent]:
    """Scrape articles from RSS links in category_to_sources

    :param session: aiohttp ClientSession object
    :type session: :class:`aiohttp.ClientSession`

    :param category_to_sources: Dictionary mapping ArticleCategory to list of RSS links
    :type category_to_sources: :class:`dict[ArticleCategory, list[str]]`

    :param start_date: Start date of the date range
    :type start_date: :class:`datetime.datetime`

    :param end_date: End date of the date range
    :type end_date: :class:`datetime.datetime`

    :return: List of ArticleWithNoContent objects
    :rtype: :class:`list[ArticleWithNoContent]`
    """
    all_articles: list[ArticleWithNoContent] = []
    tasks = []
    for category, sources in category_to_sources.items():
        for rss_link in sources:
            tasks.append(fetch_rss_feed(session, rss_link))
    items_lists = await tqdm.gather(*tasks, desc="Fetching RSS feeds")

    for items, (category, sources) in zip(items_lists, category_to_sources.items()):
        for rss_link, items in zip(sources, items_lists):
            # Filter rss items by date
            filtered_items = [
                item
                for item in items
                if start_date.strftime("%Y-%m-%d")
                <= parse(item["published"]).strftime("%Y-%m-%d")
                <= end_date.strftime("%Y-%m-%d")
            ]

            print(f"Found {len(filtered_items)} articles from {rss_link}")

            articles = process_rss_items(filtered_items, category)
            all_articles.extend(articles)

    return all_articles


async def async_get_today_articles(
    category_to_sources: dict[ArticleCategory, list[str]] = default_category_to_sources,
    timezone: str = "Asia/Ho_Chi_Minh",
) -> list[Article]:
    """Scrape articles from RSS links for today

    :param category_to_sources: Dictionary mapping ArticleCategory to list of RSS links
    :type category_to_sources: :class:`dict[ArticleCategory, list[str]]`

    :param timezone: Timezone to filter articles by date, defaults to "Asia/Ho_Chi_Minh"
    :type timezone: :class:`str`

    :return: List of Article objects
    :rtype: :class:`list[Article]`
    """
    today = datetime.datetime.now(pytz.timezone(timezone))
    next_day = datetime.datetime.now(pytz.timezone(timezone)) + datetime.timedelta(
        days=1
    )

    print(f"Today: {today}")

    async with aiohttp.ClientSession() as session:
        articles_with_no_content = await get_articles_from_sources(
            session, category_to_sources, today, next_day
        )
        print(f"Found {len(articles_with_no_content)} articles from RSS feeds.")
        articles = await fetch_article_contents(session, articles_with_no_content)
        print(f"Processed {len(articles)} articles.")

    return articles


def get_today_articles(
    category_to_sources: dict[ArticleCategory, list[str]] = default_category_to_sources,
    timezone: str = "Asia/Ho_Chi_Minh",
) -> list[Article]:
    return asyncio.run(async_get_today_articles(category_to_sources, timezone))
