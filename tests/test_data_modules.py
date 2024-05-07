from datetime import datetime
from vnnews_graph_producer.data_models.article import Article, ArticleCategory
from vnnews_graph_producer.data_models.entity import Entity, EntityType
from vnnews_graph_producer.data_models.link import Link
from vnnews_graph_producer.data_models.graph import SubNewsGraph


def test_equal_entity():
    entity_1 = Entity(name="Vương Đình Huệ", type=EntityType.Person)
    entity_2 = Entity(name="Vuong Dinh Hue", type=EntityType.Person)
    entity_3 = Entity(name="Vương Đình Hụê", type=EntityType.Person)

    assert entity_1 == entity_2 == entity_3


def test_equal_link():
    entity_1 = Entity(name="Vương Đình Huệ", type=EntityType.Person)
    entity_2 = Entity(name="Tập đoàn Thuận An", type=EntityType.Organization)

    link_1 = Link(source=entity_1, target=entity_2)
    link_2 = Link(source=entity_2, target=entity_1)

    assert link_1 == link_2

    d = {link_1: "link"}

    assert d[link_2] == "link"


def test_merge_graph():
    entity_1 = Entity(name="Vương Đình Huệ", type=EntityType.Person)
    entity_2 = Entity(name="Tập đoàn Thuận An", type=EntityType.Organization)
    entity_3 = Entity(name="Tập đoàn Vingroup", type=EntityType.Organization)
    entity_4 = Entity(name="Tập đoàn Vinamilk", type=EntityType.Organization)

    article_1 = Article(
        title="Ông Vương Đình Huệ đến thăm Tập đoàn Thuận An và Tập đoàn Vingroup",
        url="https://example.com",
        published_date=datetime.now(),
        category=ArticleCategory.News,
        content="Ông Vương Đình Huệ đã đến thăm Tập đoàn Thuận An và Tập đoàn Vingroup",
    )

    article_2 = Article(
        title="Tập đoàn Vinamilk và Tập đoàn Vingroup ký kết hợp tác",
        url="https://example.com",
        published_date=datetime.now(),
        category=ArticleCategory.News,
        content="Tập đoàn Vinamilk và Tập đoàn Vingroup đã ký kết hợp tác, buổi lễ được ông Vương Đình Huệ chủ trì",
    )

    graph_1 = SubNewsGraph.full_graph_from_article(
        nodes=[entity_1, entity_2, entity_3],
        article=article_1,
    )

    graph_2 = SubNewsGraph.full_graph_from_article(
        nodes=[entity_1, entity_3, entity_4],
        article=article_2,
    )

    new_graph = graph_1 + graph_2

    assert set(new_graph.nodes) == {entity_1, entity_2, entity_3, entity_4}
    assert new_graph.links == {
        Link(source=entity_1, target=entity_2): {article_1},
        Link(source=entity_1, target=entity_3): {article_1, article_2},
        Link(source=entity_1, target=entity_4): {article_2},
        Link(source=entity_2, target=entity_3): {article_1},
        Link(source=entity_3, target=entity_4): {article_2},
    }
