import mysql.connector
import pandas as pd

SRC = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yourpassword',
    'database': 'adventureworks'
}

q = """
SELECT
  c.CustomerID AS customer_id,
  c.AccountNumber,
  c.CustomerType,
  t.Name AS territory_name,
  ct.FirstName,
  ct.LastName,
  ct.EmailAddress,
  a.City,
  sp.Name AS state_province,
  cr.Name AS country_region
FROM adventureworks.customer c
LEFT JOIN adventureworks.individual i ON c.CustomerID = i.CustomerID
LEFT JOIN adventureworks.contact ct ON i.ContactID = ct.ContactID
LEFT JOIN adventureworks.customeraddress ca ON c.CustomerID = ca.CustomerID
LEFT JOIN adventureworks.address a ON ca.AddressID = a.AddressID
LEFT JOIN adventureworks.stateprovince sp ON a.StateProvinceID = sp.StateProvinceID
LEFT JOIN adventureworks.countryregion cr ON sp.CountryRegionCode = cr.CountryRegionCode
LEFT JOIN adventureworks.salesterritory t ON c.TerritoryID = t.TerritoryID
LIMIT 1000;
"""

conn = mysql.connector.connect(**SRC)
df = pd.read_sql(q, conn)
conn.close()

df.to_json('data/dim_customers.json', orient='records', indent=2)
print("Wrote data/dim_customers.json (rows: {})".format(len(df)))
