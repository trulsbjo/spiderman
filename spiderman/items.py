from scrapy.item import Item, Field

class Hotel(Item):
    hotel_id = Field()
    hotel_name = Field()
    total_rating = Field()
    total_reviews = Field()
    price_range = Field()

class Review(Item):
	review_id = Field()
	text = Field()