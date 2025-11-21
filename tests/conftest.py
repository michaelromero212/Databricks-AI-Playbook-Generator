import pytest
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

@pytest.fixture
def sample_sql_content():
    return """
    CREATE TABLE silver_users AS
    SELECT 
        u.id, 
        u.name, 
        o.order_date 
    FROM bronze_users u
    JOIN bronze_orders o ON u.id = o.user_id
    WHERE o.order_date > '2023-01-01'
    """

@pytest.fixture
def sample_notebook_content():
    return """
    # COMMAND ----------
    import pyspark.sql.functions as F
    # COMMAND ----------
    df = spark.read.table("silver_users")
    # COMMAND ----------
    df.write.mode("overwrite").saveAsTable("gold_user_stats")
    """
