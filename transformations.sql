-- 1. Create a View for Cleaned Data (Handling Duplicates)
DROP VIEW IF EXISTS v_clean_data;
GO
CREATE VIEW v_clean_data AS
WITH deduplicated AS (
    SELECT 
        *,
        -- Row Number helps us identify duplicate pulls for the same timestamp
        ROW_NUMBER() OVER(PARTITION BY "Ticker", "Datetime" ORDER BY "Datetime" DESC) as row_num
    FROM raw_stock_data
)
SELECT * FROM deduplicated WHERE row_num = 1;
GO
-- 2. Analytical View: Moving Averages & Volatility
DROP VIEW IF EXISTS v_market_analysis;
GO
CREATE VIEW v_market_analysis AS
SELECT 
    "Datetime",
    "Ticker",
    "Close",
    
    -- Window Function: 7-Period Moving Average
    AVG("Close") OVER(
        PARTITION BY "Ticker" 
        ORDER BY "Datetime" 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as ma_7,
    
    -- Window Function: Previous Closing Price (Lag)
    LAG("Close", 1) OVER(
        PARTITION BY "Ticker" 
        ORDER BY "Datetime"
    ) as prev_close,
    
    -- Calculated: Daily Return
    ("Close" - LAG("Close", 1) OVER(PARTITION BY "Ticker" ORDER BY "Datetime")) 
    / NULLIF(LAG("Close", 1) OVER(PARTITION BY "Ticker" ORDER BY "Datetime"), 0) as daily_return

FROM v_clean_data;