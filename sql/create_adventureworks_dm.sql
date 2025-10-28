DROP DATABASE IF EXISTS adventureworks_dm;
CREATE DATABASE IF NOT EXISTS adventureworks_dm;
USE adventureworks_dm;

CREATE TABLE dim_date (
  date_id INT PRIMARY KEY,
  the_date DATE,
  year INT,
  quarter INT,
  month INT,
  day INT,
  day_of_week INT,
  is_weekend TINYINT,
  month_name VARCHAR(20),
  quarter_name VARCHAR(10)
);

CREATE TABLE dim_product (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(200),
  product_number VARCHAR(50),
  color VARCHAR(50),
  size VARCHAR(50),
  list_price DECIMAL(12,2),
  product_category VARCHAR(100),
  product_subcategory VARCHAR(100)
);

CREATE TABLE dim_customer (
  customer_id INT PRIMARY KEY,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  email_address VARCHAR(200),
  city VARCHAR(100),
  state_province VARCHAR(100),
  country_region VARCHAR(100)
);

CREATE TABLE dim_salesperson (
  salesperson_id INT PRIMARY KEY,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  territory VARCHAR(100),
  email VARCHAR(200)
);

CREATE TABLE fact_sales (
  fact_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  order_id INT,
  date_id INT,
  customer_id INT,
  product_id INT,
  salesperson_id INT,
  order_qty INT,
  unit_price DECIMAL(12,2),
  line_total DECIMAL(14,2),
  tax_amt DECIMAL(12,2),
  freight DECIMAL(12,2),
  FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
  FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
  FOREIGN KEY (salesperson_id) REFERENCES dim_salesperson(salesperson_id)
);
