import scrapy
from lianjiaSpider.items import SecondhandHouseItem
from scrapy_selenium import SeleniumRequest

class SecondhandHouseSpider(scrapy.Spider):
    name = "secondhand_house"
    allowed_domains = ["bj.lianjia.com"]
    custom_settings = {
        'ITEM_PIPELINES': {'lianjiaSpider.pipelines.SecondhandHousePipeline': 400},
    }
    base = 3
    limit = 5
    
    def start_requests(self):
        cookies = {
            "ftkrc_": "f9000d79-1bf9-4c90-be0c-5048060758df",
            "Hm_lvt_46bf127ac9b856df503ec2dbf942b67e": "1732529078",
            "lfrc_": "c15425df-31ce-46c4-8c94-2e87a0da1d03",
            "lianjia_ssid": "19288f6e-958e-4c80-9bbc-79dd69069da5",
            "lianjia_token_secure": "2.001568b67a7f38d8eb04c59f4b8d168b56",
            "lianjia_token": "2.001568b67a7f38d8eb04c59f4b8d168b56",
            "lianjia_uuid": "5a3e622c-f3ee-46f6-a366-f0b542495bf6",
            "login_ucid": "2000000263783293",
            "security_ticket": "ruogaWOEmele2hnBUumbYGfwNJ1UKlIRr+pUVGn6DtVie00VN2js8+TX5M3JT8bPF1hGiwXjtY6HudRiPm+whSKu9n6Z7bX92b9qixqelj6ayVJtorashGgDC6JZ5WXhkm9ubJW97QXLaCa9Hz45z+8FZX0cl/xD8P25xTRSsjM=",
        }
        urls = [f"https://bj.lianjia.com/ershoufang/pg{self.base + i}/" for i in range(self.limit)]
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse, cookies=cookies)
                                  
    def parse(self, response):
        item = SecondhandHouseItem()
        for each in response.xpath('/html/body/div[*]/div[@class="leftContent"]/ul[*]/li'):
            item['community'] = each.xpath('.//div[@class="positionInfo"]/a[1]/text()').get()
            item['position'] = each.xpath('.//div[@class="positionInfo"]/a[2]/text()').get()
            item['house_info'] = each.xpath('.//div[@class="houseInfo"]/text()').get()
            item['unit_price'] = each.xpath('.//div[@class="unitPrice"]/span/text()').get()
            item['total_price'] = each.xpath('.//div[@class="totalPrice totalPrice2"]/span/text()').get() + "万"
            yield item
