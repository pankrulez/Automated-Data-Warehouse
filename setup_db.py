from sqlalchemy import create_engine, text

# 1. Connect to Database
# Make sure this matches your docker-compose credentials
db_url = 'postgresql://user:password@localhost:5432/finance_warehouse'
engine = create_engine(db_url)

# 2. Define the SQL Transformations
# We use 'text' to safely execute raw SQL
sql_commands = """
-- View 1: Deduplicate Data
CREATE OR REPLACE VIEW v_clean_data AS
WITH deduplicated AS (
    SELECT 
        *,
        ROW_NUMBER() OVER(PARTITION BY "Ticker", "Datetime" ORDER BY "Datetime" DESC) as row_num
    FROM raw_stock_data
)
SELECT * FROM deduplicated WHERE row_num = 1;

-- View 2: Calculate Moving Averages & Returns
CREATE OR REPLACE VIEW v_market_analysis AS
SELECT 
    "Datetime",
    "Ticker",
    "Close",
    AVG("Close") OVER(
        PARTITION BY "Ticker" 
        ORDER BY "Datetime" 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as ma_7,
    LAG("Close", 1) OVER(
        PARTITION BY "Ticker" 
        ORDER BY "Datetime"
    ) as prev_close,
    ("Close" - LAG("Close", 1) OVER(PARTITION BY "Ticker" ORDER BY "Datetime")) 
    / NULLIF(LAG("Close", 1) OVER(PARTITION BY "Ticker" ORDER BY "Datetime"), 0) as daily_return
FROM v_clean_data;
"""

# 3. Execute the SQL
print("Applying SQL Transformations...")
try:
    with engine.connect() as connection:
        # We split by ';' to run commands one by one, or run as a block
        connection.execute(text(sql_commands))
        connection.commit() # Commit the changes!
    print("✅ Success! Views 'v_clean_data' and 'v_market_analysis' created.")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Tip: Did you run 'etl_pipeline.py' first? The table 'raw_stock_data' must exist before creating views.")