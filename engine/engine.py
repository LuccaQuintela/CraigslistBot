from typing import List
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.scraper.spiders.craigslistspider import CraigslistSpider
from utilities.config import Config
from messager.message_client import MessageClient

class Engine:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Engine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            Engine._initialized = True
            self.buffer = []

    def _run_scraper(self):
        settings = get_project_settings()
        settings.update({
            "FEEDS": {
                "test.json": {
                    "format": "json",
                    "overwrite": True,
                }
            }
        })

        process = CrawlerProcess(settings)
        process.crawl(CraigslistSpider)
        process.start()

    def run(self):
        self._run_scraper()

    def insert_to_buffer(self, list: List[tuple]):
        self.buffer.extend(list)

    def final_processing(self):
        sorted(self.buffer)
        for listing in self.buffer[:Config.get('top_k')]:
            if listing[0] >= Config.get('threshold'):
                msg = f"{listing[1]}"
                # MessageClient.send(msg)
                print(msg)
            else:
                break
