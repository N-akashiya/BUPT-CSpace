# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NewHouseItem(scrapy.Item):
    # 楼盘名称
    name = scrapy.Field()
    # 类型
    type = scrapy.Field()
    # 地点
    position = scrapy.Field()
    # 房型
    house_type = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 单价
    unit_price = scrapy.Field()
    # 总价
    total_price = scrapy.Field()


class SecondhandHouseItem(scrapy.Item):
    # 小区名称
    community = scrapy.Field()
    # 地点
    position = scrapy.Field()
    # 房型等信息
    house_info = scrapy.Field()
    # 单价
    unit_price = scrapy.Field()
    # 总价
    total_price = scrapy.Field()