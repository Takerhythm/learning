from mini_scrapy.core.spider import Spider


class BSpider(Spider):
    name = 'baidu'
    start_urls = ['http://www.baidu.com']