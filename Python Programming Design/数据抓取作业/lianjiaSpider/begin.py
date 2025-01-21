from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lianjiaSpider.spiders.new_house import NewHouseSpider
from lianjiaSpider.spiders.secondhand_house import SecondhandHouseSpider

process = CrawlerProcess(get_project_settings())

process.crawl(NewHouseSpider)
process.crawl(SecondhandHouseSpider)

process.start()