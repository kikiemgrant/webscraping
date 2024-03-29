# Premier League Player Data Scraper

This Python script is designed to scrape detailed player information from the Premier League website.

## Table of Contents

- [Features](#features)
- [Libraries Used](#libraries-used)
- [How It Works](#how-it-works)
- [Error Handling](#error-handling)
- [Output](#output)
- [Usage](#usage)

## Features

- Fetches URLs of all Premier League clubs.
- Extracts URLs of all players associated with each club.
- Scrapes detailed player profiles including name, position, club, nationality, age, height, and weight.
- Performs data cleaning to ensure the quality of the extracted data.
- Stores the cleaned data in a CSV file.

## Libraries Used

- `requests`: For making HTTP requests.
- `BeautifulSoup`: For parsing HTML content.
- `time`: For adding delays between requests.
- `pandas`: For data manipulation and storage.

## How It Works

1. **Fetching Club URLs**: Sends a request to the main clubs page on the Premier League website and parses the returned HTML to extract individual club URLs.
2. **Extracting Player URLs**: For each club, navigates to its squad page and extracts the URLs of all associated players.
3. **Scraping Player Details**: For each player URL, the script extracts:
   - **Name**: Player's full name.
   - **Position**: Player's playing position.
   - **Club**: Associated club.
   - **Nationality**: Player's nationality.
   - **Age**: Player's age.
   - **Height**: Player's height in centimeters.
   - **Weight**: Player's weight in kilograms.
4. **Data Cleaning**: Performs several data cleaning operations to ensure the quality of the extracted data.

## Error Handling

The script is equipped with error handling mechanisms. If it encounters an issue while fetching data (possibly due to too many requests), it will wait for 5 seconds before retrying.

## Output

The cleaned data is stored in a CSV file named `playerOverviews.csv`.

## Usage

1. Ensure you have all the required libraries installed.
2. Run the script using Python.
3. Once the script completes its execution, check the output CSV file for the scraped data.
