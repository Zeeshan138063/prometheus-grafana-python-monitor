from prometheus_client import start_http_server, Counter, Gauge, Summary
import requests
from bs4 import BeautifulSoup
import time
import random

# Define Prometheus metrics
SCRAPES_TOTAL = Counter('scraper_pages_scraped_total', 'Total number of pages scraped')
SCRAPE_ERRORS = Counter('scraper_errors_total', 'Total number of scraping errors')
SCRAPE_DURATION = Summary('scraper_scrape_duration_seconds', 'Time spent scraping pages')
ACTIVE_SCRAPERS = Gauge('scraper_active_scrapers', 'Number of active scrapers')


class WebScraper:
    def __init__(self):
        self.session = requests.Session()

    def scrape_page(self, url):
        try:
            ACTIVE_SCRAPERS.inc()  # Increment active scrapers

            with SCRAPE_DURATION.time():  # Measure scrape duration
                response = self.session.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                # Simulate processing
                time.sleep(random.uniform(0.5, 2))

            SCRAPES_TOTAL.inc()  # Increment successful scrapes
            return True

        except Exception as e:
            SCRAPE_ERRORS.inc()  # Increment error counter
            print(f"Error scraping {url}: {str(e)}")
            return False

        finally:
            ACTIVE_SCRAPERS.dec()  # Decrement active scrapers


def main():
    # Start Prometheus HTTP server
    start_http_server(8000)
    print("Prometheus metrics server started on port 8000")

    # Initialize scraper
    scraper = WebScraper()

    # Sample URLs to scrape
    urls = [
        "http://example.com",
        "http://example.org",
        "http://example.net"
    ]

    # Main scraping loop
    while True:
        for url in urls:
            scraper.scrape_page(url)
        time.sleep(60)  # Wait before next round


if __name__ == "__main__":
    main()