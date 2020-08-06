# -*- coding: utf-8 -*-



from scrapy import signals
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse

class SeleniumDownloadMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path=r"D:\python工具\geckodriver.exe")
        #此处executable_path为下载到本地浏览器的驱动程序路径
    def process_request(self,request,spider):
        self.driver.get(request.url)
        #使用driver.get获取到待请求的url
        time.sleep(1)
        #程序等待一秒钟
        try:
            while True:
                showMore = self.driver.find_element_by_class_name("show-more")
                showMore.click()
                time.sleep(0.3)
                if not showMore:
                    break
        except:
            pass
        source = self.driver.page_source
        # 把网页源代码source封装成response对象，再返回给爬虫
        response = HtmlResponse(url=self.driver.current_url,body=source,request=request,encoding='utf-8')
        return response
