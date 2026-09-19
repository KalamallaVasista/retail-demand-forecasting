# Retail Demand Forecasting & Inventory Optimization

## Project Overview

This project develops a retail analytics platform for forecasting future product demand and supporting inventory planning.

The system uses historical retail sales, calendar events, pricing data, and time-series forecasting techniques to predict future demand at store and product levels.

## Data Source

M5 Forecasting Dataset containing:

- Historical sales
- Store and department information
- Product categories
- Calendar events
- Pricing information

## Tech Stack

- Python
- SQL
- Google BigQuery
- dbt
- Prophet
- LightGBM
- Streamlit
- Git and GitHub

## Project Objective

The objective is to:

- Analyze historical retail demand
- Build clean analytical datasets
- Forecast future product demand
- Store forecasting results in the data warehouse
- Provide inventory recommendations
- Visualize demand forecasts through an interactive dashboard

## Development Status

- Day 1 - Project initialized with Git, GitHub, and required project structure.
- Day 2 - Python virtual environment and project dependencies configured.
- Day 3 - M5 Forecasting dataset loaded and initial data inspection completed.
- Day 4 - Data quality validation and product, store, and date dimensions created.
- Day 5 - Sales and price fact tables created and validated using memory-efficient processing.
- Day 6 - Google Cloud and BigQuery warehouse configured and analytical tables loaded.

## BigQuery Data Warehouse

Google Cloud Project: `vasista-retail-demand-2026`

BigQuery Dataset: `retail_demand`

| Table | Rows |
|---|---:|
| `dim_product` | 3,049 |
| `dim_store` | 10 |
| `dim_date` | 1,969 |
| `fact_prices` | 6,841,121 |
| `fact_sales` | 59,181,090 |

The warehouse follows a dimensional structure containing product, store, and date dimensions together with sales and weekly pricing fact tables.