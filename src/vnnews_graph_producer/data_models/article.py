from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from vnnews_graph_producer.entity_extractor.clean_text_content import (
    clean_laodong_text,
    clean_plo_text,
    clean_text,
    clean_vtc_text,
    clean_vtv_text,
)


class ArticleCategory(Enum):
    News = "news"
    Economy = "economy"
    World = "world"
    Entertainment = "entertainment"


@dataclass(frozen=True)
class Article:
    title: str
    url: str
    publish_date: datetime
    category: ArticleCategory
    content: str

    def __repr__(self) -> str:
        return f"Article(\n\ttitle={self.title},\n\turl={self.url},\n\tpublish_date={self.publish_date},\n\tcategory={self.category},\n\tcontent={self.content[:50]}...\n)"


@dataclass(frozen=True)
class ArticleWithNoContent:
    title: str
    url: str
    publish_date: datetime
    category: ArticleCategory

    def __repr__(self) -> str:
        return f"ArticleWithNoContent(\n\ttitle={self.title},\n\turl={self.url},\n\tpublish_date={self.publish_date},\n\tcategory={self.category}\n)"

    def add_content(self, content: str, sanitize: bool = True) -> Article:
        if sanitize:
            content = self._sanitize_content(content)

        content = self.title + ". " + content

        return Article(
            title=self.title,
            url=self.url,
            publish_date=self.publish_date,
            category=self.category,
            content=content,
        )

    def _sanitize_content(self, content: str) -> str:

        # Clean VTV.vn text
        if "vtv.vn" in self.url:
            content = clean_vtv_text(content)

        # Clean PLO text
        if "plo.vn" in self.url:
            content = clean_plo_text(content)

        # Clean VTC text
        if "vtc.vn" in self.url:
            content = clean_vtc_text(content)

        # Clean laodong text
        if "laodong.vn" in self.url:
            content = clean_laodong_text(content)

        # Clean all text
        content = clean_text(content)

        return content
