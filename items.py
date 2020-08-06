# -*- coding: utf-8 -*-



import scrapy


#定义需要存储到数据库中的数据项
class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    article_id = scrapy.Field()
    origin_url = scrapy.Field()
    author = scrapy.Field()
    avatar = scrapy.Field()
    pub_time =scrapy.Field()
    read_count = scrapy.Field()
    like_count = scrapy.Field()
    words_count = scrapy.Field()
    comment_count = scrapy.Field()
    content_href = scrapy.Field()