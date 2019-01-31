# -*- coding: utf-8 -*-
import scrapy


class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    allowed_domains = ['SpiderCrawl']
    start_urls = ['http://SpiderCrawl/']

    def parse(self, response):
        pass
