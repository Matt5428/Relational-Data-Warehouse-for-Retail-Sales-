-- Dimension: Date
-- This table stores date-related information for analysis, such as day, month, quarter, and year.
CREATE TABLE IF NOT EXISTS retail_dw.dimdate (
    date_id SERIAL PRIMARY KEY,
    full_date DATE NOT NULL,
    day INT NOT NULL,
    month INT NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL
);

-- Dimension: Ship Mode
CREATE TABLE IF NOT EXISTS retail_dw.dimshipmode (
    ship_mode_id SERIAL PRIMARY KEY,
    ship_mode VARCHAR(50) NOT NULL
);

-- Dimension: Customer
CREATE TABLE IF NOT EXISTS retail_dw.dimcustomer (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(80) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20), -- Optional because not all customers may have a postal code
    region VARCHAR(20)
);

-- Dimension: Product
CREATE TABLE IF NOT EXISTS retail_dw.dimproduct (
    product_id VARCHAR(30) PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NULL, -- Optional: Sub-category of the product
    product_name VARCHAR(100) NOT NULL
);

-- Dimension: Order Priority
CREATE TABLE IF NOT EXISTS retail_dw.dimorderpriority (
    order_priority_id SERIAL PRIMARY KEY,
    order_priority VARCHAR(30) NOT NULL
);
-- Fact Table: The `factorder` table stores transactional data for retail sales, 
-- linking to dimension tables such as `dimdate`, `dimshipmode`, `dimcustomer`, 
-- `dimproduct`, and `dimorderpriority` to provide detailed context for each order.
-- Fact Table
CREATE TABLE IF NOT EXISTS retail_dw.factorder (
    order_id VARCHAR(30) PRIMARY KEY,
    order_date_id INT NOT NULL,
    ship_date_id INT NOT NULL,
    ship_mode_id INT NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(30) NOT NULL,
    order_priority_id INT NOT NULL,
    sales DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    discount DECIMAL(4, 2) NOT NULL,
    profit DECIMAL(10, 2) NOT NULL,
    shipping_cost DECIMAL(10, 2) NOT NULL, -- Cost incurred for shipping the order, separate from profit calculation

    FOREIGN KEY (order_date_id) REFERENCES retail_dw.dimdate(date_id),
    FOREIGN KEY (ship_date_id) REFERENCES retail_dw.dimdate(date_id),
    FOREIGN KEY (ship_mode_id) REFERENCES retail_dw.dimshipmode(ship_mode_id),
    FOREIGN KEY (customer_id) REFERENCES retail_dw.dimcustomer(customer_id),
    FOREIGN KEY (product_id) REFERENCES retail_dw.dimproduct(product_id),
    FOREIGN KEY (order_priority_id) REFERENCES retail_dw.dimorderpriority(order_priority_id)
);
