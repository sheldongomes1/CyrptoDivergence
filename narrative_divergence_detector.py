# narrative_divergence_detector.py
# Streamlit app skeleton with crypto narrative + price divergence logic

import streamlit as st
import pandas as pd
import requests
import datetime
import matplotlib.pyplot as plt
from github import Github

# ========== CONFIGURATION ==========
COINGECKO_API = "https://api.coingecko.com/api/v3"
DEFAULT_TOKENS = ["bitcoin", "ethereum", "solana"]
GITHUB_REPOS = {
    "bitcoin": "bitcoin/bitcoin",
    "ethereum": "ethereum/go-ethereum",
    "solana": "solana-labs/solana"
}

# ========== APP TITLE ==========
st.set_page_config(page_title="Narrative Divergence Detector", layout="wide")
st.title("Narrative Divergence Detector (MVP)")
st.markdown("Track crypto narratives vs price movements — identify divergence and AI-generated insights.")

# ========== INPUTS ==========
st.sidebar.header("Configuration")
tokens = st.sidebar.multiselect("Select Tokens to Analyze", DEFAULT_TOKENS, default=DEFAULT_TOKENS)
days_back = st.sidebar.slider("Days of History", 7, 30, 14)

# ========== DATA FETCHING ==========
@st.cache_data(show_spinner=False)
def fetch_price_data(token_id, days):
    url = f"{COINGECKO_API}/coins/{token_id}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return None
    prices = r.json()['prices']
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df.set_index("date")["price"]
    return df

@st.cache_data(show_spinner=False)
def fetch_github_commits(repo_name, days):
    g = Github()  # Use anonymous access for MVP
    repo = g.get_repo(repo_name)
    since = datetime.datetime.now() - datetime.timedelta(days=days)
    commits = repo.get_commits(since=since)
    return commits.totalCount

# ========== MAIN DISPLAY ==========
for token in tokens:
    st.subheader(f"{token.title()}")
    price_data = fetch_price_data(token, days_back)
    if price_data is None:
        st.warning(f"Failed to fetch price data for {token}.")
        continue
    price_change = ((price_data[-1] - price_data[0]) / price_data[0]) * 100

    # GitHub activity
    repo_name = GITHUB_REPOS.get(token)
    commits = fetch_github_commits(repo_name, days_back) if repo_name else "N/A"

    # Plot price
    fig, ax = plt.subplots()
    price_data.plot(ax=ax)
    ax.set_title(f"{token.title()} - {days_back}D Price Trend")
    st.pyplot(fig)

    # Show summary
    st.markdown(f"**Price Change:** {price_change:.2f}% over {days_back} days")
    st.markdown(f"**GitHub Commits:** {commits}")

    # Placeholder for AI-generated insight (to be added in next step)
    st.info("AI Insight will appear here once integrated.")
