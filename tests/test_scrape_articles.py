import aiohttp
import pytest
from vnnews_graph_producer.data_models.article import ArticleCategory
from vnnews_graph_producer.scraper import get_today_articles
from vnnews_graph_producer.scraper.article_scraper import scrape_article_content


def test_get_today_articles():
    category_to_sources = {
        ArticleCategory.Economy: ["https://thanhnien.vn/rss/kinh-te.rss"],
        ArticleCategory.Entertainment: [
            "https://vnanet.vn/vi/rss/nghe-thuat-van-hoa-va-giai-tri-1.rss"
        ],
        ArticleCategory.News: ["https://tuoitre.vn/rss/thoi-su.rss"],
    }

    articles = get_today_articles(category_to_sources)

    assert len(articles) > 0

    # Test if 3 categories of articles are collected
    categories = {article.category for article in articles}
    assert all(c in categories for c in category_to_sources.keys())


@pytest.mark.asyncio
async def test_scrape_article_content():
    url = "https://wrong_article_url.com"

    # create a session
    async with aiohttp.ClientSession() as session:
        content = await scrape_article_content(session, url)

    assert content == ""
