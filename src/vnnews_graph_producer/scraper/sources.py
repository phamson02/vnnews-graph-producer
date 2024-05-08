from vnnews_graph_producer.data_models.article import ArticleCategory, Source


ECONOMY_SOURCES = [
    Source(rss_link=link, category=ArticleCategory.Economy)
    for link in [
        "https://vnexpress.net/rss/kinh-doanh.rss",
        "http://vtv.vn/kinh-te.rss",
        "http://vtv.vn/kinh-te/bat-dong-san.rss",
        "http://vtv.vn/kinh-te/tai-chinh.rss",
        "http://vtv.vn/kinh-te/thi-truong.rss",
        "https://laodong.vn/rss/kinh-doanh.rss",
        "https://tuoitre.vn/rss/kinh-doanh.rss",
        "https://thanhnien.vn/rss/kinh-te.rss",
        "https://nld.com.vn/rss/kinh-te.rss",
        "https://nld.com.vn/rss/thi-truong.rss",
        "https://www.nguoiduatin.vn/rss/kinh-doanh.rss",
        "https://kienthuc.net.vn/rss/kinh-doanh-9.rss",
        "https://kinhtedothi.vn/kinh-te.rss",
        "https://vtcnews.vn/rss/kinh-te.rss",
        "https://vnanet.vn/vi/rss/kinh-te-4.rss",
        "https://infonet.vietnamnet.vn/rss/thi-truong.rss",
        "https://plo.vn/rss/kinh-te-13.rss",
        "https://www.sggp.org.vn/rss/kinh-te-89.rss",
        "https://toquoc.vn/rss/kinh-te-2.rss",
    ]
]

ENTERNTAINMENT_SOURCES = [
    Source(rss_link=link, category=ArticleCategory.Entertainment)
    for link in [
        "https://vnexpress.net/rss/giai-tri.rss",
        "http://vtv.vn/van-hoa-giai-tri.rss",
        "http://vtv.vn/van-hoa-giai-tri/dien-anh.rss",
        "http://vtv.vn/van-hoa-giai-tri/am-nhac.rss",
        "http://vtv.vn/van-hoa-giai-tri/sao.rss",
        "https://laodong.vn/rss/van-hoa-giai-tri.rss",
        "https://tuoitre.vn/rss/giai-tri.rss",
        "https://tuoitre.vn/rss/van-hoa.rss",
        "https://thanhnien.vn/rss/giai-tri.rss",
        "https://thanhnien.vn/rss/van-hoa.rss",
        "https://nld.com.vn/rss/giai-tri.rss",
        "https://www.nguoiduatin.vn/rss/giai-tri.rss",
        "https://kienthuc.net.vn/rss/giai-tri-11.rss",
        "https://vtcnews.vn/rss/van-hoa-giai-tri.rss",
        "https://vnanet.vn/vi/rss/nghe-thuat-van-hoa-va-giai-tri-1.rss",
        "https://plo.vn/rss/van-hoa-16.rss",
        "https://www.sggp.org.vn/rss/van-hoa-giai-tri-186.rss",
        "https://toquoc.vn/rss/van-hoa-10.rss",
        "https://giaoducthudo.giaoducthoidai.vn/rss/van-hoa",
    ]
]

NEWS_SOURCES = [
    Source(rss_link=link, category=ArticleCategory.News)
    for link in [
        "https://vnexpress.net/rss/thoi-su.rss",
        "https://vtv.vn/trong-nuoc.rss",
        "http://vtv.vn/trong-nuoc/chinh-tri.rss",
        "http://vtv.vn/trong-nuoc/xa-hoi.rss",
        "http://vtv.vn/trong-nuoc/phap-luat.rss",
        "https://laodong.vn/rss/thoi-su.rss",
        "https://laodong.vn/rss/xa-hoi.rss",
        "https://tuoitre.vn/rss/thoi-su.rss",
        "https://thanhnien.vn/rss/thoi-su.rss",
        "https://nld.com.vn/rss/thoi-su.rss",
        "https://www.nguoiduatin.vn/rss/chinh-tri-xa-hoi.rss",
        "https://www.nguoiduatin.vn/rss/phap-luat.rss",
        "https://kienthuc.net.vn/rss/xa-hoi-24.rss",
        "https://kinhtedothi.vn/thoi-su.rss",
        "https://vtcnews.vn/rss/thoi-su.rss",
        "https://infonet.vietnamnet.vn/rss/doi-song.rss",
        "https://vnanet.vn/vi/rss/chinh-tri-11.rss",
        "https://vnanet.vn/vi/rss/xa-hoi-14.rss",
        "https://plo.vn/rss/thoi-su-1.rss",
        "https://plo.vn/rss/thoi-su/chinh-tri-2.rss",
        "https://www.sggp.org.vn/rss/chinh-tri-24.rss",
        "https://www.sggp.org.vn/rss/xa-hoi-199.rss",
        "https://toquoc.vn/rss/thoi-su-1.rss",
        "https://giaoducthudo.giaoducthoidai.vn/rss/thoi-su   ",
    ]
]

WORLD_NEWS_SOURCES = [
    Source(rss_link=link, category=ArticleCategory.World)
    for link in [
        "https://vnexpress.net/rss/the-gioi.rss",
        "http://vtv.vn/the-gioi.rss",
        "http://vtv.vn/the-gioi/tin-tuc.rss",
        "http://vtv.vn/the-gioi/the-gioi-do-day.rss",
        "https://laodong.vn/rss/the-gioi.rss",
        "https://tuoitre.vn/rss/the-gioi.rss",
        "https://thanhnien.vn/rss/the-gioi.rss",
        "https://nld.com.vn/rss/quoc-te.rss",
        "https://kienthuc.net.vn/rss/the-gioi-25.rss",
        "https://kinhtedothi.vn/quoc-te.rss",
        "https://vtcnews.vn/rss/the-gioi.rss",
        "https://infonet.vietnamnet.vn/rss/the-gioi.rss",
        "https://plo.vn/rss/quoc-te-8.rss",
        "https://www.sggp.org.vn/rss/the-gioi-143.rss",
        "https://toquoc.vn/rss/the-gioi-5.rss",
    ]
]


SOURCES = ECONOMY_SOURCES + ENTERNTAINMENT_SOURCES + NEWS_SOURCES + WORLD_NEWS_SOURCES


EXCLUDED_SOURCES = [
    "video.",
    "video/",
    "ban-tin/",
    "video-xa-hoi/",
]
