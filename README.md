AdventureWorks ETL Data Mart Project

This project demonstrates my understanding of basic data science systems including ETL pipelines, data integration, dimensional modeling, and analytics. It extracts data from MySQL, MongoDB, and CSV, transforms and cleans it using Python, and loads it into a MySQL data mart for analysis.


Architecture: Retail Sales  
Each row in the fact table represents a product sale from the AdventureWorks dataset.  
The data mart follows a star schema with one fact table and four dimensions:
- `dim_date` : Time attributes (year, quarter, month, etc.) 
- `dim_customer` : Customer demographics and location 
- `dim_product` : Product details and categories 
- `dim_salesperson` : Sales representatives (from CSV) 
- `fact_sales` : Sales transactions with quantity, price, tax, freight 

Data Sources: 
- Adventureworks (MySQL) : Structured (OLTP); Tables: `product`, `salesorderheader`, `salesorderdetail`; Used for products, sales, and dates - MongoDB : Semi-structured (NoSQL); `customers` collection (from exported JSON); Represents customer data
- Local CSV : Flat file; `dim_salesperson.csv`; Contains salesperson information 

Technologies Used:
- Python : (ETL scripts)
- MySQL : (source + data mart)
- MongoDB : (NoSQL source)
- SQL : for analytic queries

Repository Structure:
The repository is organized to keep the data sources, scripts, and database setup separate:
- sql/: Contains the SQL script that creates the target data mart tables.
- etl/: Holds the primary Python ETL script that runs the entire pipeline.
- scripts/: Contains the utility scripts used to export data into the source files (like the JSON and CSV).
- data/: Where the source files (the CSV and JSON files) used by the pipeline are stored.
- examples/: Includes sample SQL queries for aggregation and basic sales analysis.
