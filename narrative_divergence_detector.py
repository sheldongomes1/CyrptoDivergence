import streamlit as st

print("hello world")

# ========== CONFIGURATION ==========
COINGECKO_API = "https://api.coingecko.com/api/v3"
DEFAULT_TOKENS = ["bitcoin", "ethereum", "solana"]
GITHUB_REPOS = {
    "bitcoin": "bitcoin/bitcoin",
    "ethereum": "ethereum/go-ethereum",
    "solana": "solana-labs/solana"
}
REDDIT_SUBS = ["cryptocurrency", "ethfinance", "solana"]
PUSHSHIFT_URL = "https://api.pushshift.io/reddit/search/submission/"


# ========== APP TITLE ==========
st.set_page_config(page_title="Crypto Narrative Divergence Detector", layout="wide")
st.title("Crypto Narrative Divergence Detector (MVP)")
st.markdown("Track crypto narratives vs price movements — identify divergence and AI-generated insights.")

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

for token in tokens:
    st.subheader(f"{token.title()}")
    price_data = fetch_price_data(token, days_back)
    if price_data is None:
        st.warning(f"Failed to fetch price data for {token}.")
        continue
    price_change = ((price_data[-1] - price_data[0]) / price_data[0]) * 100
