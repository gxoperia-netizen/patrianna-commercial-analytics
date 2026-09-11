CREATE OR REPLACE VIEW `patrianna-commercial-analytics.patrianna_analytics.cohort_retention_vintage` AS
WITH user_cohorts AS (
    SELECT 
        user_id,
        DATE_TRUNC(registration_date, MONTH) AS cohort_month
    FROM `patrianna-commercial-analytics.patrianna_analytics.dim_users`
),
monthly_activity AS (
    SELECT DISTINCT
        user_id,
        DATE_TRUNC(transaction_date, MONTH) AS activity_month
    FROM `patrianna-commercial-analytics.patrianna_analytics.fact_transactions`
)
SELECT 
    c.cohort_month,
    DATE_DIFF(a.activity_month, c.cohort_month, MONTH) AS life_month,
    COUNT(DISTINCT c.user_id) AS active_users
FROM user_cohorts c
JOIN monthly_activity a ON c.user_id = a.user_id
GROUP BY 1, 2
ORDER BY 1, 2;