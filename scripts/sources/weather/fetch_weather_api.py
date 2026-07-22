"""
Fetch Historical Weather Data for Brazil.

Responsibilities
----------------
1. Read Olist order dates.
2. Determine historical date range.
3. Download historical weather from Open-Meteo.
4. Save data as NDJSON for BigQuery.
"""

import json

import pandas as pd
import requests

from scripts.utilities.config import (
    ORDERS_FILE,
    WEATHER_RAW_DIR,
)

# ==========================================================
# Configuration
# ==========================================================

OUTPUT_FILE = WEATHER_RAW_DIR / "weather_historical.json"

WEATHER_RAW_DIR.mkdir(parents=True, exist_ok=True)

BRAZIL_CITIES = [
    {"city": "Sao Paulo", "lat": -23.5505, "lon": -46.6333},
    {"city": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
    {"city": "Brasilia", "lat": -15.7939, "lon": -47.8828},
    {"city": "Salvador", "lat": -12.9777, "lon": -38.5016},
    {"city": "Fortaleza", "lat": -3.7319, "lon": -38.5267},
    {"city": "Belo Horizonte", "lat": -19.9167, "lon": -43.9345},
    {"city": "Curitiba", "lat": -25.4284, "lon": -49.2733},
    {"city": "Manaus", "lat": -3.1190, "lon": -60.0217},
    {"city": "Recife", "lat": -8.0476, "lon": -34.8770},
    {"city": "Porto Alegre", "lat": -30.0346, "lon": -51.2177},
]

# ==========================================================
# Read Olist Date Range
# ==========================================================


def get_order_date_range():

    orders = pd.read_csv(
        ORDERS_FILE,
        usecols=["order_purchase_timestamp"],
        parse_dates=["order_purchase_timestamp"],
    )

    start_date = orders["order_purchase_timestamp"].min().date().isoformat()

    end_date = orders["order_purchase_timestamp"].max().date().isoformat()

    return start_date, end_date


# ==========================================================
# Download Historical Weather
# ==========================================================


def fetch_city_weather(city, start_date, end_date):

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={city['lat']}"
        f"&longitude={city['lon']}"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
        "&daily="
        "temperature_2m_max,"
        "temperature_2m_min,"
        "precipitation_sum,"
        "rain_sum,"
        "weather_code"
        "&timezone=America/Sao_Paulo"
    )

    response = requests.get(url, timeout=120)

    response.raise_for_status()

    daily = response.json()["daily"]

    records = []

    for i in range(len(daily["time"])):

        records.append(
            {
                "city": city["city"],
                "country": "Brazil",
                "date": daily["time"][i],
                "temperature_max": daily["temperature_2m_max"][i],
                "temperature_min": daily["temperature_2m_min"][i],
                "precipitation_sum": daily["precipitation_sum"][i],
                "rain_sum": daily["rain_sum"][i],
                "weather_code": daily["weather_code"][i],
            }
        )

    return records


# ==========================================================
# Save NDJSON
# ==========================================================


def save_weather(records):

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as f:

        for record in records:

            f.write(json.dumps(record))

            f.write("\n")


# ==========================================================
# Main
# ==========================================================


def main():

    print("=" * 70)
    print("Historical Weather Downloader")
    print("=" * 70)

    start_date, end_date = get_order_date_range()

    print(f"Start Date : {start_date}")
    print(f"End Date   : {end_date}")
    print()

    all_weather = []

    for city in BRAZIL_CITIES:

        print(f"Fetching {city['city']}...")

        weather = fetch_city_weather(
            city,
            start_date,
            end_date,
        )

        print(f"  {len(weather)} daily records")

        all_weather.extend(weather)

    save_weather(all_weather)

    print()
    print("=" * 70)
    print("Completed")
    print("=" * 70)
    print(f"Cities          : {len(BRAZIL_CITIES)}")
    print(f"Weather Records : {len(all_weather)}")
    print(f"Output          : {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
