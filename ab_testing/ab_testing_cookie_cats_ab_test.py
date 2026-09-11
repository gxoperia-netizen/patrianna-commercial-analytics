import pandas as pd
import numpy as np
import zipfile
from scipy.stats import chi2_contingency, mannwhitneyu

# 1. Colab-ის შიდა არქივიდან ფაილის ავტომატურად ამოარქივება და წაკითხვა
with zipfile.ZipFile('cookie_cats.csv.zip', 'r') as zip_ref:
    zip_ref.extractall('extracted_data')

# ვპოულობთ ამოარქივებულ csv ფაილს
df = pd.read_csv('extracted_data/cookie_cats.csv')

# 2. Chi-Square ტესტი 7-დღიან Retention-ზე
contingency_table = pd.crosstab(df['version'], df['retention_7'])
chi2, p_val_ret7, dof, ex = chi2_contingency(contingency_table)

# 3. Mann-Whitney U ტესტი თამაშის რაუნდებზე (sum_gamerounds)
gate_30 = df[df['version'] == 'gate_30']['sum_gamerounds']
gate_40 = df[df['version'] == 'gate_40']['sum_gamerounds']
stat_mw, p_val_mw = mannwhitneyu(gate_30, gate_40)

# 4. Bootstrapping (1000 სიმულაცია)
boot_7d = []
for i in range(1000):
    boot_mean = df.sample(frac=1, replace=True).groupby('version')['retention_7'].mean()
    boot_7d.append(boot_mean)

boot_7d = pd.DataFrame(boot_7d)
boot_7d['diff_%'] = (boot_7d['gate_30'] - boot_7d['gate_40']) / boot_7d['gate_40'] * 100

print(f"--- COOKIE CATS A/B EXPERIMENT RESULTS ---")
print(f"Chi-Square 7-Day Retention P-Value: {p_val_ret7:.5f}")
print(f"Mann-Whitney U Gamerounds P-Value: {p_val_mw:.5f}")
print(f"Probability Gate 30 outperforms Gate 40: {(boot_7d['diff_%'] > 0).mean() * 100:.2f}%")