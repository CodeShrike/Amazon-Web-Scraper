import schedule
import time
import json
import asyncio
from app.services import scraper, product_manager
from app.routes import csv_routes

# Read config file and load it into json
def load_config():
    with open("config.json", "r") as f:
        return json.load(f)
    
config = load_config()
interval = config["interval"]

# Process products sequentially as defined in config file and update the CSV automatically
def job():
    config = load_config()
    queries = config["query"]
    for query in queries:
        asyncio.run(scraper.landing_search(query, product_manager))
    csv_routes.update_csv()

# Schedule search to happen at the defined interval
schedule.every(interval).minutes.do(job)

if __name__ == "__main__":
    job()
    while True:
        schedule.run_pending()
        time.sleep(1)
