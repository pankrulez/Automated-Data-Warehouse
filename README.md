# 🏦 Automated Financial Data Warehouse

![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)
![SQL](https://img.shields.io/badge/SQL-Advanced-critical)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Status](https://img.shields.io/badge/Status-Production--Ready-success)

---

## 📌 Executive Summary

**The Problem:**  
Most data science projects rely on static CSVs, which become outdated immediately. Real-world analysis requires live, reliable data pipelines.

**The Solution:**  
I built an end-to-end **ELT (Extract, Load, Transform) pipeline** that ingests live crypto and stock data, stores it in a Dockerized PostgreSQL warehouse, and performs complex analytical transformations (window functions, volatility calculations) directly within the database.

**The Result:**  
A fault-tolerant data warehouse powering a live Streamlit dashboard with **<100ms latency** for key financial metrics.

---

## 🏗️ Architecture

1. **Extract**  
   Python script fetches hourly OHLCV data for:
   - BTC
   - ETH
   - AAPL
   - TSLA  
   using `yfinance`.

2. **Load**  
   Raw data is **upserted** into a PostgreSQL database running inside a Docker container.

3. **Transform (SQL-First)**  
   All data cleaning and feature engineering happens inside SQL using **views**:
   - **Deduplication:** `ROW_NUMBER()` for overlapping API pulls  
   - **Feature Engineering:**  
     - 7-day moving averages  
     - Daily returns  
     using **SQL Window Functions**

4. **Visualize**  
   A Streamlit dashboard connects directly to SQL views and renders live interactive charts.

---

## 🛠️ Tech Stack & Key Skills

| Component        | Technology              | Key Skills Demonstrated |
|------------------|--------------------------|--------------------------|
| Orchestration    | Python / Cron            | Automated ETL, API Error Handling |
| Warehouse        | PostgreSQL 13            | Star Schema Design, Indexing |
| Transformation  | Advanced SQL             | CTEs, Window Functions (`OVER`, `PARTITION BY`), Views |
| Infrastructure  | Docker, docker-compose  | Containerization, Networking |
| Frontend         | Streamlit + Plotly       | Low-latency Visualization, SQL Connectivity |

---

## 📊 Dashboard Preview

_(Generated dynamically from the SQL warehouse)_

- **Live Metrics:**  
  Real-time price, 7-day trend, and volatility risk

- **Interactive Charts:**  
  Zoomable price history vs. moving averages

- **Risk Analysis:**  
  Histogram of daily returns to visualize tail risk

---

## 💻 How to Run This

### 1. Prerequisites

- Docker Desktop installed  
- Python 3.8+

---

### 2. Start the Database

```bash
# Spin up the Postgres container
docker-compose up -d
```

---

### 3. Initialize the Pipeline

```bash
# Install dependencies
pip install -r requirements.txt

# Run the ETL script (Extract -> Load)
python etl_pipeline.py

# Apply SQL Transformations (Creates Views & Analytics)
python setup_db.py
```

---

### 4. Launch the Dashboard

```bash
streamlit run app.py
```

Access the dashboard at:

```
http://localhost:8501
```

---

## 🧠 SQL Logic Example

```sql
SELECT 
    "Datetime",
    "Ticker",
    "Close",
    -- 7-Period Moving Average calculated in SQL
    AVG("Close") OVER(
        PARTITION BY "Ticker" 
        ORDER BY "Datetime" 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS ma_7
FROM v_clean_data;
```

---

## 👤 Author

**Pankaj**
