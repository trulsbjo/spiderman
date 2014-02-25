# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Hotel(Item):
    # define the fields for your item here like:
    hotel_id = Field()
    hotel_name = Field()
    total_rating = Field()
    total_reviews = Field()
    price_range = Field()