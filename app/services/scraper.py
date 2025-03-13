import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime

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

# Send a GET request to Amazon utilising the headers to mimic browser requests, if an error occurs flag it, then return the response as a BeautifulSoup object to be parsed
def url_setter(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  
    return BeautifulSoup(response.text, "lxml")

# Determine the selectors we need to go through by which has the higher count - Noticed this has helped to let the program go through media requests which were otherwise being dropped
def get_selectors(soup):
    a_section_count = len(soup.select(".a-section.a-spacing-base"))
    listitem_count = len(soup.select('div[role="listitem"]'))
    if a_section_count > listitem_count:
        selectors = soup.select(".a-section.a-spacing-base")
    else:
        selectors = soup.select('div[role="listitem"]')
    return selectors


# Cursory search over the landing page to extract quick details; we set the attributes depending on the appropriate selectors and then ensure we aren't pulling malformed data, skipping it if we do
def landing_search(query, product_manager):
    url = f"https://www.amazon.co.uk/s?k={query.replace(' ', '+')}"
    soup = url_setter(url)
    selectors = get_selectors(soup)

    for product in selectors:
        try:
            title_element = product.find("h2")
            if not title_element:
                continue

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
            rating_count = (
           int(rating_num_element.text.replace(",", "").strip()) if rating_num_element and rating_num_element.text.replace(",", "").strip().isdigit() else None 
    )
            link = f"https://www.amazon.co.uk{link_element['href']}" if link_element else None
            if not rating or not image or not price or not rating_count or not link:
                continue
            product_manager.add_product(timestamp, combined_title, price, image, rating, rating_count, link)
        except Exception as e:
            print(f"Error in processing: {e}")

    return product_manager.get_all_products()
