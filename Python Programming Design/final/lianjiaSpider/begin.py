from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lianjiaSpider.lianjiaSpider.spiders.spider import LianjiaSpider

process = CrawlerProcess(get_project_settings())

process.crawl(LianjiaSpider)

process.start()