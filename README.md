# Patrianna Commercial Analytics & Advanced A/B Testing Suite

This project was built to comprehensively showcase the commercial ecosystem of Patrianna (B2B Social Gaming) — starting from raw data ingestion and BigQuery architecture, all the way to predictive machine learning and C-level financial dashboards.

Often in analytical projects, things stop at pretty visuals. That's why my main focus here was on solid logic, real margin management models (such as tracking GGR down to NGR margin leakage, bonuses, and payment gateway fees), and statistical rigor.

### Key Technologies & Logic:

The entire data pipeline is built in Google BigQuery. Using Python, I set up an ETL process that transformed raw transaction logs into an organized analytical structure. Furthermore, the project includes two robust modules:

1. **Predictive ML Pipeline (LTV & Churn):** Using the `lifetimes` library and BG/NBD / Gamma-Gamma models, I calculated individual customer survival probabilities ($P_{alive}$) and expected 90-day LTV. These predictions are automatically sent back to BigQuery, where DAX powers automated risk tiers (such as critical VIP risk zones).
2. **Advanced A/B Testing (Cookie Cats):** I ran a full statistical analysis on mobile gaming metrics — a Chi-Square test on 7-day retention, a Mann-Whitney U test on game rounds, and a 1,000-iteration bootstrapping simulation. This proved a 99.9% probability of why an earlier progression gate (Gate 30) outperforms a later one.

### Repository Structure:
* `sql/` — BigQuery schemas, ETL transaction facts, and vintage cohort retention views.
* `ml_pipeline/` — Python scripts for machine learning and predictive modeling.
* `ab_testing/` — Cookie Cats advanced statistical A/B testing script.
* `power_bi/` — A 3-page interactive Executive Dashboard (`.pbix`) combining commercial health, cross-brand cannibalization matrices, and risk scatter plots.
* `presentation/` — C-level strategic PDF presentation deck.

### How to Review and Verify the Report:
If you'd like to explore the Power BI dashboard interactively, you can download `power_bi/patrianna_commercial_dash.pbix` and open it in Power BI Desktop. The SQL scripts and Python codes are fully structured and ready for review in their respective directories.
