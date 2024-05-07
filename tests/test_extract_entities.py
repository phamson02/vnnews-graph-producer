from vnnews_graph_producer.data_models.entity import Entity, EntityType
from vnnews_graph_producer.entity_extractor import (
    get_entities_from_text,
    get_subwords,
)


def test_get_subword():
    text = "Donald Trump"
    subwords = get_subwords(text)

    assert sorted(subwords) == sorted(["Donald", "Trump"])

    text = "Nguyễn Thị Hồng Chương"

    subwords = get_subwords(text)

    assert sorted(subwords) == sorted(
        [
            "Nguyễn",
            "Thị",
            "Hồng",
            "Chương",
            "Nguyễn Thị",
            "Thị Hồng",
            "Hồng Chương",
            "Nguyễn Thị Hồng",
            "Thị Hồng Chương",
        ]
    )


def test_extract_entities():
    text = "Ông Huệ từ chức, theo thông tin mới từ Ban Chấp hành Trung ương Đảng. Trung ương đánh giá ông Vương Đình Huệ là cán bộ lãnh đạo chủ chốt của Đảng và Nhà nước, được đào tạo cơ bản, trưởng thành từ cơ sở; được phân công giữ nhiều chức vụ lãnh đạo quan trọng của Đảng và Nhà nước.Tuy nhiên, theo báo cáo của Ủy ban Kiểm tra Trung ương và các cơ quan chức năng, ông Đình Huệ đã vi phạm quy định về những điều Đảng viên không được làm, quy định về trách nhiệm nêu gương của cán bộ, Đảng viên, trước hết là Ủy viên Bộ Chính trị, Ủy viên Ban Bí thư, Ủy viên Ban Chấp hành Trung ương Đảng và chịu trách nhiệm người đứng đầu theo các quy định của Đảng và pháp luật của Nhà nước."

    entities = get_entities_from_text(text)

    assert set(entities) == {
        Entity(name="Vương Đình Huệ", type=EntityType.Person),
        Entity(name="Ủy ban Kiểm tra Trung ương", type=EntityType.Organization),
        Entity(name="Bộ Chính trị", type=EntityType.Organization),
        Entity(name="Ban Bí thư", type=EntityType.Organization),
        Entity(name="Ban Chấp hành Trung ương Đảng", type=EntityType.Organization),
    }
