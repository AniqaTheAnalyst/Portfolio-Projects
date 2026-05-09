CREATE DATABASE restaurant_db;

USE restaurant_db;


-- outlets: extracted from the outlet column in both CSVs
CREATE TABLE outlets (
    outlet_id   INT IDENTITY(1,1) PRIMARY KEY,
    outlet_name VARCHAR(100) NOT NULL
);

-- products: extracted from inventory.csv
CREATE TABLE products (
    product_id   VARCHAR(10)  PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category     VARCHAR(100),
    unit_cost    DECIMAL(8,2),
    supplier     VARCHAR(150) DEFAULT 'Unknown'
);

-- sales: from sales.csv
CREATE TABLE sales (
    sale_id        INT IDENTITY(1,1) PRIMARY KEY,
    order_id       VARCHAR(10)  NOT NULL,
    item_name      VARCHAR(150) NOT NULL,
    category       VARCHAR(100) DEFAULT 'Uncategorized',
    quantity       INT          NOT NULL,
    unit_price     DECIMAL(8,2) NOT NULL,
    total_amount   DECIMAL(10,2),
    outlet_id      INT,
    order_date     DATE,
    payment_method VARCHAR(50)  DEFAULT 'Unknown',
    FOREIGN KEY (outlet_id) REFERENCES outlets(outlet_id)
);

-- inventory: from inventory.csv
CREATE TABLE inventory (
    inventory_id   INT IDENTITY(1,1) PRIMARY KEY,
    product_id     VARCHAR(10),
    outlet_id      INT,
    stock_level    INT     DEFAULT 0,
    expiry_date    DATE,
    low_stock_flag BIT     DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (outlet_id)  REFERENCES outlets(outlet_id)
);


select * from outlets;

select * from products;

select * from sales;
select * from inventory;



