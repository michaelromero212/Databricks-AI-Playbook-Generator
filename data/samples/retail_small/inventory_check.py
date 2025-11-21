# COMMAND ----------
# Inventory Data Validation

import pyspark.sql.functions as F

# COMMAND ----------

df_inventory = spark.read.table("silver_inventory")

# Check for negative stock
negative_stock = df_inventory.filter(F.col("quantity_on_hand") < 0)

if negative_stock.count() > 0:
    print("WARNING: Negative stock detected!")
    negative_stock.show()
else:
    print("Inventory levels look good.")
