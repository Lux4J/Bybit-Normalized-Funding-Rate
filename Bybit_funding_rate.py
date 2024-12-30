#!/usr/bin/env python
# coding: utf-8

# In[116]:


import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
import numpy as np
from sklearn.preprocessing import QuantileTransformer

def fetch_btc_price():
    url = "https://api.bybit.com/v5/market/kline"
    start_time = int(datetime(2023, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)  # Start of 2023 in milliseconds
    end_time = int(datetime.now(timezone.utc).timestamp() * 1000)  # Current time in milliseconds
    limit = 1000  # Maximum number of data points per request
    interval = 'D'  # Daily interval

    all_data = []

    params = {
        "category": "linear",
        "symbol": "BTCUSDT",
        "interval": interval,
        "start": start_time,
        "end": end_time,
        "limit": limit
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        result = response.json().get("result", {})
        data = result.get("list", [])
        if not data:
            print("No more data returned by API.")

        all_data.extend(data)
        # Log progress
        print(f"Retrieved {len(data)} entries. Next start time: {datetime.fromtimestamp(start_time / 1000, tz=timezone.utc)}")

    else:
        print(f"Error fetching data: {response.status_code} {response.text}")

    if all_data:
        # Convert data to DataFrame
        price_df = pd.DataFrame(
            [{
                "time": int(item[0]),
                "close": float(item[4])
            } for item in all_data]
        )

        price_df['time'] = pd.to_datetime(price_df['time'], unit='ms')
        return price_df
    else:
        print("No data fetched.")
        return pd.DataFrame()

def fetch_funding_rate(symbol: str):
    url = "https://api.bybit.com/v5/market/funding/history"
    end_time = int(datetime.now(timezone.utc).timestamp() * 1000)  # Current time in ms
    start_time = int(datetime(2023, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)  # Start of 2023 in ms

    funding_data = []

    while start_time < end_time:
        params = {
            "category": "linear",
            "symbol": symbol,
            "startTime": start_time,
            "endTime": end_time,
            "limit": 200
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get("result", {}).get("list", [])
            if not data:  # Break if no data is returned
                print("No more data available from the API.")
                break
            funding_data.extend(data)

            # Update start_time to the last retrieved timestamp + 1 ms to avoid overlap
            last_timestamp = int(data[-1]["fundingRateTimestamp"])
            if last_timestamp <= start_time:  # Ensure progress is being made
                print("No progress in data timestamps. Breaking loop.")
                break
            end_time = last_timestamp
        else:
            print(f"Error fetching data: {response.status_code} {response.text}")
            break

    # Filter only daily 0:00 UTC timestamps
    filtered_data = []
    for entry in funding_data:
        timestamp = int(entry["fundingRateTimestamp"]) / 1000
        dt = datetime.fromtimestamp(timestamp, timezone.utc)  # Corrected for timezone-aware datetime
        if dt.hour == 0:  # Keep only entries with 0:00 UTC timestamp
            filtered_data.append(entry)
            
    return filtered_data

def quantile_normalization(data):
    n_samples = len(data)
    n_quantiles = min(1000, n_samples)  # Use the number of samples or 1000, whichever is smaller
    quantile_transformer = QuantileTransformer(n_quantiles=n_quantiles, output_distribution='normal', random_state=42)
    normalized_rates = quantile_transformer.fit_transform(data.reshape(-1, 1)).flatten()
    return normalized_rates

def plot_combined(btc_price_df, funding_data):
    if btc_price_df.empty:
        print("No BTC price data to plot.")
        return

    if not funding_data:
        print("No funding data to plot.")
        return

    # Convert funding data to a pandas DataFrame
    funding_df = pd.DataFrame(funding_data)
    funding_df["timestamp"] = pd.to_datetime(funding_df["fundingRateTimestamp"].astype(int) / 1000, unit="s")
    funding_df["fundingRate"] = funding_df["fundingRate"].astype(float)
    funding_df = funding_df.sort_values("timestamp")

    # Perform quantile normalization on funding rates
    funding_df["normalizedFundingRate"] = quantile_normalization(funding_df["fundingRate"].values)

    # Calculate thresholds for top and bottom 2.5%
    upper_threshold = funding_df["normalizedFundingRate"].quantile(0.975)
    lower_threshold = funding_df["normalizedFundingRate"].quantile(0.025)

    # Identify timestamps for top and bottom thresholds
    upper_exceed = funding_df[funding_df["normalizedFundingRate"] > upper_threshold]["timestamp"]
    lower_exceed = funding_df[funding_df["normalizedFundingRate"] < lower_threshold]["timestamp"]

    # Plot the data
    fig, ax2 = plt.subplots(figsize=(12, 6))

    # Plot BTC price on the second y-axis
    ax2.plot(btc_price_df['time'], btc_price_df['close'], label='BTC Close Price', color='orange', zorder=3)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('BTC Price (USD)', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    # Create first y-axis for funding rate
    ax1 = ax2.twinx()
    ax1.plot(funding_df['timestamp'], funding_df['normalizedFundingRate'], label='Normalized Funding Rate', color='blue', zorder=2)

    # Highlight vertical lines for top and bottom 2.5%
    for timestamp in upper_exceed:
        ax1.axvline(pd.Timestamp(timestamp, tz=timezone.utc), color='red', linestyle='-', alpha=0.7, zorder=1)
    for timestamp in lower_exceed:
        ax1.axvline(pd.Timestamp(timestamp, tz=timezone.utc), color='green', linestyle='-', alpha=0.7, zorder=1)

    # Add a single entry for the vertical line labels
    ax1.plot([], [], color='red', linestyle='-', label='Overbought (Z > 1.96)')
    ax1.plot([], [], color='green', linestyle='-', label='Oversold (Z < -1.96)')

    ax1.set_ylabel('Normalized Funding Rate', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Add grid, title, and legend
    fig.suptitle('Bybit BTC Normalized Funding Rate')
    ax2.grid(True)

    # Combine legends into one box
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    plt.show()

# Fetch data
btc_price = fetch_btc_price()
funding_data = fetch_funding_rate("BTCUSD")

# Plot combined chart
plot_combined(btc_price, funding_data)



# In[ ]:





# In[ ]:




