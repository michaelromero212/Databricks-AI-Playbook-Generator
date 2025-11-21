# COMMAND ----------
# Silver to Gold: Risk Scoring Model
# Applies ML model to transaction history to generate risk scores.

import mlflow
import pandas as pd
from pyspark.sql.functions import *

# COMMAND ----------

# Load Silver Data
df_tx = spark.read.table("silver_transactions")
df_cust = spark.read.table("silver_customers_scd2").filter("is_current = true")

# Feature Engineering
df_features = df_tx.join(df_cust, "account_id") \
    .groupBy("account_id") \
    .agg(
        avg("amount").alias("avg_tx_amount"),
        count("tx_id").alias("tx_count"),
        max("tx_timestamp").alias("last_tx_date")
    )

# COMMAND ----------

# Load Model
model_uri = "models:/FraudDetection/Production"
model = mlflow.spark.load_model(model_uri)

# Generate Scores
df_scored = model.transform(df_features)

# Write to Gold
df_scored.write.format("delta").mode("overwrite").saveAsTable("gold_risk_scores")
