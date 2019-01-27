# -*- coding: utf-8 -*-
import scrapy
from  douban.items import DoubanItem

class ScrapyDoubanSpider(scrapy.Spider):
    name = 'scrapy_douban' #note:this is the real spider name the scrapy crawl command need run this name
    allowed_domains = ['https://movie.douban.com/']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath('//div[@class="article"]//ol[@class = "grid_view"]/li')
        for movie_item in movie_list:
            douban_items = DoubanItem()
            douban_items['serial_num'] = movie_item.xpath('.//div[@class = "item"]//em/text()').extract_first()
            douban_items['movie_name'] = movie_item.xpath('.//div[@class = "info"]//a/span[@class = "title"]/text()')\
                    .extract_first()
            iintroduce_content_item = movie_item.xpath('.//div[@class = "info"]//div[@class = "bd"]/p[1]/text()').extract()
            for introduce_content in iintroduce_content_item:
                introduce_content = "".join(introduce_content.split())
                douban_items['introduce'] = introduce_content
            douban_items['star'] = movie_item.xpath('.//div[@class = "star"]/span[@class = "rating_num"]/text()').extract_first()
            douban_items['evaluate'] = movie_item.xpath('.//div[@class = "star"]/span[4]/text()').extract_first()
            douban_items['describe'] = movie_item.xpath('.//p[@class = "quote"]/span[@class ="inq"]/text()').extract_first()
            yield  douban_items
        next_link = response.xpath('//div[@class = "paginator"]/span[@class = "next"]/link/@href').extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250"+ next_link,callback=self.parse,dont_filter=True)
    pass
