import os
import pandas as pd
import numpy as np
from google.cloud import bigquery
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data

# 1. GCP ავტორიზაცია
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp_key.json'
client = bigquery.Client()

# 2. მონაცემების წამოღება BigQuery-დან
query = """
SELECT 
    user_id,
    transaction_date,
    amount_usd
FROM `patrianna-commercial-analytics.patrianna_analytics.fact_transactions`
"""
df = client.query(query).to_dataframe()

# 3. RFM (Recency, Frequency, Monetary) მატრიცის შექმნა
rfm = summary_data_from_transaction_data(
    df, 
    customer_id_col='user_id', 
    datetime_col='transaction_date', 
    monetary_value_col='amount_usd',
    freq='D'
)

# გავფილტროთ მხოლოდ განმეორებითი ტრანზაქციის მქონე მომხმარებლები
rfm_cal = rfm[rfm['frequency'] > 0].copy()

# 4. BG/NBD მოდელი (Churn Probability - P_alive)
bgf = BetaGeoFitter(penalizer_coef=0.01)
bgf.fit(rfm_cal['frequency'], rfm_cal['recency'], rfm_cal['T'])

rfm_cal['P_alive'] = bgf.conditional_probability_alive(rfm_cal['frequency'], rfm_cal['recency'], rfm_cal['T'])
rfm_cal['churn_probability'] = 1 - rfm_cal['P_alive']
rfm_cal['predicted_purchases_90d'] = bgf.conditional_expected_number_of_purchases_up_to_time(90, rfm_cal['frequency'], rfm_cal['recency'], rfm_cal['T'])

# 5. Gamma-Gamma მოდელი (Monetary / LTV)
ggf = GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(rfm_cal['frequency'], rfm_cal['monetary_value'])

rfm_cal['predicted_90d_ltv'] = ggf.customer_lifetime_value(
    bgf, 
    rfm_cal['frequency'], 
    rfm_cal['recency'], 
    rfm_cal['T'], 
    rfm_cal['monetary_value'], 
    time=3, # 3 თვე (90 დღე)
    freq='D'
)

# 6. შედეგების მომზადება და BigQuery-ში ჩაწერა
ml_results = rfm_cal.reset_index()[['user_id', 'frequency', 'recency', 'P_alive', 'churn_probability', 'predicted_purchases_90d', 'predicted_90d_ltv']]

table_id = f"{client.project}.patrianna_analytics.ml_user_predictions"
job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

job = client.load_table_from_dataframe(ml_results, table_id, job_config=job_config)
job.result()

print(f"ML პროგნოზები წარმატებით ჩაიწერა BigQuery-ში: {table_id}")