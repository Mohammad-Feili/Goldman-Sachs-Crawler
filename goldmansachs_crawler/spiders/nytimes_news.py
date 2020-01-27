# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy import Selector
from time import sleep
from goldmansachs_crawler.items import GoldmansachsNewyorkTimesItem
from scrapy.loader import ItemLoader


class NytimesNewsSpider(scrapy.Spider):
    name = 'nytimes_news'
    allowed_domains = ['nytimes.com/search?dropmab=false']
    start_urls = [
        'https://www.nytimes.com/search?dropmab=false&endDate=20181231&query=goldman%20sachs&sort=best&startDate=20100101']

    def __init__(self):
        self.driver = webdriver.Chrome(
            r'C:\Users\mohammad feili\Documents\Scrapers\GoldmanSachs_Crawler\goldmansachs_crawler\spiders\chromedriver.exe')

    def parse(self, response):
        self.driver.get(
            'https://www.nytimes.com/search?dropmab=false&endDate=20181231&query=goldman%20sachs&sort=best&startDate=20100101')

        # next Button that works with xhr in json format data for laoding the content in webpages
        load_more_button = self.driver.find_element_by_xpath(
            '//*[@data-testid="search-show-more-button"]')

        while True:
            try:
                load_more_button.click()
                sleep(2.5)
            except:
                break

        sleep(20)
        text = self.driver.page_source
        selector = Selector(text=text)
        L = ItemLoader(item=GoldmansachsNewyorkTimesItem(), response=response)
        ''' news_title = selector.xpath('//a/h4/text()').extract()
        news_body  = selector.xpath(
            '//a/h4/following-sibling::p[1]/text()').extract() '''

        all_news = selector.xpath('//a/h4')
        for news in all_news:
            news_title = news.xpath('.//text()').extract_first()
            news_body = news.xpath(
                './/following-sibling::p[1]/text()').extract_first()

            yield {
                "title": news_title,
                "body": news_body
            }

            L.add_value('title', news_title)
            L.add_value('body', news_body)

            L.load_item()
