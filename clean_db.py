from sqlalchemy import create_engine, text

# Connect
db_url = 'postgresql://user:password@localhost:5432/finance_warehouse'
engine = create_engine(db_url)

# Drop everything to start fresh
sql_reset = """
DROP VIEW IF EXISTS v_market_analysis;
DROP VIEW IF EXISTS v_clean_data;
DROP TABLE IF EXISTS raw_stock_data;
"""

print("Cleaning database...")
with engine.connect() as conn:
    conn.execute(text(sql_reset))
    conn.commit()
print("✅ Database cleaned. Ready for new ETL.")