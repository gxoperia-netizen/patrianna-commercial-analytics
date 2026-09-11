import os
import pandas as pd
import numpy as np
from google.cloud import bigquery

# 1. GCP Service Account ავტორიზაცია
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp_key.json'
client = bigquery.Client()

# 2. Dataset-ის შექმნა BigQuery-ში
dataset_id = f"{client.project}.patrianna_raw"
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"
dataset = client.create_dataset(dataset, exists_ok=True)

# 3. მონაცემთა წაკითხვა და B2B Sweepstakes ეკონომიკის სიმულაცია
df = pd.read_csv('data.csv.zip', encoding='unicode_escape')
df = df.dropna(subset=['CustomerID'])
df = df[df['Quantity'] > 0]

df['user_id'] = df['CustomerID'].astype(int).astype(str)
df['transaction_id'] = df['InvoiceNo'].astype(str)
df['transaction_date'] = pd.to_datetime(df['InvoiceDate']).dt.strftime('%Y-%m-%d %H:%M:%S')
df['amount_usd'] = df['Quantity'] * df['UnitPrice']
df['purchased_gc'] = (df['amount_usd'] * 1000).astype(int)
df['bonus_sc'] = df['amount_usd'] * 1.0
df['payment_fee_usd'] = df['amount_usd'] * 0.03

brands = ['Brand_A_Slots', 'Brand_B_Bingo', 'Brand_C_Sweeps']
np.random.seed(42)
df['brand_id'] = np.random.choice(brands, len(df), p=[0.5, 0.3, 0.2])

final_cols = ['user_id', 'transaction_id', 'transaction_date', 'brand_id', 'amount_usd', 'purchased_gc', 'bonus_sc', 'payment_fee_usd']
df_final = df[final_cols]

# 4. BigQuery API-ით პირდაპირი Load
table_id = f"{dataset_id}.fact_transactions_raw"
job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
job = client.load_table_from_dataframe(df_final, table_id, job_config=job_config)
job.result()
print(f"წარმატებით აითვირთა {job.output_rows} სტრიქონი BigQuery-ში.")