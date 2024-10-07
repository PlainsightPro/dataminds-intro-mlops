# Databricks notebook source
# MAGIC %md
# MAGIC # Demo setup
# MAGIC
# MAGIC In order to guarantee a similar setup we provide the "Demo setup" notebook.
# MAGIC
# MAGIC You can just run this notebook entirely.

# COMMAND ----------

# MAGIC %md
# MAGIC ## General configs

# COMMAND ----------

#Let's skip some warnings for cleaner output
import warnings
warnings.filterwarnings("ignore")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Unity Catalog setup
# MAGIC
# MAGIC We will use the 'main' catalog.

# COMMAND ----------

catalog = "main"
schema = dbName = db = "mlops_demo"

# COMMAND ----------

spark.sql(f"DROP SCHEMA IF EXISTS {catalog}.{schema} CASCADE")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data setup
# MAGIC We will download the data directly from the IBM site and place erveryting in our catalog.

# COMMAND ----------

import pandas as pd
import re
import requests
from io import StringIO

# COMMAND ----------

bronze_table_name = "customer_churn"
dataset_location = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
data_csv = requests.get(dataset_location).text
df = pd.read_csv(StringIO(data_csv), sep=",")
def cleanup_column_names(pdf):
    # Clean up column names
    pdf.columns = [re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower().replace("__", "_") for name in pdf.columns]
    pdf.columns = [re.sub(r'[\(\)]', '', name).lower() for name in pdf.columns]
    pdf.columns = [re.sub(r'[ -]', '_', name).lower() for name in pdf.columns]
    return pdf.rename(columns = {'streaming_t_v': 'streaming_tv', 'customer_i_d': 'customer_id'})
df = cleanup_column_names(df)
spark_df = spark.createDataFrame(df)
(
    spark_df.write
            .mode("overwrite")
            .option("overwriteSchema", "true")
            .saveAsTable(f"{catalog}.{schema}.{bronze_table_name}")
)
