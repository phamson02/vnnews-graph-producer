import html
import ssl
import urllib.request


def fix_thanhnien_title(title: str) -> str:
    """Fix thanhnien.vn title"""
    if "<![CDATA[" in title:
        title = title.replace("<![CDATA[ ", "").replace("]]>", "")

    # Decode HTML entities
    decoded_str = html.unescape(title)

    # Strip leading and trailing whitespaces
    decoded_str = decoded_str.strip()

    return decoded_str


def open_vnanet_article(article_link: str) -> str:
    """Special handling of links scraped from vnnet rss feed"""

    assert "vnanet.vn" in article_link, "Not a vnanet article"

    # https://vnanet.vnhttps://vnanet.vn/Frontend/TrackingView.aspx?IID=XXXXXX
    # -> https://vnanet.vn/Frontend/TrackingView.aspx?IID=XXXXXX
    article_link = article_link.replace(
        "https://vnanet.vnhttps://vnanet.vn", "https://vnanet.vn"
    )

    try:
        # Set up SSL context to allow legacy TLS versions
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT

        url = urllib.request.urlopen(article_link, context=ctx).geturl()
        return url
    except Exception as e:
        print(f"Error opening {article_link}:\n{e}")
        return article_link
