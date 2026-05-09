Restaurant Operations ETL Pipeline
Project Description: This project automates the creation and population of a SQL Server database for managing daily sales transactions and inventory stock across multiple restaurant outlets. It involves ETL (Extract, Transform, Load) processes to migrate raw CSV data into a structured relational database, enabling efficient querying and operational analysis of restaurant performance.
Dataset Overview
Source Files: sales_data.csv, inventory_data.csv
Sales Columns: order_id, item_name, category, quantity, unit_price, total_amount, outlet, order_date, payment_method
Inventory Columns: product_id, product_name, category, stock_level, unit_cost, expiry_date, supplier, outlet, low_stock_flag
Data Size: 47+ sales records, 40 products across 4 outlet locations
Key Observations:
unit_cost contained $ symbols requiring stripping before numeric conversion
order_date and expiry_date had mixed formats and NULL values
stock_level contained negative values requiring correction to zero
Outlet names stored as text required mapping to integer foreign keys
Duplicate product_id entries identified and removed
Database Configuration
Config File: config.ini
Stores SQL Server connection settings (server, database, driver, trusted_certificate)
Uses Windows Integrated Security (Trusted_Connection=yes) — no hardcoded passwords
TrustServerCertificate=yes configured for local development environment
Script Workflow (etl_script.py)
Step 1: Connects to SQL Server via pyodbc using settings from config.ini
Step 2: Reads sales_data.csv and inventory_data.csv into pandas DataFrames
Step 3: Applies 8-step transformation to each dataset — null removal, deduplication, text standardisation, currency cleaning, date parsing, negative stock correction, supplier fill, low stock flagging
Step 4: Deletes existing records in child-before-parent order to respect foreign key constraints
Step 5: Loads cleaned data into 4 relational tables using parameterised INSERT queries with null-safe date handling and outlet name-to-ID mapping
Technical Highlights
Uses pyodbc with ODBC Driver 17 for SQL Server connectivity
Credentials managed securely via configparser — no sensitive data in source code
All SQL queries use ? parameterised placeholders — protected against SQL injection
Foreign key delete order (sales → inventory → outlets → products) maintains referential integrity
Null-safe date conversion using pd.notnull() prevents runtime crashes on missing dates
Skills Utilized
Database Management
SQL Server schema design with 4 relational tables and foreign key constraints
SQL operations: DELETE, INSERT, IF NOT EXISTS, SELECT
Python Programming
Libraries: pyodbc, pandas, configparser, sys, os
Techniques: lambda functions, type casting, dictionary mapping, null handling
ETL Processes
Extract: Multi-file CSV ingestion via pd.read_csv()
Transform: 8-step cleaning pipeline per dataset
Load: Ordered relational insert with per-table commit management
Business Impact
Enables queries such as: 
Best-selling items and revenue by outlet and category
Low stock alerts for inventory replenishment
Payment method breakdown for financial reporting
Products approaching expiry to reduce food waste
Outlet-level performance comparison

