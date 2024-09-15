import re
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests


def scrape_movies(url):

    response = requests.get(url)
    data = response.json()
    films_data = []
    for year_data in data["results"]:
        for film in year_data["films"]:
            film_details = {
                "film": film["Film"],
                "year": clean_year(year_data["year"]),
                "wiki_url": film["Wiki URL"],
                "oscar_winner": film["Winner"],
                "detail_url": film["Detail URL"],
                "producers": film["Producer(s)"],
                "production_company": film["Production Company(s)"],
                # "original_budget": scrape_budget(film["Detail URL"]),
            }
            films_data.append(film_details)
    detail_urls = [film["detail_url"] for film in films_data]
    budgets = scrape_budgets_concurrently(detail_urls)

    for i, film in enumerate(films_data):
        film["original_budget"] = budgets[i]

    return pd.DataFrame(films_data)


def scrape_budget(detail_url):

    response = requests.get(detail_url)
    if response.status_code != 200:
        print(
            f"Error accessing details URL {detail_url}. Status code: {response.status_code}"
        )
        return "0"
    data = response.json()
    original_budget = data.get("Budget", "")
    return original_budget


def scrape_budgets_concurrently(detail_urls):
    budgets = ["0"] * len(detail_urls)
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_url = {
            executor.submit(scrape_budget, url): idx
            for idx, url in enumerate(detail_urls)
        }
        for future in as_completed(future_to_url):
            idx = future_to_url[future]
            try:
                budgets[idx] = future.result()
            except Exception as e:
                print(f"Error in future for index {idx}: {e}")
    return budgets


def clean_year(year):
    return re.search(r"\b\d{4}\b", year).group()


def add_converted_budget(df):

    df["converted_budget"] = df["original_budget"].str.replace(
        r"\[.*?\]", "", regex=True
    )
    df["converted_budget"] = df["converted_budget"].str.replace(
        r"\(.*?\)", "", regex=True
    )
    df["converted_budget"] = df["converted_budget"].str.split("-").str[0]
    df["converted_budget"] = df["converted_budget"].str.split("–").str[0]
    df["converted_budget"] = df["converted_budget"].str.replace("est.", "")
    df["converted_budget"] = df["converted_budget"].str.replace("million", "")
    df["converted_budget"] = df["converted_budget"].str.strip()

    df["converted_budget"] = (
        df["converted_budget"]
        .str.extract(r"(.*)or £", expand=False)
        .fillna(df["converted_budget"])
    )
    df["converted_budget"] = df["converted_budget"].str.replace(",", "")
    df["converted_budget"] = df["converted_budget"].str.replace(r":.*", "", regex=True)
    df["converted_budget"] = df["converted_budget"].apply(
        lambda x: (
            "${}".format(min(map(float, re.findall(r"\d+\.?\d*", x))))
            if x and "or" in x
            else x
        )
    )
    df["converted_budget"] = df["converted_budget"].apply(
        lambda x: (
            "${}".format(max(map(float, re.findall(r"\d+\.?\d*", x))))
            if x and "$" in x
            else x
        )
    )

    df["converted_budget"] = (
        df["converted_budget"]
        .str.replace("US$", "")
        .str.replace("USD", "")
        .str.replace("$", "")
    )

    df["converted_budget"] = df["converted_budget"].apply(
        lambda x: str(float(x[1:]) * 1.3) if isinstance(x, str) and "£" in x else x
    )
    df["converted_budget"] = df["converted_budget"].apply(
        lambda x: str(float(x[1:]) * 1.1) if isinstance(x, str) and "€" in x else x
    )
    df["converted_budget"] = df["converted_budget"].apply(
        lambda x: str(float(x[1:]) * 1.1) if isinstance(x, str) and "₤" in x else x
    )

    df["converted_budget"] = pd.to_numeric(
        df["converted_budget"], errors="raise"
    ).fillna(0)
    df["converted_budget"] = (
        df["converted_budget"].apply(lambda x: x * 1_000_000 if x < 700 else x).round()
    )
    df["converted_budget"] = df["converted_budget"].astype(int)

    return df


def main():
    url = "http://oscars.yipitdata.com/"
    df = scrape_movies(url)
    df = add_converted_budget(df)
    df["year"] = df["year"].astype(int)

    if not df.empty:
        df.to_csv("cleaned_oscar_movies.csv", index=False)
        print("Data exported to 'cleaned_oscar_movies.csv'.")
    else:
        print("No data was exported.")


if __name__ == "__main__":
    main()
