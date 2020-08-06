# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Scrapy_jianshuSpider.items import ArticleItem
import os
global i

i = 990

class JsSpiderSpider(CrawlSpider):
    name = 'js_spider'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),

    )

    def parse_detail(self, response):
        title = response.xpath("//*[@id='__next']/div[1]/div/div/section[1]/h1/text()").get()
        avatar = response.xpath("//*[@id='__next']/div[1]/div/div/section[1]/div[1]/div/a/img/@src").get()
        author = response.xpath("//*[@id='__next']/div[1]/div/div/section[1]/div[1]/div/div/div[1]/span/a/text()").get()
        pub_time = response.xpath("//*[@id='__next']/div[1]/div/div/section[1]/div[1]/div/div/div[2]/time/text()").get()
        # 分析url得到两种形式：
        # https://www.jianshu.com/p/a0199fe1507c?utm_campaign=maleskine&utm_content=note&utm_medium=pc_all_hots&utm_source=recommendation
        # https://www.jianshu.com/p/a0199fe1507c
        origin_url = response.url
        # url被问号？分割后返回一个列表['https://www.jianshu.com/p/a0199fe1507c', 'utm_campaign=maleskine&utm_content=note&utm_medium=pc_all_hots&utm_source=recommendation']
        # 或者得到列表['https://www.jianshu.com/p/a0199fe1507c']
        url = origin_url.split('?')[0]
        article_id = url.split('/')[-1]
        # 文章内容，包括所有的html标签，而不是纯文本信息
        content = response.xpath("//*[@id='__next']/div[1]/div/div/section[1]/article").get()
        #将文章详情页content内容分别存储到本地不同的txt文本中
        global i
        content_str = str(content)
        with open("F:\python项目\文本\%04d.txt" % i, "w", encoding='utf-8') as f:
            if f.write(content_str):
                i = i + 1
            f.close()

        content_href = str(response.request.headers[b'Referer'])[2:-1]
        words_count = response.xpath("//*[@id='__next']/div[1]/div/div/section[1]/div[1]/div/div/div[2]/span[2]/text()").get()
        comment_count = response.xpath("//*[@id='note-page-comment']/section/h3/div[1]/span[2]/text()").get()
        like_count = response.xpath("//span[@class='likes-count']/text()").get()
        read_count = response.xpath("//*[@id="'__next'"]/div[1]/div/div/section[1]/div[1]/div/div/div[2]/span[3]/text()").get()


        words_count = words_count.split(" ")[-1] #使用空格分隔成列表后取列表最后一个值
        if comment_count:
            comment_count = int(comment_count.split(" ")[-1])
        if like_count:
            like_count = int(like_count.split(" ")[-1])
        if  read_count:
            read_count = int(read_count.split(" ")[-1])


        item = ArticleItem(
            title = title,
            content = content,
            avatar = avatar,
            author = author,
            pub_time = pub_time,
            origin_url = origin_url,
            article_id = article_id,
            words_count = words_count,
            comment_count = comment_count,
            like_count = like_count,
            read_count = read_count,
            content_href = content_href,
        )
        yield item #将item中的数据项传到pipelines管道中进行存储

