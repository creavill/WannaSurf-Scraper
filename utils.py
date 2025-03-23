#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Surf Spot Web Scraper - Utility Functions

This module contains utility functions for the web scraper,
including country list generation and URL construction.
"""

import requests
from bs4 import BeautifulSoup

def make_URL_lists():
    """
    Generate a list of URLs and output files from a country list file.
    
    Returns:
        list: List of tuples (url, output_file)
    """
    try:
        with open("countryList.txt", "r") as f:
            countries = f.readlines()
    except FileNotFoundError:
        print("Error: countryList.txt file not found.")
        print("Creating a new country list from the website...")
        countries = get_countries("https://www.wannasurf.com/spot/index.html")
        with open("countryList.txt", "w") as f:
            for country in countries:
                f.write(country.replace("/spot/", "").replace("/index.html", "") + "\n")
    
    urls = []
    for c in countries:
        country = c.strip()
        output_file = country.split("/")[0] + ".txt"
        url = f"https://www.wannasurf.com/spot/{country}/index.html"
        urls.append((url, output_file))
    
    return urls

def get_countries(url):
    """
    Scrape the list of countries from the main page.
    
    Args:
        url (str): URL of the main page
        
    Returns:
        list: List of country URLs
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching countries: {e}")
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all country links
    country_links = []
    for a in soup.find_all('a', {'class': 'wanna-sublink countryWithSpot'}, href=True):
        country_links.append(a['href'])

    return country_links
