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
st.set_page_config(page_title="Narrative Divergence Detector", layout="wide")
st.title("Narrative Divergence Detector (MVP)")
st.markdown("Track crypto narratives vs price movements — identify divergence and AI-generated insights.")
