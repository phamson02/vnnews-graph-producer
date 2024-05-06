from vnnews_graph_producer.data_models.article import ArticleCategory
from vnnews_graph_producer.data_models.graph import Graph
from vnnews_graph_producer.entity_extractor import get_entities_from_text
from vnnews_graph_producer.scraper import get_today_articles


def main():
    category_to_sources = {
        ArticleCategory.News: [
            "https://tuoitre.vn/rss/thoi-su.rss",
            "http://vtv.vn/trong-nuoc/chinh-tri.rss",
            "https://vtc.vn/rss/thoi-su.rss",
        ],
    }

    articles = get_today_articles(category_to_sources)

    graphs: list[Graph] = []
    for article in articles:
        entities = get_entities_from_text(article.content)
        print(f"Entities in article {article.title}: {entities}")
        graph = Graph.full_graph(entities)
        graphs.append(graph)

    final_graph = graphs[0]
    for graph in graphs[1:]:
        final_graph += graph

    print("Final graph:")
    print(final_graph)


if __name__ == "__main__":
    main()
