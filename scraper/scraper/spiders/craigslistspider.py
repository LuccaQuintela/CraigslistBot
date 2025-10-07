import json
import scrapy
import time
from scraper.scraper.items import ListingItem
from utilities.config import Config
from utilities.logger import Logger

class CraigslistSpider(scrapy.Spider):
    name = "craigslist"
    start_urls = [
        "https://sfbay.craigslist.org/search/bia?postal=94105&query=54cm%20frame%20road%20bike&search_distance=15&sort=date"
    ]

    def __init__(self, llm_client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.llm_client = llm_client

    def parse(self, response):
        """
        Parse the Craigslist search results page to extract individual listing URLs.
        
        This method is called for the initial search page and extracts links to individual
        bike listings from the search results. It iterates through each listing result
        and follows the link to the detailed listing page.
        
        Args:
            response (scrapy.Response): The response object containing the search results page HTML.
            
        Yields:
            scrapy.Request: Request objects to follow each individual listing URL.
        """
        Logger.log("Parsing search results page", component="SPIDER", context={"url": response.url})
        for list_item in response.css("li.cl-static-search-result")[:Config.get('listing_count_limit')]:

            link = list_item.css("a::attr(href)").get()
            if not link:
                Logger.warning("Search result missing href", component="SPIDER")
                continue
            yield response.follow(
                link, 
                callback=self.parse_detail_page,
                meta={'listing_url': link}
            )

    def parse_detail_page(self, response):
        """
        Parse individual Craigslist bike listing page to extract detailed information.
        
        This method extracts comprehensive information from each individual bike listing
        including the title, post ID, bike attributes, description content, and last
        updated timestamp. It handles cases where certain elements may not be present
        on the page.
        
        Args:
            response (scrapy.Response): The response object containing the individual listing page HTML.
            
        Yields:
            dict: A dictionary containing the scraped bike listing data with the following keys:
                - title (str): The listing title
                - post_id (int): The Craigslist post ID
                - attribute_group (dict): Extracted bike attributes as key-value pairs
                - updated_at (str): Last updated timestamp
                - content (str): The main description text of the listing
                - url (str): The original listing URL
        """
        Logger.log("Parsing detail page", component="SPIDER", context={"url": response.meta.get('listing_url', response.url)})
        item = ListingItem()
        item["title"] = "Title Not Found"
        item["content"] = "Content Not Found"
        item["post_id"] = None
        item["attribute_group"] = None
        item["updated_at"] = None
        item["price"] = "Price Not Found"
        item["url"] = response.meta.get('listing_url', response.url)

        posting_data_script = response.css('script#ld_posting_data::text').get()
        if posting_data_script:
            try:
                posting_data_script = posting_data_script.strip()
                posting_data = json.loads(posting_data_script)
                item["title"] = posting_data.get("name", "Title Not Found")
                item["content"] = posting_data.get("description", "Content Not Found")
                item["price"] = posting_data.get("offers", {}).get("price", "Price Not Found")
            except (json.JSONDecodeError, AttributeError) as e:
                Logger.warning(f"Failed to parse JSON-LD data: {e}", component="SPIDER")
                item["title"] = self._extract_title_from_css(response)
                item["content"] = self._extract_content_from_css(response)
        else:
            item["title"] = self._extract_title_from_css(response)
            item["content"] = self._extract_content_from_css(response)

        item["post_id"] = self._extract_post_id(response)
        item["attribute_group"] = self._extract_attributes(response)
        item["updated_at"] = self._extract_updated_timestamp(response)

        yield item
    
    def _extract_title_from_css(self, response):
        """Extract title using CSS selectors with error handling."""
        try:
            title_element = response.css('h1.postingtitle span#titletextonly::text').get()
            return title_element.strip() if title_element else "Title Not Found"
        except Exception as e:
            Logger.warning(f"Failed to extract title from CSS: {e}", component="SPIDER")
            return "Title Not Found"
    
    def _extract_content_from_css(self, response):
        """Extract content using CSS selectors with error handling."""
        try:
            content_elements = response.css('section#postingbody::text').getall()
            if content_elements:
                content = " ".join(text.strip() for text in content_elements if text.strip())
                return content.strip() if content else "Content Not Found"
            return "Content Not Found"
        except Exception as e:
            Logger.warning(f"Failed to extract content from CSS: {e}", component="SPIDER")
            return "Content Not Found"
    
    def _extract_post_id(self, response):
        """Extract post ID with proper integer conversion and error handling."""
        try:
            post_id_text = response.css('div.postinginfos p.postinginfo::text').get()
            if not post_id_text:
                Logger.warning("Post ID element not found", component="SPIDER")
                return None
            
            colon_index = post_id_text.find(':')
            if colon_index == -1:
                Logger.warning(f"Post ID format unexpected: {post_id_text}", component="SPIDER")
                return None
            
            id_part = post_id_text[colon_index + 2:].strip()
            if not id_part:
                Logger.warning("Post ID is empty after parsing", component="SPIDER")
                return None
            
            return int(id_part)
        except ValueError as e:
            Logger.warning(f"Failed to convert post ID to integer: {e}", component="SPIDER")
            return None
        except Exception as e:
            Logger.warning(f"Unexpected error extracting post ID: {e}", component="SPIDER")
            return None
    
    def _extract_updated_timestamp(self, response):
        """Extract updated timestamp with proper error handling."""
        try:
            timestamp_elements = response.css('div.postinginfos p.postinginfo.reveal time.date.timeago::text').getall()
            if len(timestamp_elements) > 1:
                return timestamp_elements[1]
            elif len(timestamp_elements) == 1:
                return timestamp_elements[0]
            else:
                Logger.warning("No timestamp elements found", component="SPIDER")
                return None
        except IndexError:
            Logger.warning("Index error accessing timestamp elements", component="SPIDER")
            return None
        except Exception as e:
            Logger.warning(f"Unexpected error extracting timestamp: {e}", component="SPIDER")
            return None
        
    def _extract_attributes(self, response):
        attrs = {}
        for row in response.css("div.attrgroup div.attr"):
            key = row.css("span.labl::text").get()
            value = row.css('span.valu a::text').get()
            if value is None:
                value = row.css("span.valu::text").getall()
                value = " ".join(v.strip() for v in value)
            else:
                value = value.strip()

            if key and value:
                key = key.strip().rstrip(":")
                attrs[key] = value
        
        return attrs
    
    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super().from_crawler(crawler, *args, **kwargs)
    #     crawler.signals.connect(spider.item_scraped, signal=scrapy.signals.item_scraped)
    #     return spider
    
    # def _stop_spider(self, reason: str):
    #     self.crawler.engine.close_spider(self, reason)

    # def item_scraped(self, item, response, spider):
    #     # self.items_scraped += 1
    #     # if self.items_scraped >= Config.get('listing_count_limit'):
    #     #     self._stop_spider("Maximum items scraped")
    #     pass
            
