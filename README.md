# Commercial Analytics & Advanced A/B Testing Portfolio

This project was built to showcase a complete, end-to-end commercial analytics workflow—moving from raw data ingestion and SQL warehouse architecture to predictive machine learning and executive-level reporting. 

Instead of relying on synthetic or toy data, the project is built using well-established public datasets to solve realistic business and product problems:
* **Online Retail Dataset (Kaggle/UCI):** Used for transactional pipeline engineering, financial metrics calculation, and predictive LTV/churn modeling.
* **Cookie Cats Dataset (Kaggle):** Used for rigorous mobile gaming A/B testing and statistical validation.

### Core Components & Architecture:

1. **Data Warehousing & ETL (Google BigQuery & Python):** 
   Raw transaction logs are ingested, cleaned, and transformed into an analytical structure. I built automated scripts to handle core business logic, such as calculating net revenue conversions, payment gateway fees, and promotional overhead.

2. **Predictive ML Pipeline (LTV & Churn):** 
   Using Python’s `lifetimes` library (BG/NBD and Gamma-Gamma models), the pipeline calculates individual customer survival probabilities ($P_{alive}$) and expected 90-day LTV based on Recency, Frequency, and Monetary (RFM) metrics. These outputs are fed back into BigQuery to power dynamic risk segmentation.

3. **Advanced A/B Testing (Cookie Cats Module):** 
   To evaluate product changes, I ran a full statistical evaluation comparing two mobile game progression gates (`gate_30` vs `gate_40`). This includes a Chi-Square test on 7-day retention ($p = 0.00160$), a Mann-Whitney U test on gameplay distribution, and a 1,000-iteration bootstrapping simulation proving a 99.9% probability of superiority for the earlier gate.

4. **Executive BI Reporting:** 
   A 3-page interactive Power BI dashboard (`.pbix`) built to translate these complex metrics into clear commercial insights, featuring risk scatter plots, retention trends, and performance drivers.

### Repository Structure:
* `sql/` - BigQuery schemas, raw data ingestion scripts, and analytical views.
* `ml_pipeline/` - Python scripts for BG/NBD & Gamma-Gamma predictive modeling.
* `ab_testing/` - Statistical A/B testing scripts and evaluation logic.
* `power_bi/` - Executive PBIX dashboard file.
* `presentation/` - C-level strategic PDF presentation deck.

### How to Review:
You can explore the SQL and Python code directly within their respective directories. For the dashboard, download the `.pbix` file from the `power_bi/` folder and open it in Power BI Desktop.
