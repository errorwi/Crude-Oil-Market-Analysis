import pandas as pd
import yfinance as yf


START_DATE = "2015-01-01"


def load_market_prices(start_date=START_DATE):
    """
    Download daily WTI and Brent crude oil prices.

    WTI  -> CL=F
    Brent -> BZ=F
    """

    # Download WTI
    wti = yf.download(
        "CL=F",
        start=start_date,
        auto_adjust=False,
        progress=False
    )

    # Download Brent
    brent = yf.download(
        "BZ=F",
        start=start_date,
        auto_adjust=False,
        progress=False
    )

    # Extract closing prices
    wti = wti[["Close"]].copy()
    brent = brent[["Close"]].copy()

    # Rename columns
    wti.columns = ["wti_price"]
    brent.columns = ["brent_price"]

    # Combine
    prices = wti.join(brent, how="outer")

    # Convert index into date column
    prices.index.name = "date"
    prices = prices.reset_index()

    return prices


if __name__ == "__main__":
    prices = load_market_prices()

    print("\nFirst 5 rows:")
    print(prices.head())

    print("\nData information:")
    prices.info()

    print("\nMissing values:")
    print(prices.isna().sum())

    # Save raw data
    output_path = "data/raw/market_prices.csv"
    prices.to_csv(output_path, index=False)

    print(f"\nSaved data to: {output_path}")