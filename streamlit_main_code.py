# Streamlit main code
import streamlit as st
import pandas as pd
import math
from collections import namedtuple
import altair as alt
import requests
import time
from datetime import datetime, timedelta

"""
# Find Fresh Wallets Fast

Enter a token below to find fresh wallet trades. Run time generally <7s.

If you have any questions or notice any errors text me on [Twitter](https://twitter.com/JamesT0lan).

### Powered by the [Syve.ai](https://www.syve.ai/) API. 
"""

def request_fresh_wallet_trades(token_address, days, API_KEY):

    url = f'https://api.syve.ai/v1/fresh-wallet-trades?token_address={token_address}&days={days}&key={API_KEY}'

    response = requests.get(url)

    return pd.DataFrame(response.json())

token_address = st.text_input("Token Address", "0xd084944d3c05cd115c09d072b9f44ba3e0e45921")

days = st.text_input("Fresh Wallet Age in Days", '7')

try:
    days = int(days)
except ValueError:
    st.warning("Please enter a valid integer for days.")
    days = None
  
fresh_wallets_df = request_fresh_wallet_trades(token_address, days, API_KEY)
st.write(f"Fresh Wallet Trades Over {days} Days")
st.write(fresh_wallets_df)
