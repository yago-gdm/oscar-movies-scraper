# Oscar Movies Scraper

This repository contains a Python script for scraping movie data related to the Oscars, processing the budget information, and exporting the cleaned data to a CSV file.

## Features
- Scrapes movie data from the Oscars API
- Cleans and normalizes the budget data
- Exports the data to a CSV file with columns such as:
  - Film title
  - Year of the film
  - Wikipedia URL
  - Oscar winner status
  - Budget (with conversions applied)

## Requirements

Before running the script, ensure you have the following:

- Python 3.8 or higher
- Required Python libraries (see installation below)

## Installation (Windows)

1. Clone the repository (skip if you already has the project in zip format extrated):

   ```bash
   git clone https://github.com/yago-gdm/oscar-movies-scraper.git
   ```

2. Go to the repository folder:

   ```bash
   cd oscar-movies-scraper
   ```

3. Create a virtual environment (optional but recommended):
    ```bash
   python -m venv venv
    ```

4. Create a virtual environment (optional but recommended):
    ```bash
    .\venv\Scripts\activate
    ```

5. Install the required dependencies:
    ```bash
   pip install -r requirements.txt
    ```

## Usage

To run the script and scrape Oscar movies data, simply execute the following command:

1. Run the script
    ```bash
   python .\src\main.py
    ```
2. Output: The cleaned data will be exported to cleaned_oscar_movies.csv.

# Function Documentation

## `scrape_movies(url: str) -> pd.DataFrame`
Fetches movie data from a given URL and returns a DataFrame containing Oscar-nominated films and their details.

### Parameters:
- **url** (`str`): The URL where movie data is fetched from.

### Returns:
- **pandas.DataFrame**: A DataFrame containing information about films, including:
  - `film`: Name of the film.
  - `year`: The year of the film.
  - `wiki_url`: URL to the film's Wikipedia page.
  - `oscar_winner`: Whether the film won an Oscar (`True`/`False`).
  - `detail_url`: URL with more detailed information about the film.
  - `producers`: List of producers for the film.
  - `production_company`: The production company for the film.
  - `original_budget`: The original budget (scraped from the detailed film URL).

## `scrape_budget(detail_url: str) -> str`
Fetches the budget information for a given film from a detailed page.

### Parameters:
- **detail_url** (`str`): URL to the page with the film's detailed information (including budget).

### Returns:
- **str**: The original budget of the film. If an error occurs during the request, returns `"0"`.

## `scrape_budgets_concurrently(detail_urls: list[str]) -> list[str]`
Fetches the budget information concurrently for a list of films from their respective detail pages using multithreading. It leverages Python's ThreadPoolExecutor to perform concurrent requests, improving the efficiency of the process when multiple URLs are provided.

### Parameters:
- **detail_urls** (`list[str]`): A list of URLs, each pointing to a page with detailed information about a specific film, including its budget.

### Returns:
- **list[str]**: A list where each element corresponds to the budget of the film from the respective URL. If an error occurs during the scraping process for a specific URL, the corresponding budget in the returned list will be "0".

## `clean_year(year: str) -> str`
Cleans a given year string to extract the 4-digit year.

### Parameters:
- **year** (`str`): A string potentially containing a year.

### Returns:
- **str**: A string representing the 4-digit year extracted from the input.

## `add_converted_budget(df: pd.DataFrame) -> pd.DataFrame`
Cleans and converts the budget column in the DataFrame to a numeric format, handling various currency symbols and notations.

### Parameters:
- **df** (`pandas.DataFrame`): DataFrame containing a column `original_budget` with raw budget information.

### Returns:
- **pandas.DataFrame**: The original DataFrame with an additional column `converted_budget`, containing cleaned and converted budget data.

### Assumptions:
1. Both amounts in $ and amounts in other currencies can be considered.
2. Re-release values ​​are irrelevant.
3. Amounts below 700 USD represent millions.
4. The conversion rates are: £1 ≈ $1.30, €1 ≈ $1.10, ₤1 ≈ $1.10.
5. The first year mentioned corresponds to the year of the film.

## `main()`
The main function that orchestrates the scraping, cleaning, and exporting of Oscar-nominated movie data.

### Workflow:
1. Calls `scrape_movies(url)` to fetch movie data from a predefined URL.
2. Cleans and converts the budget data using `add_converted_budget(df)`.
3. Ensures the `year` column is in integer format.
4. Exports the cleaned data to a CSV file named `cleaned_oscar_movies.csv`.

### Exports:
- A CSV file named `'cleaned_oscar_movies.csv'` is created if the DataFrame is not empty.

### Notes:
- If no data is available or the DataFrame is empty, a message indicating no data was exported is printed.
