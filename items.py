# -*- coding: utf-8 -*-

import scrapy

class DoubanMoviesItem(scrapy.Item):
    Title = scrapy.Field()
    Rate = scrapy.Field()
    Rating_no = scrapy.Field()
    Length = scrapy.Field()
    Directors = scrapy.Field()
    Casts = scrapy.Field()
    Year = scrapy.Field()
    Country = scrapy.Field()
    Genre = scrapy.Field()
    Tags = scrapy.Field()
