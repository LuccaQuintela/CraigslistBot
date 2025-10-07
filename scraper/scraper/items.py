# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ListingItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    post_id = scrapy.Field()
    attribute_group = scrapy.Field()
    updated_at = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
