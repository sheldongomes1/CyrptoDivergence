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
set_page_config(page_title="Narrative Divergence Detector", layout="wide")
title("Narrative Divergence Detector (MVP)")
markdown("Track crypto narratives vs price movements — identify divergence and AI-generated insights.")

# ========== INPUTS ==========
sidebar.header("Configuration")
tokens = st.sidebar.multiselect("Select Tokens to Analyze", DEFAULT_TOKENS, default=DEFAULT_TOKENS)
days_back = st.sidebar.slider("Days of History", 7, 30, 14)
