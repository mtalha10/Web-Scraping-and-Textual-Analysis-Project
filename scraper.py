import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to extract article text from URL
def extract_article(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.find("title").get_text().strip()
            article_text = "\n".join(p.get_text().strip() for p in soup.find_all("p"))
            return title, article_text
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1}: Error fetching {url}: {e}")
            time.sleep(delay)
    logging.error(f"Failed to fetch article from {url} after {retries} attempts.")
    return None, None

# Function to scrape articles from input Excel file
def scrape_articles(input_file, output_dir):
    df = pd.read_excel(input_file)
    os.makedirs(output_dir, exist_ok=True)

    for index, row in df.iterrows():
        url_id = row["URL_ID"]
        url = row["URL"]
        logging.info(f"Processing URL_ID {url_id}: {url}")
        title, article_text = extract_article(url)

        if title and article_text:
            filename = os.path.join(output_dir, f"{url_id}.txt")
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"{title}\n\n{article_text}")
            logging.info(f"Article saved: {filename}")
        else:
            logging.error(f"Failed to extract article from URL_ID {url_id}: {url}")

    logging.info("Scraping completed.")
