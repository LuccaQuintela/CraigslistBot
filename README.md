# Craigslist Bot

## Problem Statement

People use Craigslist extensively in San Francisco, but finding quality listings can be tedious due to the abundance of poor or irrelevant posts. This bot solves the problem of manually filtering through countless listings to find good deals.

**Target Search**: 54cm frame road bike with components comparable to Shimano 105's within 15 miles of 94105

## Solution Overview

This bot automates the entire process of finding quality Craigslist listings by:

1. **Automated Scraping**: Scrapes Craigslist every 120 minutes to identify new listings
2. **Intelligent Filtering**: Uses an LLM to evaluate whether listings are good matches based on criteria
3. **Smart Notifications**: Sends text message alerts with links to the best listings

## Approach

The bot is deployed as a Google Cloud Function that runs on a scheduled basis (every 120 minutes). Here's how it works:

1. **Configuration Loading**: Extracts relevant scraping parameters from a config file
2. **Targeted Scraping**: Runs a bot scraper to find Craigslist postings matching the search criteria
3. **LLM Evaluation**: Sends scraped postings to an LLM in batches for relevancy scoring and high-level filtering
4. **Notification Delivery**: Sends the top-k best results to the user via text message

## Tech Stack

- **uv**: Dependency management (compiled to requirements.txt for Google Cloud Function deployment)
- **Scrapy**: Web scraping framework for extracting Craigslist data
- **OpenAI Framework**: LLM integration for intelligent listing evaluation
- **Twilio**: SMS service for sending text message notifications
- **Google Cloud Functions**: Serverless deployment platform with scheduled execution

## Important Notes
- I am currently using Twilio to send out messages, this works great except for the fact that U.S law requires a series of registration steps in order to effectively send SMS messages normally that I can't fill out since I'm not legally a business and would take around 7 days to process anyway. Since I'm on a time crunch and this isn't actually getting deployed to a real production environment, I opted to use their WhatsApp functionality instead for now.

## Future Considerations

- Currently, this service will both scrape and evaluate duplicates. The first thing I would like to do in the future, given more time, is implement Redis as a cache to prevent not only wasting compute time on listings that are already seen, but also to prevent sending messages of the same listings to the user. 
- At the moment, the LLM only processes text information to make its decisions, e.g. the bio, the attributes, the name of the bike, etc. However, especially on services like Craigslist, people often leave out relevant information and so if the LLM could process the images of the items as well, it could make more informed decisions about whether the item matches the description
- At a completely deeper level of complexity, in the future could be coupled with an agentic system that automatically sends emails/messages to the sellers with an offer and can negotiate for you based on a provided style(e.g. lowballing, listing price, bidding, etc.). Could either use a score threshold to determine what to send offers to or use human in the loop depending on use case. Would ensure human in the loop before actually purchasing anything.  
- Right now, my custom llm client class only handles OpenAI models, I would like to eventually make it easy to swap models in case it ever becomes helpful.
- A preprocessing LLM step could also be included to simplify configuration. In this case, the user wants to find “54cm frame road bike with components comparable to Shimano 105’s within 15 miles of 94105”. While this makes sense to an LLM or to a human, in order to search craigslist properly, this query must be separated out. Including details like "components comparable to Shimano 105s" in the search within craigslist will interfere with your search results in a destructive manner. But it's still important information for comparison. So the configuration file separates these components out in a way that easily allows the scraper and llm to find the information it needs. However, you need to separate this manually at the moment and that can be ineffective. Allowing a dev to write in simple language what they're looking for and having the LLM deal with separation will increase efficiency in the future.
- In the future, a RAG component could be helpful. For example, in this use case, the LLM can understand everything about its task very effectively, however, it might not know details about the Shimano 105 depending on its training. So the LLM will have to guess whether a bike matches that description, which can lead to hallucinations and such. Therefore, having a system that can look up that information, determine what components make up a Shimano 105 and therefore make the proper comparisons, would increase accuracy significantly. 
   - This can be combined with the previous config preprocessing step. You would be able to set a single query, the llm separates out all relevant components and anything that requires clarification can be looked up to define a more detailed configuration. 