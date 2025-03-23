#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Surf Spot Web Scraper - Main Entry Point

This script serves as the entry point for the web scraper application.
It coordinates the scraping process by reading the list of countries,
creating output files, and calling the appropriate scraping functions.
"""

import argparse
from scraper import scrape_url, web_scraper
from utils import make_URL_lists, get_countries

def main():
    """
    Main function that orchestrates the scraping process.
    Reads the list of countries, creates output files, and calls the scraping functions.
    """
    parser = argparse.ArgumentParser(description='Scrape surf spot data from wannasurf.com')
    parser.add_argument('--country', type=str, help='Specific country to scrape (e.g., "Europe/France")')
    args = parser.parse_args()
    
    if args.country:
        # Scrape a specific country
        country = args.country
        output_file = country.split("/")[0] + ".txt"
        url = f"https://www.wannasurf.com/spot/{country}/index.html"
        scrape_url(url, web_scraper(url, output_file), output_file)
    else:
        # Scrape all countries
        for url, output_file in make_URL_lists():
            print(f"Scraping {url} -> {output_file}")
            scrape_url(url, web_scraper(url, output_file), output_file)

if __name__ == "__main__":
    main()
