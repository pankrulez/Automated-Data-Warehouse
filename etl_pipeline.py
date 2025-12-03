import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

# 1. Connect
db_url = 'postgresql://user:password@localhost:5432/finance_warehouse'
engine = create_engine(db_url)
tickers = ['BTC-USD', 'ETH-USD', 'AAPL', 'TSLA']

def extract_load():
    print("Extracting data...")
    # 1. Download Data
    # group_by='column' ensures the structure is (Price, Ticker)
    data = yf.download(tickers, period="1d", interval="1h", group_by='column')
    
    # 2. Reshape Data (The Fix)
    # level=1 moves 'Ticker' to the index (Rows), leaving Price as Columns.
    data = data.stack(level=1).reset_index()
    
    # 3. Rename Columns to match SQL expectations exactly
    # yfinance index is usually 'Date' or 'Datetime' -> We map to "Datetime"
    # The stacked level is usually named 'Ticker' or 'level_1' -> We map to "Ticker"
    data = data.rename(columns={
        'Date': 'Datetime', 
        'index': 'Datetime', 
        'level_1': 'Ticker'
    })
    
    # 4. Verify columns before upload
    required_cols = ['Datetime', 'Ticker', 'Close']
    for col in required_cols:
        if col not in data.columns:
            # Fallback if yfinance named the ticker column 'Ticker' automatically
            print(f"Warning: Column {col} missing. Columns are: {data.columns}")
    
    # 5. Load to Postgres
    data.to_sql('raw_stock_data', engine, if_exists='append', index=False)
    print(f"✅ Data loaded successfully. Rows: {len(data)}")

if __name__ == "__main__":
    extract_load()