# narrative_divergence_detector.py
# Streamlit app with crypto narrative + price divergence logic

import streamlit as st
import pandas as pd
import requests
import datetime
import matplotlib.pyplot as plt
import time

# ========== CONFIGURATION ==========
COINGECKO_API = "https://api.coingecko.com/api/v3"
DEFAULT_TOKENS = ["bitcoin", "ethereum", "solana"]

# Note: GitHub API and Reddit API functionality removed due to rate limiting issues
# You can add them back with proper API keys and error handling

# ========== APP TITLE ==========
st.set_page_config(page_title="Narrative Divergence Detector", layout="wide")
st.title("🧠 Narrative Divergence Detector (MVP)")
st.markdown("Track crypto narratives vs price movements — identify divergence and AI-generated insights.")

# ========== INPUTS ==========
st.sidebar.header("Configuration")
tokens = st.sidebar.multiselect("Select Tokens to Analyze", DEFAULT_TOKENS, default=DEFAULT_TOKENS)
days_back = st.sidebar.slider("Days of History", 7, 30, 14)

# ========== DATA FETCHING ==========
@st.cache_data(show_spinner=True, ttl=300)  # Cache for 5 minutes
def fetch_price_data(token_id, days):
    """Fetch price data from CoinGecko API with error handling"""
    try:
        url = f"{COINGECKO_API}/coins/{token_id}/market_chart"
        params = {"vs_currency": "usd", "days": days, "interval": "daily"}
        
        # Add headers to avoid rate limiting
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        r = requests.get(url, params=params, headers=headers, timeout=10)
        
        if r.status_code == 429:  # Rate limited
            st.warning(f"Rate limited for {token_id}. Waiting...")
            time.sleep(2)
            return None
            
        if r.status_code != 200:
            st.error(f"API Error {r.status_code} for {token_id}")
            return None
            
        data = r.json()
        
        if 'prices' not in data:
            st.error(f"No price data found for {token_id}")
            return None
            
        prices = data['prices']
        if not prices:
            st.error(f"Empty price data for {token_id}")
            return None
            
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
        df = df.set_index("date")["price"]
        return df
        
    except requests.exceptions.RequestException as e:
        st.error(f"Network error fetching data for {token_id}: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error processing data for {token_id}: {str(e)}")
        return None

def calculate_price_metrics(price_data):
    """Calculate additional price metrics"""
    if len(price_data) < 2:
        return {}
    
    metrics = {}
    metrics['price_change'] = ((price_data.iloc[-1] - price_data.iloc[0]) / price_data.iloc[0]) * 100
    metrics['volatility'] = price_data.pct_change().std() * 100
    metrics['max_price'] = price_data.max()
    metrics['min_price'] = price_data.min()
    metrics['current_price'] = price_data.iloc[-1]
    
    return metrics

# ========== MAIN DISPLAY ==========
if not tokens:
    st.warning("Please select at least one token to analyze.")
else:
    for token in tokens:
        st.subheader(f"📈 {token.title()}")
        
        # Create columns for better layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Fetch and display price data
            with st.spinner(f"Fetching price data for {token}..."):
                price_data = fetch_price_data(token, days_back)
            
            if price_data is None:
                st.error(f"Failed to fetch price data for {token}.")
                continue
            
            if len(price_data) == 0:
                st.error(f"No price data available for {token}.")
                continue
            
            # Plot price with better styling
            fig, ax = plt.subplots(figsize=(10, 6))
            price_data.plot(ax=ax, color='#1f77b4', linewidth=2)
            ax.set_title(f"{token.title()} - {days_back} Day Price Trend", fontsize=14, fontweight='bold')
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (USD)")
            ax.grid(True, alpha=0.3)
            
            # Format y-axis for better readability
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.2f}'))
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()  # Close figure to prevent memory leaks
        
        with col2:
            # Calculate and display metrics
            metrics = calculate_price_metrics(price_data)
            
            if metrics:
                st.metric(
                    label="Current Price",
                    value=f"${metrics['current_price']:,.2f}"
                )
                
                st.metric(
                    label="Price Change",
                    value=f"{metrics['price_change']:+.2f}%",
                    delta=f"{metrics['price_change']:.2f}%"
                )
                
                st.metric(
                    label="Volatility",
                    value=f"{metrics['volatility']:.2f}%"
                )
                
                st.metric(
                    label="Max Price",
                    value=f"${metrics['max_price']:,.2f}"
                )
                
                st.metric(
                    label="Min Price",
                    value=f"${metrics['min_price']:,.2f}"
                )
        
        # Placeholder sections for future features
        st.markdown("---")
        
        # GitHub Activity Section (Placeholder)
        with st.expander("📊 Development Activity (Coming Soon)"):
            st.info("GitHub commit tracking will be added here with proper API authentication.")
        
        # Social Media Mentions Section (Placeholder)
        with st.expander("🗣️ Social Media Sentiment (Coming Soon)"):
            st.info("Reddit and Twitter mention tracking will be added here.")
        
        # AI Insights Section (Placeholder)
        with st.expander("🧠 AI-Generated Insights (Coming Soon)"):
            if metrics:
                # Simple rule-based insights as placeholder
                if metrics['price_change'] > 10:
                    st.success("📈 Strong upward momentum detected!")
                elif metrics['price_change'] < -10:
                    st.error("📉 Significant downward movement detected!")
                else:
                    st.info("📊 Price movement within normal range.")
                
                if metrics['volatility'] > 5:
                    st.warning("⚠️ High volatility detected - exercise caution!")
            
            st.info("Advanced AI analysis will be integrated here in future updates.")
        
        st.markdown("---")

# ========== FOOTER ==========
st.markdown("---")
st.markdown("**Note:** This is an MVP version. GitHub API and Reddit API features are disabled to avoid rate limiting issues. Add your own API keys for full functionality.")

# Add some helpful information
with st.sidebar:
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This tool analyzes cryptocurrency price movements and will eventually include:")
    st.markdown("- Development activity tracking")
    st.markdown("- Social media sentiment analysis") 
    st.markdown("- AI-powered narrative analysis")
    st.markdown("- Divergence detection algorithms")
