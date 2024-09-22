
# Project Title: News Data Aggregator and Analysis Tool

## Overview

This project aggregates news data from various Ukrainian news websites, parses and analyzes it to identify key trends and visualize the results. The script scrapes news articles from **RBC**, **Pravda**, **Unian**, and **24tv**, and performs data analysis on the collected information. Visualizations, including bar charts and word clouds, are generated to display trends in article frequency and common words used in the headlines.

## Features

- **Web Scraping**: Utilizes `requests` and `BeautifulSoup` to extract news headlines and timestamps from four major Ukrainian news sites.
- **Data Aggregation**: Merges news from different sources into a unified format for comprehensive analysis.
- **Time-Based Analysis**: Calculates the number of news articles published during different hours over two consecutive days.
- **Word Cloud Generation**: Extracts frequent words from the articles to generate word clouds that represent popular terms.
- **Visualization**: Uses `matplotlib` to generate bar charts showing the distribution of news articles over time, and 3D bar charts to compare the frequency of articles across different news sources.

## Technologies Used

- **Python**: The main programming language for implementing the scraper and the analysis tool.
- **BeautifulSoup**: For parsing HTML and extracting the news content from web pages.
- **Requests**: To make HTTP requests to the news websites.
- **Matplotlib**: For creating bar charts and other visual representations.
- **WordCloud**: To generate word clouds of frequently mentioned words in the news articles.

## How to Use

1. **Install Required Libraries**:
   - `requests`
   - `beautifulsoup4`
   - `matplotlib`
   - `wordcloud`
   
   You can install them using:
   ```
   pip install requests beautifulsoup4 matplotlib wordcloud
   ```

2. **Run the Script**:
   Simply run the `main.py` file to start fetching the news and performing the analysis:
   ```bash
   python main.py
   ```

3. **View Results**:
   - The script outputs a `.txt` file containing the aggregated news headlines.
   - Visualizations, such as bar charts and word clouds, are displayed to show insights from the collected data.
