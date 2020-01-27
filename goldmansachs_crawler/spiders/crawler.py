# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from goldmansachs_crawler.items import GoldmansachsCrawlerItem


class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    allowed_domains = []
    start_urls = [
        'https://github.com/Danbo3004/financial-news-dataset/tree/master/ReutersNews106521/']

    def parse(self, response):
        file_urls = response.xpath(
            '//td[@class="content"]/span/a/@href').extract()
        for href in file_urls:
            absulote_href = response.urljoin(href)
            yield Request(absulote_href, callback=self.parse_news_files)

    def parse_news_files(self, response):
        news_pages = response.xpath(
            '//td[@class="content"]/span/a/@href').extract()
        for news_page in news_pages:
            absulote_news_page = response.urljoin(news_page)
            yield Request(absulote_news_page, callback=self.news_extractor)

    def news_extractor(self, response):
        content = response.xpath('//td[contains(@id, "LC")]/text()').extract()
        l = ItemLoader(item=GoldmansachsCrawlerItem(), response=response)
        l.add_value("content", content)
        return l.load_item()
