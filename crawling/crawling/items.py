# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlingItem(scrapy.Item):
    city = scrapy.Field()
    temperature = scrapy.Field()
    atm_pressure = scrapy.Field()
    wind_speed = scrapy.Field()

