import scrapy
from lianjiaSpider.items import NewHouseItem
from scrapy_selenium import SeleniumRequest

class NewHouseSpider(scrapy.Spider):
    name = "new_house"
    allowed_domains = ["bj.fang.lianjia.com"]
    custom_settings = {
        'ITEM_PIPELINES': {'lianjiaSpider.pipelines.NewHousePipeline': 300},
    }
    base = 3
    limit = 5

    def start_requests(self):
        urls = [f"https://bj.fang.lianjia.com/loupan/pg{self.base + i}/" for i in range(self.limit)]
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        item = NewHouseItem()
        for each in response.xpath('/html/body/div[*]/ul[*]/li[*]/div'):
            item['name'] = each.xpath('.//div[@class="resblock-name"]/h2/a/text()').get()
            item['type'] = each.xpath('.//div[@class="resblock-name"]/span[@class="resblock-type"]/text()').get()
            location = each.xpath('.//div[@class="resblock-location"]/span/text()').getall()
            detailed_location = each.xpath('.//div[@class="resblock-location"]/a/text()').get()
            item['position'] = " / ".join(location) + " / " + detailed_location
            room = each.xpath('.//a[@class="resblock-room"]/span/text()').getall()
            item['house_type'] = " / ".join(room)
            item['area'] = each.xpath('.//div[@class="resblock-area"]/span/text()').get()
            number = each.xpath('.//div[@class="resblock-price"]/div[@class="main-price"]/span[@class="number"]/text()').get()
            item['unit_price'] = number + "元/㎡(均价)"
            item['total_price'] = each.xpath('.//div[@class="resblock-price"]/div[@class="second"]/text()').get()
            yield item