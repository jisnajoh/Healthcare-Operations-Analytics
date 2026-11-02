
-- QUERY 1: NO-SHOW RATE BY GENDER
SELECT
    gender,
    COUNT(*) AS total_appointments,
    SUM(no_show) AS missed_appointments,
    ROUND(AVG(no_show) * 100, 2) AS no_show_rate
FROM appointments
GROUP BY gender
ORDER BY no_show_rate DESC;


-- QUERY 2: NO-SHOW RATE BY AGE GROUP
SELECT
    CASE
        WHEN age BETWEEN 0 AND 17 THEN '0-17'
        WHEN age BETWEEN 18 AND 34 THEN '18-34'
        WHEN age BETWEEN 35 AND 49 THEN '35-49'
        WHEN age BETWEEN 50 AND 64 THEN '50-64'
        ELSE '65+'
    END AS age_group,
    COUNT(*) AS total_appointments,
    SUM(no_show) AS missed_appointments,
    ROUND(AVG(no_show) * 100, 2) AS no_show_rate
FROM appointments
GROUP BY age_group
ORDER BY no_show_rate DESC;


-- QUERY 3: TOP 10 NEIGHBORHOODS BY NO-SHOW RATE
-- Require at least 100 appointments to avoid tiny groups.
SELECT
    neighbourhood,
    COUNT(*) AS total_appointments,
    SUM(no_show) AS missed_appointments,
    ROUND(AVG(no_show) * 100, 2) AS no_show_rate
FROM appointments
GROUP BY neighbourhood
HAVING COUNT(*) >= 100
ORDER BY no_show_rate DESC
LIMIT 10;


-- QUERY 4: NO-SHOW RATE BY SCHEDULING LEAD TIME
SELECT
    CASE
        WHEN waiting_days = 0 THEN 'Same day'
        WHEN waiting_days BETWEEN 1 AND 7 THEN '1-7 days'
        WHEN waiting_days BETWEEN 8 AND 14 THEN '8-14 days'
        WHEN waiting_days BETWEEN 15 AND 30 THEN '15-30 days'
        ELSE '31+ days'
    END AS waiting_group,
    COUNT(*) AS total_appointments,
    SUM(no_show) AS missed_appointments,
    ROUND(AVG(no_show) * 100, 2) AS no_show_rate
FROM appointments
GROUP BY waiting_group
ORDER BY
    CASE waiting_group
        WHEN 'Same day' THEN 1
        WHEN '1-7 days' THEN 2
        WHEN '8-14 days' THEN 3
        WHEN '15-30 days' THEN 4
        ELSE 5
    END;
