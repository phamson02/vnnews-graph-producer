from vnnews_graph_producer.data_models.entity import Entity, EntityType, Link
from vnnews_graph_producer.data_models.graph import Graph


def test_entity():
    entity_1 = Entity(name="Vương Đình Huệ", type=EntityType.Person)
    entity_2 = Entity(name="Tập đoàn Thuận An", type=EntityType.Organization)
    entity_3 = Entity(name="Tập đoàn Vingroup", type=EntityType.Organization)

    assert entity_1 != entity_2

    assert set([entity_1, entity_2, entity_3, entity_3]) == {
        entity_1,
        entity_2,
        entity_3,
    }


def test_link():
    entity_1 = Entity(name="Vương Đình Huệ", type=EntityType.Person)
    entity_2 = Entity(name="Tập đoàn Thuận An", type=EntityType.Organization)

    link_1 = Link(source=entity_1, target=entity_2)
    link_2 = Link(source=entity_2, target=entity_1)

    assert link_1 == link_2

    d = {link_1: "link"}

    assert d[link_2] == "link"


def test_graph():
    entity_1 = Entity(name="Vương Đình Huệ", type=EntityType.Person)
    entity_2 = Entity(name="Tập đoàn Thuận An", type=EntityType.Organization)
    entity_3 = Entity(name="Tập đoàn Vingroup", type=EntityType.Organization)
    entity_4 = Entity(name="Tập đoàn Vinamilk", type=EntityType.Organization)

    graph_1 = Graph(
        nodes=[entity_1, entity_2, entity_3],
        graph={
            entity_1: [entity_2, entity_3],
            entity_2: [entity_1],
            entity_3: [entity_1],
        },
    )
    graph_2 = Graph(
        nodes=[entity_1, entity_2, entity_4],
        graph={
            entity_1: [entity_2],
            entity_2: [entity_1, entity_4],
            entity_4: [entity_2],
        },
    )

    new_graph = graph_1 + graph_2

    assert set(new_graph.nodes) == {entity_1, entity_2, entity_3, entity_4}
    assert new_graph.graph == {
        entity_1: [entity_2, entity_3, entity_2],
        entity_2: [entity_1, entity_1, entity_4],
        entity_3: [entity_1],
        entity_4: [entity_2],
    }
