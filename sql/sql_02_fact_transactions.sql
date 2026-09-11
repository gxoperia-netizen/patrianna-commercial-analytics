CREATE OR REPLACE TABLE `patrianna-commercial-analytics.patrianna_analytics.fact_transactions` AS
SELECT 
    transaction_id,
    user_id,
    brand_id,
    TIMESTAMP(transaction_date) AS transaction_timestamp,
    DATE(transaction_date) AS transaction_date,
    amount_usd,
    purchased_gc,
    amount_usd * 0.15 AS bonus_sc, -- ბონუსი შევამცირეთ 15%-მდე (რეალური iGaming სტანდარტი)
    payment_fee_usd,
    ROUND(amount_usd - (amount_usd * 0.15) - payment_fee_usd, 2) AS estimated_ngr_usd
FROM `patrianna-commercial-analytics.patrianna_raw.fact_transactions_raw`;