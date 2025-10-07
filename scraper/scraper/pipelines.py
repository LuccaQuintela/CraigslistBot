# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from utilities.config import Config
from utilities.logger import Logger
from twisted.internet.threads import deferToThread
from twisted.internet.defer import DeferredList
from llm.client import ListingEvaluatorLLMClient

class LLMBufferPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            llm_client=getattr(crawler.spider, "llm_client")
        )

    def __init__(self, llm_client: ListingEvaluatorLLMClient):
        self.batch_size = Config.get('batch_size')
        self.buffer = []
        self.llm_client = llm_client
        self._pending_evaluations = []

    def process_item(self, item, spider):
        self.buffer.append(item)
        
        if len(self.buffer) >= self.batch_size:
            batch = [dict(i) for i in self.buffer]
            self.buffer.clear()
            Logger.log(f"Dispatching LLM evaluation for batch size: {len(batch)}", component="PIPELINE")
            d = deferToThread(self._evaluate_batch, batch)
            self._pending_evaluations.append(d)
        
        return item

    def close_spider(self, spider):
        if self.buffer:
            batch = [dict(i) for i in self.buffer]
            self.buffer.clear()
            Logger.log(f"Flushing final LLM evaluation batch size: {len(batch)}", component="PIPELINE")
            d = deferToThread(self._evaluate_batch, batch)
            self._pending_evaluations.append(d)

        if self._pending_evaluations:
            return DeferredList(self._pending_evaluations, consumeErrors=True)

    def _evaluate_batch(self, batch):
        try:
            self.llm_client.evaluate_listings(batch)
        except Exception as e:
            Logger.error(f"Failed to evaluate listings batch: {e}", component="PIPELINE")
