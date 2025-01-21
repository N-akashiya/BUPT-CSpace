# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class RentItem(scrapy.Item):
    # 板块
    plate = scrapy.Field()
    # 朝向
    orien = scrapy.Field()
    # 房型
    house_type = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 房租
    rental = scrapy.Field()