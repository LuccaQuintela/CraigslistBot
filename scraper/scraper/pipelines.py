# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from utilities.config import Config

class LLMBufferPipeline:
    def __init__(self):
        self.batch_size = Config.get('batch_size')
        self.buffer = []

    def process_item(self, item, spider):
        self.buffer.append(item)

        if len(self.buffer >= self.batch_size):
            # send to async queue
            batch = self.buffer.copy()
            self.buffer.clear()
            # send(batch)
        
        
        return item
