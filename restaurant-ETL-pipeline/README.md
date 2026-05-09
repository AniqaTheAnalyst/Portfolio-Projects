# Restaurant Operations ETL Pipeline

## Project Description
This project automates the creation and population of a SQL Server database for managing daily sales transactions and inventory stock across multiple restaurant outlets.

It follows a complete **ETL (Extract, Transform, Load)** workflow using Python and SQL Server to migrate raw CSV data into a structured relational database for efficient querying and operational analysis.

---

# Dataset Overview

## Source Files
- `sales_data.csv`
- `inventory_data.csv`

## Sales Dataset Columns
- order_id
- item_name
- category
- quantity
- unit_price
- total_amount
- outlet
- order_date
- payment_method

## Inventory Dataset Columns
- product_id
- product_name
- category
- stock_level
- unit_cost
- expiry_date
- supplier
- outlet
- low_stock_flag

## Data Size
- 47+ sales records
- 40 products
- 4 outlet locations

---

# Key Data Observations

- `unit_cost` contained `$` symbols requiring stripping before numeric conversion
- `order_date` and `expiry_date` had mixed formats and NULL values
- `stock_level` contained negative values requiring correction to zero
- Outlet names stored as text required mapping to integer foreign keys
- Duplicate `product_id` entries were identified and removed

---

# Database Configuration

## Config File
`config.ini`

Stores:
- SQL Server name
- Database name
- Driver configuration
- Trusted certificate settings

## Security Features
- Uses Windows Integrated Security (`Trusted_Connection=yes`)
- No hardcoded passwords in source code
- `TrustServerCertificate=yes` enabled for local development

---

# ETL Workflow (`etl_script.py`)

## Step 1 — Database Connection
Connects to SQL Server using `pyodbc` and settings from `config.ini`.

## Step 2 — Data Extraction
Reads:
- `sales_data.csv`
- `inventory_data.csv`

into Pandas DataFrames.

## Step 3 — Data Transformation
Applies an 8-step cleaning pipeline including:

- Null value handling
- Deduplication
- Text standardization
- Currency cleaning
- Date parsing
- Negative stock correction
- Supplier value filling
- Low stock flag generation

## Step 4 — Existing Data Cleanup
Deletes existing records in child-before-parent order to maintain foreign key integrity.

Deletion Order:
```sql
sales → inventory → outlets → products
```

## Step 5 — Data Loading
Loads cleaned data into 4 relational tables using:
- Parameterized `INSERT` queries
- Null-safe date handling
- Outlet name-to-ID mapping

---

# Technical Highlights

- Uses `pyodbc` with **ODBC Driver 17 for SQL Server**
- Secure credential management via `configparser`
- SQL injection prevention using parameterized queries (`?`)
- Referential integrity maintained using ordered deletes
- `pd.notnull()` used for safe NULL date handling

---

# Skills Utilized

## Database Management
- SQL Server schema design
- Relational database modeling
- Foreign key constraints
- SQL operations:
  - `INSERT`
  - `DELETE`
  - `SELECT`
  - `IF NOT EXISTS`

## Python Programming
### Libraries
- pandas
- pyodbc
- configparser
- sys
- os

### Techniques
- Lambda functions
- Type casting
- Dictionary mapping
- Null handling

## ETL Processes
### Extract
- Multi-file CSV ingestion using `pd.read_csv()`

### Transform
- 8-step data cleaning pipeline

### Load
- Ordered relational inserts
- Per-table commit management

---

# Business Impact

This system enables analysis such as:

- Best-selling items by outlet and category
- Revenue analysis across restaurant locations
- Low stock alerts for inventory replenishment
- Payment method breakdown for financial reporting
- Product expiry tracking to reduce food waste
- Outlet-level performance comparison

---

# Technologies Used

- Python
- Pandas
- SQL Server
- PyODBC
- ConfigParser
- CSV Data Processing

---

# Example Project Structure

```bash
Restaurant-Operations-ETL/
│
├── data/
│   ├── sales_data.csv
│   └── inventory_data.csv
│
├── sql/
│   └── schema.sql
│
├── etl_script.py
├── config.ini
├── requirements.txt
└── README.md
```

---

# Future Improvements

- Power BI dashboard integration
- Streamlit web dashboard
- Automated ETL scheduling
- Logging and exception handling
- Docker containerization

---

# Author

Developed as a portfolio project demonstrating:
- ETL pipeline development
- SQL Server database management
- Data cleaning and transformation
- Python automation
- Relational database design
```
