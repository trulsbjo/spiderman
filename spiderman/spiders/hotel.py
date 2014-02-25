import pymongo
import re

from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.http.request import Request
from scrapy.conf import settings
from spiderman.items import Hotel as HotelItem


class Hotel(Spider):

    name = "hotel"
    allowed_domains = ["tripadvisor.com"]
    start_urls = ["http://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels"]


    def parse(self, response):

        sel = Selector(response)

        next_page_url = sel.xpath('//div[contains(@id, "pager_bottom")]//a[contains(@class, "guiArw sprite-pageNext")]/@href').extract()
        if next_page_url and len(next_page_url) > 0:
            next_page = "http://www.tripadvisor.com" + next_page_url[0]
            yield Request(next_page, self.parse)

        hotel_urls = sel.xpath('//a[contains(@class, "property_title")]/@href').extract()
        if hotel_urls:
            for hotel_url in hotel_urls:
                yield Request("http://www.tripadvisor.com" + hotel_url, self.parse)

        if response.url.find('/Hotel_Review') != -1:
            hi = HotelItem()
            hi['hotel_id'] = re.search('d[0-9]+', response.url).group(0)
            hi['hotel_name'] = sel.xpath('//h1[contains(@id, "HEADING")]/text()').extract()[1].strip()
            hi['total_rating'] = sel.xpath('//div[contains(@rel, "v:rating")]//img/@content').extract()[0]
            hi['total_reviews'] = sel.xpath('//div[contains(@class, "rs rating")]//a//span[contains(@property, "v:count")]/text()').extract()[0]
            hi['price_range'] = sel.xpath('//span[contains(@property, "v:pricerange")]/text()').extract()[0].strip()
        yield hi