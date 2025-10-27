AdventureWorks ETL Data Mart Project

This project demonstrates my understanding of basic data science systems including ETL pipelines, data integration, dimensional modeling, and analytics. It extracts data from MySQL, MongoDB, and CSV, transforms and cleans it using Python, and loads it into a MySQL data mart for analysis.


## Architecture
**Business process modeled:** Retail Sales  
Each row in the fact table represents a product sale (order line item) from the AdventureWorks dataset.  
The data mart follows a **star schema** with one fact table (`fact_sales`) and four dimensions:

| Table | Type | Description |
|--------|------|--------------|
| `dim_date` | Dimension | Time attributes (year, quarter, month, etc.) |
| `dim_customer` | Dimension | Customer demographics and location |
| `dim_product` | Dimension | Product details and categories |
| `dim_salesperson` | Dimension | Sales representatives (from CSV) |
| `fact_sales` | Fact | Sales transactions with quantity, price, tax, freight |

---

## 🧩 Data Sources
| Source | Type | Origin | Notes |
|---------|------|--------|-------|
| **AdventureWorks (MySQL)** | Structured (OLTP) | Tables: `product`, `salesorderheader`, `salesorderdetail` | Used for products, sales, and dates |
| **MongoDB** | Semi-structured (NoSQL) | `customers` collection (from exported JSON) | Represents customer data |
| **Local CSV** | Flat file | `dim_salesperson.csv` | Contains salesperson information |

---

## ⚙️ Technologies Used
- **Python** (ETL scripts)
- **MySQL** (source + data mart)
- **MongoDB** (NoSQL source)
- **Pandas**, **mysql-connector-python**, **pymongo**
- **SQL** for analytic queries

---

## 📂 Repository Structure
adventureworks-etl/
│
├── sql/
│ └── create_adventureworks_dm.sql # Creates the target data mart schema
│
├── etl/
│ └── etl_multisource_pipeline.py # Main ETL pipeline script
│
├── scripts/
│ ├── export_customers_to_json.py # Extracts customer data from MySQL → JSON
│ └── export_salespeople_csv.py # Extracts salesperson data from MySQL → CSV
│
├── data/
│ ├── dim_customers.json # MongoDB JSON file (created by export script)
│ └── dim_salesperson.csv # Local CSV source
│
├── examples/
│ └── example_queries.sql # Aggregation and analysis SQL examples
│
└── README.md
