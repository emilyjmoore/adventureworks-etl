import pandas as pd
import mysql.connector
from pymongo import MongoClient
from datetime import datetime

MYSQL_SRC = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yourpassword',
    'database': 'adventureworks'
}

MYSQL_DST = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yourpassword',
    'database': 'adventureworks_dm'
}

MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = "adventureworks_sources"
MONGO_COLL = "customers"

CSV_PATH = "./data/dim_salesperson.csv"

def get_mysql_conn(cfg):
    return mysql.connector.connect(**cfg)

def get_mongo_coll():
    client = MongoClient(MONGO_URI)
    return client[MONGO_DB][MONGO_COLL]

# EXTRACT

def extract_products():
    q = """
    SELECT
      p.ProductID AS product_id,
      p.Name AS product_name,
      p.ProductNumber,
      p.Color,
      p.Size,
      p.ListPrice,
      ps.Name AS product_subcategory,
      pc.Name AS product_category
    FROM adventureworks.product p
    LEFT JOIN adventureworks.productsubcategory ps ON p.ProductSubcategoryID = ps.ProductSubcategoryID
    LEFT JOIN adventureworks.productcategory pc ON ps.ProductCategoryID = pc.ProductCategoryID;
    """
    with get_mysql_conn(MYSQL_SRC) as conn:
        return pd.read_sql(q, conn)

def extract_sales():
    q = """
    SELECT
      soh.SalesOrderID AS order_id,
      soh.OrderDate,
      soh.CustomerID AS customer_id,
      sod.ProductID AS product_id,
      soh.SalesPersonID AS salesperson_id,
      sod.OrderQty AS order_qty,
      sod.UnitPrice AS unit_price,
      sod.LineTotal AS line_total,
      soh.TaxAmt AS tax_amt,
      soh.Freight AS freight
    FROM adventureworks.salesorderheader soh
    JOIN adventureworks.salesorderdetail sod
      ON soh.SalesOrderID = sod.SalesOrderID
    LIMIT 5000;
    """
    with get_mysql_conn(MYSQL_SRC) as conn:
        return pd.read_sql(q, conn)

def extract_customers_from_mongo():
    coll = get_mongo_coll()
    docs = list(coll.find({}, {'_id': 0}))  # drop Mongo _id
    return pd.DataFrame(docs)

def extract_salespeople_csv():
    return pd.read_csv(CSV_PATH)

# TRANSFORM

def build_date_dim(df):
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    date_df = pd.DataFrame({'the_date': df['OrderDate'].unique()})
    date_df['date_id'] = date_df['the_date'].dt.strftime('%Y%m%d').astype(int)
    date_df['year'] = date_df['the_date'].dt.year
    date_df['quarter'] = date_df['the_date'].dt.quarter
    date_df['month'] = date_df['the_date'].dt.month
    date_df['day'] = date_df['the_date'].dt.day
    date_df['day_of_week'] = date_df['the_date'].dt.weekday + 1
    date_df['is_weekend'] = date_df['day_of_week'].isin([6,7]).astype(int)
    date_df['month_name'] = date_df['the_date'].dt.month_name()
    date_df['quarter_name'] = 'Q' + date_df['quarter'].astype(str)
    return date_df

# LOAD

def load_table(df, table):
    conn = get_mysql_conn(MYSQL_DST)
    cursor = conn.cursor()
    cols = ', '.join(df.columns)
    vals = ', '.join(['%s'] * len(df.columns))
    sql = f"INSERT IGNORE INTO {table} ({cols}) VALUES ({vals})"
    data = [tuple(None if pd.isna(v) else v for v in row) for row in df.to_numpy()]
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()
    conn.close()

# MAIN ETL

def main():
    products = extract_products()
    sales = extract_sales()

    customers = extract_customers_from_mongo()

    salespeople = extract_salespeople_csv()

    dates = build_date_dim(sales)

    load_table(dates, 'dim_date')
    load_table(products, 'dim_product')
    load_table(customers, 'dim_customer')
    load_table(salespeople, 'dim_salesperson')

    sales['date_id'] = pd.to_datetime(sales['OrderDate']).dt.strftime('%Y%m%d').astype(int)
    fact_sales = sales[['order_id','date_id','customer_id','product_id','salesperson_id',
                        'order_qty','unit_price','line_total','tax_amt','freight']]
    load_table(fact_sales, 'fact_sales')

if __name__ == "__main__":
    main()
