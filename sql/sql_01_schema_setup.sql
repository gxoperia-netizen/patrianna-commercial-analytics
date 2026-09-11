-- Create Datasets (Schemas) for Staging and Analytics layers in BigQuery
CREATE SCHEMA IF NOT EXISTS `patrianna-commercial-analytics.patrianna_raw` OPTIONS(location="US");
CREATE SCHEMA IF NOT EXISTS `patrianna-commercial-analytics.patrianna_analytics` OPTIONS(location="US");