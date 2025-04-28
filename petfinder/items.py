# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PetfinderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    pet_id = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    species = scrapy.Field()
    profile = scrapy.Field()
    amount = scrapy.Field()
    vaccinated = scrapy.Field()
    dewormed = scrapy.Field()
    spayed = scrapy.Field()
    condition = scrapy.Field()
    body = scrapy.Field()
    color = scrapy.Field()
    location = scrapy.Field()
    posted = scrapy.Field()
    price = scrapy.Field()
    uploader_type = scrapy.Field()
    uploader_name = scrapy.Field()
    status = scrapy.Field()
