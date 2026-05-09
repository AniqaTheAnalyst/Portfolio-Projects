
"""""
Restaurant ETL Script
Extract, Transform, Load data for restaurant operations
"""

import configparser
import pandas as pd
import pyodbc
import sys
import os



# Read config file
config = configparser.ConfigParser()
config.read('config.ini')

# Load settings
server = config['sqlserver']['server']
database = config['sqlserver']['database']
driver = config['sqlserver']['driver']
trust_cert = config['sqlserver'].get(
    'trusted_certificate', 'no')  # fallback to 'no' if missing

# Build connection string
conn_str = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
    f"TrustServerCertificate={trust_cert};"
    "Connection Timeout=10;"
)


# Connect to SQL Server
try:
    conn = pyodbc.connect(conn_str)
    print("Connected successfully!")
except pyodbc.OperationalError as e:
    print(f"\n[Connection Failed]")
    print(f"  Server  : {server}")
    print(f"  Database: {database}")
    print(f"  Driver  : {driver}")
    print(f"\nError: {e}")
    sys.exit(1)


# ── EXTRACT ──────────────────────────────────────────
print("\n📥 Extracting data from CSV files...")
sales_df = pd.read_csv('data/sales.csv')
inventory_df = pd.read_csv('data/inventory.csv')

print(f"   sales.csv     → {len(sales_df)} rows loaded")
print(f"   inventory.csv → {len(inventory_df)} rows loaded")

# d1 = sales_df.head(20)
# print(d1)


# TRANSFORM: SALES
# 1. Remove duplicate orders
sales_df.drop_duplicates(subset='order_id', inplace=True)

# 2. Standardise text columns
sales_df['item_name'] = sales_df['item_name'].str.title().str.strip()
sales_df['category'] = sales_df['category'].str.title().str.strip()
sales_df['outlet'] = sales_df['outlet'].str.title().str.strip()
sales_df['payment_method'] = sales_df['payment_method'].str.title().str.strip()

# 3. Fix price column
# disable regex to avoid confusion as $ has special meaning
sales_df["unit_price"] = sales_df["unit_price"].astype(
    "str").str.replace('$', "", regex=False)
sales_df["unit_price"] = pd.to_numeric(sales_df["unit_price"], errors='coerce')

# 4. Remove rows where price could not be parsed
sales_df.dropna(subset=['unit_price'], inplace=True)
# 5. Remove rows with zero or negative quantity
sales_df = sales_df[sales_df['quantity'] > 0]

# 6. Standardise date format
sales_df['order_date'] = pd.to_datetime(
    sales_df['order_date'], dayfirst=True, errors='coerce')

# 7. Fill missing values
sales_df['category'] = sales_df['category'].fillna('Uncategorized')
sales_df['payment_method'] = sales_df['payment_method'].fillna('Unknown')

# 8. Calculate total_amount
sales_df['total_amount'] = sales_df['quantity'] * sales_df['unit_price']


# ── TRANSFORM: INVENTORY ─────────────────────────────
print("\n🔧 Transforming inventory data...")

inventory_df.dropna(subset=['product_id', 'product_name'], inplace=True)

inventory_df = inventory_df[
    inventory_df['product_id'].str.strip() != ""
]
inventory_df = inventory_df[
    inventory_df['product_name'].str.strip() != ""
]


# 2. Remove duplicates
inventory_df.drop_duplicates(subset='product_id', inplace=True)

# 3. Standardise text columns
inventory_df['product_name'] = inventory_df['product_name'].str.title().str.strip()
inventory_df['category'] = inventory_df['category'].str.title().str.strip()
inventory_df['outlet'] = inventory_df['outlet'].str.title().str.strip()


# 4. Fix unit_cost
inventory_df["unit_cost"] = inventory_df["unit_cost"].astype(
    "str").str.replace('$', "", regex=False)
inventory_df["unit_cost"] = pd.to_numeric(
    inventory_df["unit_cost"], errors='coerce')

# 5. Fix negative stock levels — set to 0
inventory_df['stock_level'] = inventory_df['stock_level'].apply(
    lambda x: 0 if x < 0 else x)

# 6. Standardise date format
inventory_df['expiry_date'] = pd.to_datetime(
    inventory_df['expiry_date'], dayfirst=True, errors='coerce'
)

# 7. Fill missing suppliers
inventory_df['supplier'] = inventory_df['supplier'].fillna('Unknown')

# 8. Flag low stock
inventory_df['low_stock_flag'] = inventory_df['stock_level'].apply(
    lambda x: 1 if x < 20 else 0)

print(f"row after cleaning{len(inventory_df)}")


d2 = inventory_df.head(30)
print(d2)

# d2.keys()




cursor = conn.cursor()


# Extract unique outlet names from both files
all_outlets = pd.concat([
    sales_df['outlet'],
    inventory_df['outlet']
]).dropna().unique()

for outlet_name in all_outlets:
    cursor.execute("""
        IF NOT EXISTS (SELECT 1 FROM outlets WHERE outlet_name = ?)
        INSERT INTO outlets (outlet_name) VALUES (?)
    """, outlet_name, outlet_name)

conn.commit()
print("Outlets loaded")

# Build outlet lookup dictionary {name: id}
cursor.execute("SELECT outlet_id, outlet_name FROM outlets")
outlet_map = {row.outlet_name: row.outlet_id for row in cursor.fetchall()}


for _, row in inventory_df.iterrows():
    cursor.execute("""
        IF NOT EXISTS (SELECT 1 FROM products WHERE product_id = ?)
        INSERT INTO products (product_id, product_name, category, unit_cost, supplier)
        VALUES (?, ?, ?, ?, ?)
    """,
                   row['product_id'],
                   row['product_id'], row['product_name'], row['category'],
                   row['unit_cost'],  row['supplier'])

conn.commit()
print("Products loaded")


sales_records = []

for _, row in sales_df.iterrows():
    outlet_id = outlet_map.get(row['outlet'])
    sales_records.append((
        row['order_id'],
        row['item_name'],
        row['category'],
        int(row['quantity']),
        float(row['unit_price']),
        float(row['total_amount']),
        outlet_id,
        row['order_date'].date() if pd.notna(row['order_date']) else None,
        row['payment_method']
    ))

cursor.executemany("""
    INSERT INTO sales
    (order_id, item_name, category, quantity, unit_price,
     total_amount, outlet_id, order_date, payment_method)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", sales_records)

conn.commit()
print(f"Sales loaded: {len(sales_records)} rows")


inventory_records = []

for _, row in inventory_df.iterrows():
    outlet_id = outlet_map.get(row['outlet'])
    inventory_records.append((
        row['product_id'],
        outlet_id,
        int(row['stock_level']),
        row['expiry_date'].date() if pd.notna(row['expiry_date']) else None,
        int(row['low_stock_flag'])
    ))

cursor.executemany("""
    INSERT INTO inventory
    (product_id, outlet_id, stock_level, expiry_date, low_stock_flag)
    VALUES (?, ?, ?, ?, ?)
""", inventory_records)

conn.commit()
print(f"Inventory loaded: {len(inventory_records)} rows")


cursor.close()
conn.close()
print("ETL complete. Connection closed.")
