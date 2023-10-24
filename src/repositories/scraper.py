from bs4 import BeautifulSoup
from selenium import webdriver
import time

class ScraperRepository:
    def scrape(self, url, sleep=1):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("--no-sandbox")

        with webdriver.Chrome(options=options) as driver:
            driver.get(url)  # Fetch url
            time.sleep(sleep)  # Wait for JS to load
            soup = BeautifulSoup(driver.page_source, "lxml")
        return soup
