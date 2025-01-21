import scrapy
from lxml import etree
from lianjiaSpider.items import RentItem
from scrapy_selenium import SeleniumRequest

def get_districts(city_name):
    target_url = "https://{}.lianjia.com/zufang/".format(city_name)
    return target_url

def get_start_urls(city_name, name):
    urls = []
    for i in name:
        url = "https://{}.lianjia.com/zufang/{}/pg1/".format(city_name, i)
        urls.append(url)
    return urls

class LianjiaSpider(scrapy.Spider):
    """
    爬取流程：城市首页 -> 区域列表 -> 板块列表 -> 房源详情
    """
    name = "rent_house"
    allowed_domains = ["lianjia.com"]
    city_name = "bj"
    # city_name = "sh"
    # city_name = "gz"
    # city_name = "sz"
    # city_name = "su"

    def start_requests(self):
        url = get_districts(self.city_name)
        yield SeleniumRequest(url=url, callback=self.parse_district, meta={'city_name': self.city_name, 'proxy': self.settings.get('HTTP_PROXY')})

    def parse_district(self, response):
        city_name = response.meta['city_name']
        html_string = response.text
        html_tree = etree.HTML(html_string)
        districts = html_tree.xpath('//ul[@data-target="area" and @class=""]/li/a/@href')
        districts = [district.split("/")[2] for district in districts]
        
        d_urls = get_start_urls(city_name, districts)
        for url in d_urls:
            yield SeleniumRequest(url=url, callback=self.parse_plate, meta={'city_name': city_name, 'proxy': response.meta['proxy']})

    def parse_plate(self, response):
        city_name = response.meta['city_name']
        html_string = response.text
        html_tree = etree.HTML(html_string)
        plates = html_tree.xpath('//ul[@data-target="area" and not(@class)]/li/a/@href')
        plates = [plate.split("/")[2] for plate in plates]
        
        seen_plates = set() # 去重
        for plate in plates:
            if plate not in seen_plates:
                seen_plates.add(plate)
                url = "https://{}.lianjia.com/zufang/{}/pg1/".format(city_name, plate)
                yield SeleniumRequest(url=url, callback=self.parse, meta={'city_name': city_name, 'plate': plate, 'proxy': response.meta['proxy']})

    def parse(self, response):
        city_name = response.meta['city_name']
        plate = response.meta['plate']
        # 检查页面是否为空
        isempty = bool(response.xpath('//div[@class="content__list--empty"]'))
        if not isempty:
            page = response.url.split("/")[-2]
            for each in response.xpath('//div[@class="content__list--item"]'):
                item = RentItem()
                item['plate'] = each.xpath('.//p[@class="content__list--item--des"]/a[2]/text()').get()
                if item['plate'] is not None:
                    item['plate'] = item['plate'].strip()
                
                description = each.xpath('.//p[@class="content__list--item--des"]').xpath('string(.)').get()
                if description:
                    description = ''.join(description).replace('\n', '').strip()
                    parts = [part.strip() for part in description.split('/') if part.strip()]
                    if len(parts) >= 4:
                        item['orien'] = ' '.join(parts[2].split())
                        item['house_type'] = parts[3]
                        item['area'] = parts[1].replace('㎡', '').strip() + "平方米"

                item['rental'] = each.xpath('.//span/em/text()').get() + "元/月"
                yield item
            
            if page != "pg100":
                next_page = int(page[2:]) + 1
                next_url = "https://{}.lianjia.com/zufang/{}/pg{}/".format(city_name, plate, next_page)
                yield scrapy.Request(next_url, callback=self.parse, meta={'city_name': city_name, 'plate': plate, 'page': next_page, 'proxy': response.meta['proxy']})