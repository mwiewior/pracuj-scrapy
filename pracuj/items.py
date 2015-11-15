# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PracujItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    jobTitle = scrapy.Field()
    jobLocation = scrapy.Field()
    jobDesc = scrapy.Field()
    jobLink = scrapy.Field()
