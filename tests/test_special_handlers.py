from vnnews_graph_producer.scraper.special_handlers import (
    fix_thanhnien_title,
    open_vnanet_article,
)


def test_fix_thanhnien_title():
    input_str = "<![CDATA[ K&yacute; ức kh&oacute; qu&ecirc;n về chuyến bay lịch sử c&ugrave;ng Đại tướng V&otilde; Nguy&ecirc;n Gi&aacute;p ]]>"
    output_str = "Ký ức khó quên về chuyến bay lịch sử cùng Đại tướng Võ Nguyên Giáp"
    assert fix_thanhnien_title(input_str) == output_str


def test_open_vnanet_article():
    article_link = (
        "https://vnanet.vnhttps://vnanet.vn/Frontend/TrackingView.aspx?IID=7357917"
    )
    output_link = "https://www.vietnamplus.vn/indonesia-ky-vong-xuat-khau-sang-trung-quoc-dat-70-ty-usd-post943456.vnp"
    assert open_vnanet_article(article_link) == output_link
