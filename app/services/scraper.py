import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime
import concurrent.futures
import time
import asyncio
import aiohttp

# User agents to cycle through in the header in order to successfully get through to Amazons domain with our requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
]

# Headers for the HTML requests to Amazon
HEADERS = {
    'User-Agent': random.choice(USER_AGENTS),
    'Accept-Language': 'da, en-gb, en',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}

# Asynchronously send a GET request to Amazon utilising the headers to mimic browser requests, if an error occurs flag it, then return the response as a BeautifulSoup object to be parsed    
async def async_url_setter(url, session):
    try:
        async with session.get(url, timeout=5) as response:
            response.raise_for_status()
            text = await response.text()
            return BeautifulSoup(text, "lxml")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Find upper boundary of pages for product by selecting pagination elements except for "Next" button, return the last page element found
def get_pages(soup):
    pages = soup.select("a.s-pagination-item:not(.s-pagination-next), span.s-pagination-item:not(.s-pagination-next)")
    if not pages:
        print("Error in pagination: No pages found. Returning 0")
        return 0
    try:
        max_pages = pages[-1]
    except Exception as e:
        print(f"Error in pagination: {e}. Returning 0")
        return 0
    try:
        return int(max_pages.get_text(strip=True))
    except Exception as e:
        print(f"Error converting page text to int: {e}. Returning 0")
        return 0

# Determine the selectors we need to go through by which has the higher count - Noticed this has helped to let the program go through media requests which were otherwise being dropped
def get_selectors(soup):
    a_section_count = len(soup.select(".a-section.a-spacing-base"))
    listitem_count = len(soup.select('div[role="listitem"]'))
    if a_section_count > listitem_count:
        selectors = soup.select(".a-section.a-spacing-base")
    else:
        selectors = soup.select('div[role="listitem"]')
    return selectors

# Process product by selecting appropriate CSS selectors and formatting them into appropriate elements
def process_product(product):
        try:
            title_element = product.find("h2")
            if not title_element:
                return None
            price_element = product.select_one(".a-price-whole,.a-offscreen")
            image_element = product.select_one(".s-image")
            rating_element = product.select_one(".a-icon-alt")
            rating_num_element = product.select_one("a .a-size-base.s-underline-text")
            link_element = product.select_one(".a-link-normal")
            title_extra_element = product.select_one("h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal")

            title_extra = title_extra_element.text.strip() if title_extra_element else ""
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            title = title_element.text.strip()
            combined_title = f"{title} {title_extra}" if title_extra and title_extra != title else title
            price = price_element.text.strip() if price_element else None
            image = image_element.attrs.get("src") if image_element else None
            rating = float(rating_element.text.strip().split(" ")[0]) if rating_element else None
            rating_count = (int(rating_num_element.text.replace(",", "").strip()) if rating_num_element and rating_num_element.text.replace(",", "").strip().isdigit() else None)
            link = f"https://www.amazon.co.uk{link_element['href']}" if link_element else None
            if not rating or not image or not price or not rating_count or not link:
                return None
            return timestamp, combined_title, price, image, rating, rating_count, link
        except Exception as e:
            print(f"Error in processing: {e}")

# Cursory search over the landing page to extract quick details; we set the attributes depending on the appropriate selectors and then ensure we aren't pulling malformed data, skipping it if we do
async def landing_search(query, product_manager):
    formatted_query = query.replace(' ', '+')
    base_url = f"http://www.amazon.co.uk/s?k={formatted_query}"
    
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        main_soup = await async_url_setter(base_url, session)
        if not main_soup:
            return product_manager.get_all_products()
        
        max_pages = get_pages(main_soup)
        print(f"Max pages found: {max_pages}")
        
        urls = [f"{base_url}&page={pg}" for pg in range(1, max_pages + 1)]
        tasks = [async_url_setter(url, session) for url in urls]
        soups = await asyncio.gather(*tasks)
    
    selectors = []
    for soup in soups:
        if soup:
            try:
                selectors.extend(get_selectors(soup))
            except Exception as e:
                print(f"Error processing selectors: {e}")
    
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(None, process_product, selector) for selector in selectors]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        if result:
            product_manager.add_product(*result)
    
    return product_manager.get_all_products()
