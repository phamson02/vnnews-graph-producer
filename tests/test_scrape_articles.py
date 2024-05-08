import aiohttp
import pytest
from vnnews_graph_producer.data_models.article import ArticleCategory, Source
from vnnews_graph_producer.scraper import async_get_last_24h_articles
from vnnews_graph_producer.scraper.article_scraper import scrape_article_content


@pytest.mark.asyncio
async def test_get_last_24h_articles():
    sources = [
        Source(
            rss_link="https://thanhnien.vn/rss/kinh-te.rss",
            category=ArticleCategory.Economy,
        ),
        Source(
            rss_link="https://vnanet.vn/vi/rss/nghe-thuat-van-hoa-va-giai-tri-1.rss",
            category=ArticleCategory.Entertainment,
        ),
        Source(
            rss_link="https://tuoitre.vn/rss/thoi-su.rss",
            category=ArticleCategory.News,
        ),
        Source(
            rss_link="http://vtv.vn/the-gioi.rss",
            category=ArticleCategory.World,
        ),
    ]

    articles = await async_get_last_24h_articles(sources)

    assert len(articles) > 0

    # Test if 3 categories of articles are collected
    categories = {article.category for article in articles}
    assert all(c in categories for c in {s.category for s in sources})


@pytest.mark.asyncio
async def test_scrape_article_content():
    url = "https://wrong_article_url.com"

    # create a session
    async with aiohttp.ClientSession() as session:
        content = await scrape_article_content(session, url)

    assert content == ""
