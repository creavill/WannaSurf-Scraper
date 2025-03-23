#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Surf Spot Web Scraper - Core Scraping Functionality

This module contains the core web scraping functions for extracting
surf spot data from wannasurf.com. It handles both table-based and
spot detail pages.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from data_processor import clean_df

def web_scraper(url, output_file):
    """
    Main scraper function that dispatches to the appropriate extraction function
    based on page structure.
    
    Args:
        url (str): URL to scrape
        output_file (str): Path to output file for storing results
        
    Returns:
        pandas.DataFrame or dict: Extracted data
    """
    # Send a GET request to the URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table with id='wanna-table'
    table = soup.find('table', {'id': 'wanna-table'})

    if table is None:
        # If no table found, this is a spot detail page
        return extract_spot_data(soup, url, output_file)
    else:
        # This is a listing page with a table
        return extract_table_data(table)

def extract_spot_data(soup, url, output_file):
    """
    Extract data from individual surf spot pages.
    
    Args:
        soup (BeautifulSoup): Parsed HTML content
        url (str): URL of the page
        output_file (str): Path to output file
        
    Returns:
        dict: Extracted spot data
    """
    # Find all span elements with class="wanna-item-label-gps" or "wanna-item-label"
    labels = soup.find_all('span', {'class': 'wanna-item-label-gps'})
    labels += soup.find_all('span', {'class': 'wanna-item-label'})

    # Create a dictionary to store the data, including the spot's path in the site structure
    data = {"url": url.replace("/index.html", "").replace("https://www.wannasurf.com/spot/", "")}

    # Loop through the labels and extract the text and value
    for label in labels:
        # Get the text and value from the label
        text = label.text.strip()
        temp = label.next_sibling

        # Handle cases where there is no value
        if temp is None:
            value = "None"
        else:
            value = temp.text.strip()

        # Add the data to the dictionary
        data[text] = value

    # Append the data to the output file
    with open(output_file, "a") as f:
        f.write(str(data) + "\n")
        
    return data

def extract_table_data(table):
    """
    Extract data from tables that list multiple surf spots.
    
    Args:
        table (BeautifulSoup): Table element containing surf spot data
        
    Returns:
        pandas.DataFrame: Processed table data
    """
    # Extract the table headers
    headers = [th.text.strip() for th in table.find('thead').find_all('th')]

    # Extract the table data
    data = []
    for row in table.find('tbody').find_all('tr'):
        rows = [td.text.strip() for td in row.find_all('td')]
        
        # Check if there is a <a href> tag in the first column
        if row.find('td').find('a'):
            if "sublink" not in headers:
                headers.append("sublink")
            # Extract the URL
            link_url = row.find('td').find('a')['href']
            # Add a new column "sublink" with the URL
            rows.append(link_url)
            
        data.append(rows)

    # Create a DataFrame with the extracted data
    df = pd.DataFrame(data, columns=headers)
    
    # Clean the dataframe and return
    cleaned_df = clean_df(df)
    print(cleaned_df)
    print("\n")
    return cleaned_df

def scrape_url(url, df, output_file):
    """
    Recursively scrape URLs and their sub-URLs.
    
    Args:
        url (str): Base URL to scrape
        df (pandas.DataFrame): DataFrame containing links to sub-URLs
        output_file (str): Path to output file
    """
    base_url = 'https://www.wannasurf.com'
    
    # If df is None (error occurred), return early
    if df is None:
        return
        
    # If df is a dictionary, it's a spot detail, no need to recurse
    if isinstance(df, dict):
        return
        
    # If df has sublinks, recurse into them
    if "sublink" in df.columns:
        for sub_url in df['sublink']:
            # Construct the full sub-URL
            full_sub_url = base_url + sub_url
            print(full_sub_url)
            
            # Scrape the sub-URL
            sub_df = web_scraper(full_sub_url, output_file)
            
            # Recursively scrape any further sub-URLs
            if sub_df is not None and not isinstance(sub_df, dict) and "sublink" in sub_df.columns:
                scrape_url(full_sub_url, sub_df, output_file)
