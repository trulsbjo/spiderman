import pymongo
import re

from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.http.request import Request
from scrapy.conf import settings
from spiderman.items import Review as ReviewItem


class Review(Spider):

    name = "review"
    allowed_domains = ["tripadvisor.com"]
    start_urls = ["http://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels"]


    def parse(self, response):

        sel = Selector(response)

        #Get the urls from all the hotels (30 per page)
        hotel_urls = sel.xpath('//a[contains(@class, "property_title")]/@href').extract()
        
        #Goes through the hotels and run parse method (recursive) on the url
        if hotel_urls:
            for hotel_url in hotel_urls:
                yield Request("http://www.tripadvisor.com" + hotel_url, self.parse)

        #Extract the first review url
        review_url = sel.xpath('//div[contains(@class, "quote")]//a/@href').extract()[0]

        #Goes through the first review page
        if review_url and response.url.find('/Hotel_Review') != -1:
            yield Request("http://www.tripadvisor.com" + review_url, self.parse)

        #If the crawler is at a review web site, collect the reviews
        if response.url.find('/ShowUserReviews') != -1:

            reviews_text = sel.xpath("//div[@class='entry']//p").extract()

            for review_text in (reviews_text):
                review_item = ReviewItem()
                review_item['text'] = review_text
                yield review_item