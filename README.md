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
3. **Smart Termination**: Continues scraping until one of these conditions is met:
   - Running out of listings
   - Finding posts it has already seen (sorted by newest)
   - Reaching the configured posting limit
   - Encountering posts that are too old
4. **LLM Evaluation**: Sends scraped postings to an LLM in batches for relevancy scoring and high-level filtering
5. **Notification Delivery**: Sends the top-k best results to the user via text message

## Tech Stack

- **uv**: Dependency management (compiled to requirements.txt for Google Cloud Function deployment)
- **Scrapy**: Web scraping framework for extracting Craigslist data
- **OpenAI Framework**: LLM integration for intelligent listing evaluation
- **Twilio**: SMS service for sending text message notifications
- **Google Cloud Functions**: Serverless deployment platform with scheduled execution

## Important Notes


## Future Considerations

- I would like to add a multi-threaded appraoch to increase efficiency. At the moment though, this isn't run often enough and doesn't deal with enough volume to justify the extra requirements necessary.