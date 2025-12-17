

SELECT * 
FROM exchange_rates
LIMIT 10;

--

SELECT 
    EXTRACT(YEAR FROM date_gregorian) AS year,
    ROUND(AVG(close_price) / 10, 2) AS avg_close_tmn
FROM exchange_rates
GROUP BY year
ORDER BY year;


--

SELECT
  DATE_TRUNC('month', date_gregorian) AS month,   
  ROUND(AVG(vol_intraday)::numeric, 4)            
FROM exchange_rates
GROUP BY month
ORDER BY month;

---
SELECT 
  EXTRACT(YEAR FROM date_gregorian) AS year,
  PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY ret_close_close) AS ret_threshold,
  PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY drawdown) AS dd_threshold
FROM exchange_rates
GROUP BY year
ORDER BY year;

---

UPDATE exchange_rates e
SET is_crisis = CASE 
  WHEN e.ret_close_close <= (
           SELECT PERCENTILE_CONT(0.05) 
           WITHIN GROUP (ORDER BY ret_close_close)
           FROM exchange_rates
           WHERE EXTRACT(YEAR FROM date_gregorian) = EXTRACT(YEAR FROM e.date_gregorian)
        )
    OR e.drawdown <= (
           SELECT PERCENTILE_CONT(0.05) 
           WITHIN GROUP (ORDER BY drawdown)
           FROM exchange_rates
           WHERE EXTRACT(YEAR FROM date_gregorian) = EXTRACT(YEAR FROM e.date_gregorian)
        )
  THEN 1 ELSE 0
END;
---
SELECT 
  EXTRACT(YEAR FROM date_gregorian) AS year,
  SUM(is_crisis) AS crisis_days,
  COUNT(*) AS total_days,
  ROUND((100.0 * SUM(is_crisis) / COUNT(*))::numeric, 2) AS pct_crisis_days
FROM exchange_rates
GROUP BY year
ORDER BY year;

---
SELECT 
    date_gregorian,
    close_price,
    ret_close_close,
    drawdown,
    vol_intraday,
    is_crisis
FROM exchange_rates
WHERE is_crisis = 1
ORDER BY date_gregorian;

---
SELECT
    CASE WHEN is_crisis = 1 THEN 'Crisis Day' ELSE 'Normal Day' END AS day_type,
    ROUND(AVG(ret_close_close)::numeric, 4) AS avg_return,
    ROUND(AVG(drawdown)::numeric, 4) AS avg_drawdown,
    COUNT(*) AS num_days
FROM exchange_rates
GROUP BY day_type;
