# -*- coding: utf-8 -*-

import scrapy
import json
import re
from douban_movies.items import DoubanMoviesItem

pattern1 = re.compile('(\d+)')
pattern2 = re.compile(r"制片国家/地区:</span> (.+?)<br>")
pattern3 = re.compile('</?\w+[^>]*>')

class DoubanMovie(scrapy.Spider):
    name = 'DoubanSpider'
    base_url = 'https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={}&genres=%E5%89%A7%E6%83%85'

    def start_requests(self):
        for i in range(100):
            url = self.base_url.format(str(i*20))
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        jsondata = json.loads(response.body_as_unicode())
        for info in jsondata['data']:
            yield scrapy.Request(info['url'], self.parse_movies)

    def parse_movies(self, response):
        item = DoubanMoviesItem()
        self.get_title(response, item)
        self.get_rate(response, item)
        self.get_ratingno(response, item)
        self.get_length(response, item)
        self.get_director(response, item)
        self.get_casts(response, item)
        self.get_year(response, item)
        self.get_country(response, item)
        self.get_genre(response, item)
        self.get_tags(response, item)
        return item


    def get_title(self, response, item):
        title = response.xpath("//title/text()").extract()
        if title:
            item['Title'] = title[0].replace(r" (豆瓣)", '').strip()

    def get_rate(self, response, item):
        rate = response.xpath("//strong[@class='ll rating_num']/text()").extract()
        if rate:
            item['Rate'] = float(rate[0])

    def get_ratingno(self, response, item):
        rating_no = response.xpath("//span[@property='v:votes']/text()").extract()
        if rating_no:
            item['Rating_no'] = int(rating_no[0])

    def get_length(self, response, item):
        length = response.xpath("//span[@property='v:runtime']/text()").re(pattern1)
        if length:
            item['Length'] = int(length[0])

    def get_director(self, response, item):
        directors = response.xpath("//a[@rel='v:directedBy']/text()").extract()
        if directors:
            item['Directors'] = directors

    def get_casts(self, response, item):
        casts = response.xpath("//a[@rel='v:starring']/text()").extract()
        if casts:
            item['Casts'] = casts

    def get_year(self, response, item):
        year = response.xpath("//span[@class='year']").re(pattern1)
        if year:
            item['Year'] = year[0]

    def get_country(self, response, item):
        list = ''.join(response.xpath("//div[@id='info']").extract())
        country = pattern2.findall(list)
        if country:
            item['Country'] = country

    def get_genre(self, response, item):
        genre = response.xpath("//span[@property='v:genre']/text()").extract()
        if genre:
            item['Genre'] = genre

    def get_tags(self, response, item):
        tag = ''.join(response.xpath("//div[@class='tags-body']").extract())
        raw_tag = pattern3.sub('', tag).split('\n')
        tags = []
        if raw_tag:
            for t in raw_tag:
                t = t.strip()
                tags.append(t)
        tags = tags[1:-1]
        item['Tags'] = tags
