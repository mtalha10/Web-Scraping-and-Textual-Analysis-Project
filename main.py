# to run python main.py --input input.xlsx --output output_data.xlsx
import argparse
import pandas as pd
from scraper import scrape_articles
from text_analysis import analyze_text_files

def main():
    parser = argparse.ArgumentParser(description="Web Scraping and Text Analysis Tool")
    parser.add_argument("--input", required=True, help="Path to input Excel file")
    parser.add_argument("--scraped_dir", default="extracted_articles", help="Directory to save scraped articles")
    parser.add_argument("--output", required=True, help="Path to output Excel file")
    args = parser.parse_args()

    # Scrape articles
    scrape_articles(args.input, args.scraped_dir)

    # Analyze scraped articles
    analyze_text_files(args.scraped_dir, args.output)

if __name__ == "__main__":
    main()
