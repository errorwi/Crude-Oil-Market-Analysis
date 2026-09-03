import os
import requests
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv


load_dotenv()

START_DATE = "2015-01-01"


def load_market_prices(start_date=START_DATE):
    """
    Download WTI and Brent futures prices from Yahoo Finance.
    """

    tickers = {
        "CL=F": "wti_price",
        "BZ=F": "brent_price"
    }

    data = yf.download(
        list(tickers.keys()),
        start=start_date,
        auto_adjust=False,
        progress=False
    )

    prices = data["Close"].copy()

    prices = prices.rename(columns=tickers)

    prices.index.name = "date"

    prices = prices.reset_index()

    return prices


def load_eia_series(
    route,
    series_name,
    start_date=START_DATE,
    end_date=None
):
    """
    Retrieve an EIA API dataset.

    Parameters
    ----------
    route : str
        EIA API route.
    series_name : str
        Column containing the desired series.
    """

    api_key = os.getenv("EIA_API_KEY")

    if not api_key:
        raise ValueError(
            "EIA_API_KEY not found. "
            "Add your API key to a .env file."
        )

    url = f"https://api.eia.gov/v2/petroleum/crd/data/"

    params = {
        "api_key": api_key,
        "frequency": "monthly",
        "data[0]": "value",
        "start": start_date[:7]
    }

    if end_date:
        params["end"] = end_date[:7]

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    if "response" not in result:
        raise ValueError("Unexpected EIA API response.")

    data = result["response"]["data"]

    df = pd.DataFrame(data)

    return df