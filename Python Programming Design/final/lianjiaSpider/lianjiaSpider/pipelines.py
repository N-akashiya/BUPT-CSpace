import codecs
import json

class LianjiaPipeline:
    def open_spider(self, spider):
        try:
            # self.file = codecs.open('bj-renthouse.json', 'w', encoding='utf-8')
            # self.file = codecs.open('sh-renthouse.json', 'w', encoding='utf-8')
            # self.file = codecs.open('gz-renthouse.json', 'w', encoding='utf-8')
            # self.file = codecs.open('sz-renthouse.json', 'w', encoding='utf-8')
            self.file = codecs.open('su-renthouse.json', 'w', encoding='utf-8')
        except Exception as err:
            print(err)
    
    def process_item(self, item, spider):
        dict_item = dict(item)
        json_str = json.dumps(dict_item, ensure_ascii=False) + '\n'
        self.file.write(json_str)
        return item

    def close_spider(self, spider): 
        self.file.close()