# Streamlit main code
import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime, timedelta

try:
    syve_api_key = st.secrets["syve_api_key"]
except KeyError:
    st.error("syve_api_key not found. Please ensure it's set in Streamlit secrets.")
    st.stop()

"""
# Find Fresh Wallets Fast & Spot Insider Trading

Enter an Ethereum token address below to find fresh wallet trades. Max number of days = 30.

If you have any questions or notice any errors text me on [Twitter](https://twitter.com/JxTolan).

### Powered by the [Syve.ai](https://www.syve.ai/) API. 
"""

def request_fresh_wallet_trades(token_address, days, syve_api_key):

    url = f'https://api.syve.ai/v1/fresh-wallet-trades?token_address={token_address}&days={days}&key={syve_api_key}'

    response = requests.get(url)
    try:
        df = pd.DataFrame(response.json())
        return df
    except: 
        st.write(response)
        st.write(response.text)

token_address = st.text_input("Token Address", "0xd533a949740bb3306d119cc777fa900ba034cd52")

days = st.text_input("Fresh Wallet Age in Days", '7')

try:
    days = int(days)
except ValueError:
    st.warning("Please enter a valid integer for days.")
    days = None
  
fresh_wallets_df = request_fresh_wallet_trades(token_address, days, syve_api_key)
st.write(f"Fresh Wallet Trades Over {days} Days")
st.write(fresh_wallets_df)

if days:

    # Assuming there's a 'timestamp' column in your dataframe
    fresh_wallets_df['date'] = pd.to_datetime(fresh_wallets_df['timestamp']).dt.date

    # Group by date and sum the trades
    daily_trade_volume = fresh_wallets_df.groupby('date').sum('amount_usd')  # Replace with the appropriate column to sum if different

    # Plotting
    st.bar_chart(daily_trade_volume)
