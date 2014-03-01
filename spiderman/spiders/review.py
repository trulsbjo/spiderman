import re

from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.http.request import Request
from scrapy.conf import settings
from spiderman.items import Review as ReviewItem
from spiderman.spiders.parserman import *


class Review(Spider):

    name = "review"
    allowed_domains = ["tripadvisor.com"]
    start_urls = ["http://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels"]

    def parse(self, response):

        sel = Selector(response)

        hotel_urls = sel.xpath('//a[contains(@class, "property_title")]/@href').extract()

        next_hotel_page = sel.xpath('//a[contains(@class, "guiArw sprite-pageNext")]/@href').extract()

        if next_hotel_page:
            next_page = "http://www.tripadvisor.com" + next_hotel_page[0]
            yield Request(next_page, self.parse) 
        
        if hotel_urls:
            for hotel_url in hotel_urls:
                yield Request("http://www.tripadvisor.com" + hotel_url, self.parse)
                self.crawler.stats.inc_value('number_of_hotels_crawled')

        review_url = sel.xpath('//div[contains(@class, "quote")]//a/@href').extract()[0]

        if review_url and response.url.find('/Hotel_Review') != -1:
            yield Request("http://www.tripadvisor.com" + review_url, self.parse)

        if response.url.find('/ShowUserReviews') != -1:

            next_page_url = sel.xpath('//a[contains(@class, "guiArw sprite-pageNext")]/@href').extract()
            
            if next_page_url and len(next_page_url) > 0:
                next_page = "http://www.tripadvisor.com" + next_page_url[0]
                yield Request(next_page, self.parse)
     
            reviews = sel.xpath("//div[contains(@id, 'review_')]").extract()
            hotel_id = re.search('d[0-9]+', response.url).group(0)
            
            for review_text in reviews:
                review_item = ReviewItem()
                review_item['hotel_id'] = hotel_id
                review_item['review_id'] = get_review_id(review_text)
                review_item['review_text'] = get_review_text(review_text)
                review_item['review_date'] = get_date(review_text) 
                review_item['review_helpful'] = get_helpfullness(review_text)
                review_item['review_rating'] = get_review_rating(review_text)

                review_item['author_location'] = get_review_location(review_text)
                review_item['author_name'] = get_author(review_text)
                review_item['author_reviews'] = get_author_reviews(review_text)
                review_item['author_hotel_reviews'] = get_author_hotel_reviews(review_text)
                review_item['author_helpful_votes'] = get_author_helpful_votes(review_text)

                yield review_item