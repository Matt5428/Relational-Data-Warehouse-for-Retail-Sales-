-- Top 100 country with highest sales
SELECT c.country, SUM(f.sales) as total_sales
FROM factorder f 
JOIN dimcustomer c
ON c.customer_id=f.customer_id
GROUP BY c.country
ORDER BY total_sales DESC 
LIMIT 100;

-- Top 100 country with highest profit
SELECT c.country, SUM(f.profit) as total_profit
FROM factorder f 
JOIN dimcustomer c
ON c.customer_id=f.customer_id
GROUP BY c.country
ORDER BY total_profit DESC 
LIMIT 100;

-- Analyze the relationship between sales and profit on different Discount Level
SELECT
  discount,
  COUNT(*) AS num_orders,
  SUM(sales) AS total_sales,
  SUM(profit) AS total_profit,
  AVG(profit) AS avg_profit_per_order,
  AVG(sales) AS avg_sales_per_order
FROM factorder 
GROUP BY discount
ORDER BY discount;

-- Correlation between discount and profit
SELECT CORR(Discount, Profit) AS discount_profit_correlation
FROM factorder;

-- Discount Level Analysis with CTEs
WITH bucketed_orders AS (
  SELECT
    CASE
      WHEN discount = 0 THEN 'No Discount'
      WHEN discount > 0 AND discount <= 0.1 THEN '0-10%'
      WHEN discount > 0.1 AND discount <= 0.2 THEN '11-20%'
      WHEN discount > 0.2 AND discount <= 0.3 THEN '21-30%'
      WHEN discount > 0.3 AND discount <= 0.4 THEN '31-40%'
      WHEN discount > 0.4 AND discount <= 0.5 THEN '41-50%'
      WHEN discount > 0.5 AND discount <= 0.7 THEN '51-70%'
      ELSE 'Above 70%'
    END AS discount_bucket,
    sales,
    profit
  FROM factorder
)
SELECT
  discount_bucket,
  COUNT(*) AS num_orders,
  SUM(sales) AS total_sales,
  SUM(profit) AS total_profit,
  AVG(profit) AS avg_profit_per_order,
  AVG(sales) AS avg_sales_per_order
FROM bucketed_orders
GROUP BY discount_bucket
ORDER BY
  CASE discount_bucket
    WHEN 'No Discount' THEN 0
    WHEN '0-10%' THEN 1
    WHEN '11-20%' THEN 2
    WHEN '21-30%' THEN 3
    WHEN '31-40%' THEN 4
    WHEN '41-50%' THEN 5
    WHEN '51-70%' THEN 6
    ELSE 7
  END;