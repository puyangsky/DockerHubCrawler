# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OfficialImageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    linkmd5 = scrapy.Field()


class ClassifiedImageItem(scrapy.Item):
    repo_name = scrapy.Field()
    star_count = scrapy.Field()
    pull_count = scrapy.Field()
    short_description = scrapy.Field()
    is_automated = scrapy.Field()
    is_official = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
