import pymongo
import re

from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.http.request import Request
from scrapy.conf import settings
from spiderman.items import Review as ReviewItem
from spiderman.spiders.parserman import get_review_id, get_review_text, get_review_location, get_author, get_date


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

        #Goes through the next page if any
        next_page_url = sel.xpath('//a[contains(@class, "guiArw sprite-pageNext")]/@href').extract()
        if next_page_url and len(next_page_url) > 0:
            next_page = "http://www.tripadvisor.com" + next_page_url[0]
            yield Request(next_page, self.parse)


        #If the crawler is at a review web site, collect the reviews
        if response.url.find('/ShowUserReviews') != -1:

            reviews = sel.xpath("//div[contains(@id, 'review_')]").extract()
            hotel_id = re.search('d[0-9]+', response.url).group(0)

            for review_text in reviews:
                review_item = ReviewItem()
                review_item['hotel_id'] = hotel_id
                review_item['review_id'] = get_review_id(review_text)
                review_item['review_text'] = get_review_text(review_text)
                review_item['review_date'] = get_date(review_text) 
                review_item['author_location'] = get_review_location(review_text)
                review_item['author_name'] = get_author(review_text)

                yield review_item