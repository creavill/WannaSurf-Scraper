# Surf Spot Web Scraper

## Overview
This project is a web scraper designed to extract information about surf spots from wannasurf.com. It navigates through country pages, identifies surf spot listings, and extracts detailed information about each location including wave characteristics, geographic coordinates, and other relevant data for surfers.

## Features
- Recursive scraping of country and regional surf spot data
- Extraction of detailed information for individual surf spots
- Processing of both tabular data and unstructured webpage content
- Data storage in text files organized by country

## Project Structure
- `main.py`: Entry point for the application
- `scraper.py`: Core web scraping functionality
- `data_processor.py`: Functions for processing and cleaning extracted data
- `utils.py`: Helper functions and utilities

## Usage
```python
# Run the main scraping process
python main.py

# To scrape a specific country
python main.py --country "Europe/France"
```

## Requirements
- Python 3.6+
- BeautifulSoup4
- Requests
- Pandas

## Installation
```bash
pip install -r requirements.txt
```

## Disclaimer
This code is provided for educational purposes only. Web scraping may be against the terms of service of some websites. Always check the robots.txt file and terms of service before scraping any website. The author is not responsible for any misuse of this code.

## License
MIT
