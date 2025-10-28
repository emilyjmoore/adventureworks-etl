-- 1. Total revenue by product category and year
SELECT d.year, p.product_category,
       SUM(f.line_total) AS revenue
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY d.year, p.product_category
ORDER BY d.year DESC, revenue DESC;

-- 2. Average order size by state province
SELECT c.state_province,
       AVG(f.line_total) AS avg_order_value
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
GROUP BY c.state_province
ORDER BY avg_order_value DESC;

-- 3. Top 5 salespeople by total sales
SELECT s.first_name, s.last_name, SUM(f.line_total) AS total_sales
FROM fact_sales f
JOIN dim_salesperson s ON f.salesperson_id = s.salesperson_id
GROUP BY s.salesperson_id
ORDER BY total_sales DESC
LIMIT 5;
