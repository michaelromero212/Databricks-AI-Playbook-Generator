# Databricks notebook source
# MAGIC %md
# MAGIC # Ingestion Notebook
# MAGIC This notebook ingests data from S3 to Bronze.

# COMMAND ----------

from pyspark.sql.functions import current_timestamp

# Read from S3
df = spark.read.format("json").load("s3://acme-corp/raw-data/")

# Add ingestion timestamp
df_bronze = df.withColumn("ingestion_time", current_timestamp())

# Write to Bronze table
df_bronze.write.format("delta").mode("append").saveAsTable("raw_clickstream")
