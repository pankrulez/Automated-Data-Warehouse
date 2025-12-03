import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# 1. Configuration
st.set_page_config(page_title="Financial Data Warehouse", layout="wide")
st.title("📈 Live Financial Data Warehouse")

# 2. Database Connection (Cached for performance)
# In a real app, use st.secrets for the password!
@st.cache_resource
def init_connection():
    db_url = 'postgresql://user:password@localhost:5432/finance_warehouse'
    return create_engine(db_url)

engine = init_connection()

# 3. Sidebar: User Controls
st.sidebar.header("Filter Data")
# We query distinct tickers directly from the DB to populate the dropdown
try:
    tickers = pd.read_sql("SELECT DISTINCT \"Ticker\" FROM v_market_analysis", engine)
    selected_ticker = st.sidebar.selectbox("Select Asset", tickers['Ticker'])
except Exception as e:
    # This will print the ACTUAL error on the screen
    st.error(f"Detailed Connection Error: {e}")
    st.stop()

# 4. Fetch Data (The "View" Layer)
# We use the SQL View we created earlier, not the raw table.
query = f"""
    SELECT * FROM v_market_analysis 
    WHERE "Ticker" = '{selected_ticker}' 
    ORDER BY "Datetime" ASC
"""
df = pd.read_sql(query, engine)

# 5. Key Metrics (The "Business" Layer)
latest_data = df.iloc[-1]
prev_data = df.iloc[-2]

col1, col2, col3 = st.columns(3)
col1.metric("Current Price", f"${latest_data['Close']:.2f}", 
            f"{latest_data['daily_return']*100:.2f}%")
col2.metric("7-Day Moving Avg", f"${latest_data['ma_7']:.2f}")
col3.metric("Volatility (Std Dev)", f"${df['daily_return'].std():.4f}")

# 6. Visualizations (The "Insight" Layer)
tab1, tab2 = st.tabs(["Price History", "Daily Returns"])

with tab1:
    st.subheader(f"{selected_ticker} Price Trend")
    # We plot the Closing Price vs. the Moving Average calculated in SQL
    fig = px.line(df, x='Datetime', y=['Close', 'ma_7'], 
                  color_discrete_map={'Close': 'blue', 'ma_7': 'orange'})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Daily Returns Distribution")
    fig2 = px.histogram(df, x="daily_return", nbins=50, title="Risk Profile")
    st.plotly_chart(fig2, use_container_width=True)