import codecs
import json

class NewHousePipeline:
    def open_spider(self, spider):
        try:
            self.file = codecs.open('scrapy-new-house.json', 'w', encoding='utf-8')
        except Exception as err:
            print(err)
    
    def process_item(self, item, spider):
        dict_item = dict(item)
        json_str = json.dumps(dict_item, ensure_ascii=False) + '\n'
        self.file.write(json_str)
        return item

    def close_spider(self, spider): 
        self.file.close()

class SecondhandHousePipeline:
    def open_spider(self, spider):
        try:
            self.file = codecs.open('scrapy-secondhand-house.json', 'w', encoding='utf-8')
        except Exception as err:
            print(err)
    
    def process_item(self, item, spider):
        dict_item = dict(item)
        json_str = json.dumps(dict_item, ensure_ascii=False) + '\n'
        self.file.write(json_str)
        return item

    def close_spider(self, spider):
        self.file.close()