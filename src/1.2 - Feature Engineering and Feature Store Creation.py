# Databricks notebook source
# MAGIC %md
# MAGIC # Feature engineering and Feature Store creation

# COMMAND ----------

from pyspark.sql.functions import col, when

# COMMAND ----------

# Let's first have a look at the data
churn_dataset = spark.read.table("main.mlops_demo.customer_churn")
display(churn_dataset)

# COMMAND ----------

# NOTE: If you prefer pandas, you can consider the pandas on spark API (former Koalas)!
# Here we keep the "engineering part" to a minimum to focus on the core: The feature store.

def clean_churn_features(df):
    return (
        df
        # Parsing data types (for simplicity we make all numerical)
        .withColumn("total_charges", col("total_charges").cast("double"))
        .withColumn("gender", when(col("gender") == "Female", 1).otherwise(0))
        .withColumn("partner", when(col("partner") == "Yes", 1).otherwise(0))
        .withColumn("dependents", when(col("dependents") == "Yes", 1).otherwise(0))
        .withColumn("phone_service", when(col("phone_service") == "Yes", 1).otherwise(0))
        .withColumn("multiple_lines", when(col("multiple_lines") == "Yes", 1).otherwise(0))
        .withColumn("internet_service", when(col("internet_service") == "No", 0).otherwise(1))
        .withColumn("online_security", when(col("online_security") == "Yes", 1).otherwise(0))
        .withColumn("online_backup", when(col("online_backup") == "Yes", 1).otherwise(0))
        .withColumn("device_protection", when(col("device_protection") == "Yes", 1).otherwise(0))
        .withColumn("tech_support", when(col("tech_support") == "Yes", 1).otherwise(0))
        .withColumn("streaming_tv", when(col("streaming_tv") == "Yes", 1).otherwise(0))
        .withColumn("streaming_movies", when(col("streaming_movies") == "Yes", 1).otherwise(0))
        .withColumn("paperless_billing", when(col("paperless_billing") == "Yes", 1).otherwise(0))
        .withColumn("churn", when(col("churn") == "Yes", 1).otherwise(0))
        # Handling null values
        .fillna({"tenure": 0.0, "monthly_charges": 0.0, "total_charges": 0.0})
    )

# COMMAND ----------

churn_dataset_cleaned = churn_dataset.transform(clean_churn_features)
display(churn_dataset_cleaned)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Export the "cleaned" data to silver

# COMMAND ----------

churn_dataset_cleaned.write.saveAsTable("main.mlops_demo.customer_churn_cleaned")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Add the data to the feature store
# MAGIC Note: the dataset needs to have a UNIQUE ID when working with the feature store!
# MAGIC
# MAGIC In our case this is (should be) the customer_id column.
# MAGIC
# MAGIC The Feature store will be our *uniform entry point* to build ML models (Note: Sharable accross workspaces).
# MAGIC
# MAGIC Added (compared to simple delta table):
# MAGIC
# MAGIC - Discoverability
# MAGIC - Lineage
# MAGIC - Integration with model scoring and serving
# MAGIC - Point-in-time lookups
# MAGIC
# MAGIC Features can be tagged and updated via the simple FeatureEngineeringClient API.

# COMMAND ----------

# First we drop the prediction column!
# This is not known in the feature store!
churn_features = churn_dataset_cleaned.drop("churn")
display(churn_features)

# COMMAND ----------

from databricks.feature_engineering import FeatureEngineeringClient, FeatureLookup
fe = FeatureEngineeringClient()
fe.create_table(
    name="main.mlops_demo.churn_feature_store",
    primary_keys=["customer_id"],
    df=churn_features,
    schema=churn_features.schema,
    description="Churn features")
# Note that you can keep on adding to the feature store using write_table().
