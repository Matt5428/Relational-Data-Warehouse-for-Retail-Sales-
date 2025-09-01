# Relational Data Warehouse for Retail Sales

## Overview
This project implements a robust relational data warehouse designed to simulate a real-world retail analytics pipeline. It covers the end-to-end process of data modeling, ETL (Extract, Transform, Load), data warehousing, and analytical querying. The objective is to provide a scalable framework for retail sales data analysis, reporting, and business intelligence.

## Dataset

- **Source:** [Global Super Store Dataset (Kaggle)](https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset)

To download and use the dataset:

1. **Install Kaggle CLI:**
   ```bash
   pip install kaggle
   ```
2. **Generate Kaggle API Token:**
   - Go to your Kaggle profile → Settings
   - Under "API," click "Create New Token" to download `kaggle.json`

3. **Set up Kaggle API credentials:**
   ```bash
   mkdir ~/.kaggle
   mv /path/to/kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```

4. **Download and extract the CSV file:**
   ```bash
   kaggle datasets download -d apoorvaappz/global-super-store-dataset
   unzip global-super-store-dataset.zip '*.csv' -d data/
   ```

## Project Objectives

- Design a normalized star schema for retail analytics
- Implement an ETL pipeline in Python
- Load cleansed data into a PostgreSQL database
- Perform data analysis using SQL queries

## Tools & Technologies

- **PostgreSQL:** Relational database modeling and analytics
- **Python (Pandas, SQLAlchemy):** ETL scripting, data transformation
- **Pandas:** Data cleaning and manipulation

## Data Warehouse Schema

### Fact Table: `fact_order`
- `order_id` (Primary Key)
- `order_date_id` (FK to `dim_date`)
- `ship_date_id` (FK to `dim_date`)
- `ship_mode_id` (FK to `dim_ship_mode`)
- `customer_id` (FK to `dim_customer`)
- `product_id` (FK to `dim_product`)
- `order_priority_id` (FK to `dim_order_priority`)
- `sales`
- `quantity`
- `discount`
- `profit`
- `shipping_cost`

### Dimension Tables

1. **`dim_date`** (includes order and ship dates)
   - `date_id` (PK)
   - `full_date`
   - `day`
   - `month`
   - `quarter`
   - `year`

2. **`dim_ship_mode`**
   - `ship_mode_id` (PK)
   - `ship_mode`

3. **`dim_customer`**
   - `customer_id` (PK)
   - `customer_name`
   - `segment`
   - `city`
   - `state`
   - `country`
   - `postal_code`
   - `region`

4. **`dim_product`**
   - `product_id` (PK)
   - `category`
   - `sub_category`
   - `product_name`

5. **`dim_order_priority`**
   - `order_priority_id` (PK)
   - `order_priority`

## Getting Started

1. **Clone this repository:**
   ```bash
   git clone https://github.com/Matt5428/Relational-Data-Warehouse-for-Retail-Sales.git
   cd Relational-Data-Warehouse-for-Retail-Sales
   ```

2. **Set up your Python environment and dependencies.**

3. **Download the dataset (see above).**

4. **Run the ETL pipeline scripts to load data into PostgreSQL.**

## SQL Analytics & Insights

This project includes a suite of advanced SQL queries designed to extract meaningful insights from retail sales data. The key analyses provided in [`sql_script/sql_queries.sql`](sql_script/sql_queries.sql) include:

### 1. Top Countries by Sales and Profit
- **Top 100 Countries by Sales:**  
  Identifies the 100 countries with the highest total sales, enabling targeted market analysis and strategic planning.
- **Top 100 Countries by Profit:**  
  Ranks countries based on total profit to help prioritize high-performing regions.

### 2. Discount Impact Analysis
- **Sales and Profit by Discount Level:**  
  Aggregates order counts, total sales, and profit, as well as average sales and profit per order, grouped by discount level. This analysis reveals how discounting strategies affect revenue and profitability.
- **Correlation between Discount and Profit:**  
  Computes the statistical correlation between the discount applied and the resulting profit, highlighting the overall relationship and potential trade-offs in discounting.

### 3. Discount Bucket Analysis (with CTEs)
- **Bucketed Discount Analysis:**  
  Orders are grouped into meaningful discount ranges (e.g., No Discount, 0-10%, 11-20%, etc.) using Common Table Expressions (CTEs). For each bucket, the script computes:
  - Number of orders
  - Total sales
  - Total profit
  - Average profit per order
  - Average sales per order  
  This helps stakeholders evaluate the business impact of different discount strategies at a granular level.

**Usage:**  
To run these queries, connect to your data warehouse and execute the statements in [`sql_script/sql_queries.sql`](sql_script/sql_queries.sql). Each query is documented in the SQL file for easy reference and modification.

## Key Analytical Results

### 1. Top Countries by Sales and Profit

- **Top Country by Sales:** United States ($1,912,794.40)
- **Top Country by Profit:** United States ($225,862.81)

Other high-performing countries include Australia, France, India, and China.  
See [`analysis/country_sales.csv`](analysis/country_sales.csv) and [`analysis/country_profit.csv`](analysis/country_profit.csv) for the full rankings.

---

### 2. Discount Impact Analysis

- **Correlation between Discount and Profit:**  
  The correlation coefficient between discount and profit is **-0.37** (see [`analysis/correlation.csv`](analysis/correlation.csv)), indicating that higher discounts are generally associated with lower profits.

---

### 3. Discount Bucket Sales Summary

The [`analysis/discount_bucket.csv`](analysis/discount_bucket.csv) file summarizes sales and profit by discount bucket:

| Discount Bucket | Num Orders | Total Sales   | Total Profit  | Avg Profit/Order | Avg Sales/Order |
|-----------------|------------|--------------|--------------|------------------|-----------------|
| No Discount     | 13,697     | $5,158,578   | $1,307,538   | $95.46           | $376.62         |
| 0-10%           | 453        | $316,679     | $65,644      | $144.91          | $699.07         |
| 11-20%          | 2,762      | $1,610,175   | $241,512     | $87.44           | $582.97         |
| 21-30%          | 3,030      | $1,086,389   | $87,428      | $28.85           | $358.54         |
| 31-40%          | 401        | $272,278     | -$33,488     | -$83.51          | $678.99         |
| 41-50%          | 2,767      | $749,118     | -$265,779    | -$96.05          | $270.73         |
| 51-70%          | 1,793      | $266,071     | -$280,603    | -$156.50         | $148.39         |
| Above 70%       | 132        | $17,075      | -$32,325     | -$244.89         | $129.36         |

**Insights:**
- Orders with no discount have the highest total sales and profit.
- Higher discount buckets (above 40%) often result in negative average profit per order, indicating losses.
- Moderate discounts (0-20%) still yield positive profits.

See [`analysis/discount_bucket.csv`](analysis/discount_bucket.csv) for the full breakdown.