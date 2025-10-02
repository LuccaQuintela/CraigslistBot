import json
import scrapy


class CraigslistSpider(scrapy.Spider):
    name = "craigslist"
    start_urls = [
        "https://sfbay.craigslist.org/search/bia?postal=94105&query=54cm%20frame%20road%20bike&search_distance=15&sort=date"
    ]

    def parse(self, response):
        script = response.css("script#ld_searchpage_results::text").get()
        if script: 
            data = json.loads(script)

            yield data

            # item_list = data.get("itemListElement", [])
            # for item in item_list:
            #     product = item.get("item", {})
            #     yield {
            #         # "title": product.get("name"),
            #         # "url": product.get("url"),
            #         # "datePosted": product.get("datePosted"),
            #         "product": product,
            #     }