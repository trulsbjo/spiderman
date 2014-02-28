from scrapy.item import Item, Field

class Hotel(Item):
    hotel_id = Field()
    hotel_name = Field()
    total_rating = Field()
    total_reviews = Field()
    price_range = Field()

class Review(Item):
	hotel_id = Field()
	review_id = Field()
	review_text = Field()
	review_date = Field()
	review_helpful = Field()
	review_rating = Field()

	author_location = Field()
	author_name = Field()
	author_reviews = Field()
	author_hotel_reviews = Field()
	author_helpful_votes = Field()
	author_id = Field()