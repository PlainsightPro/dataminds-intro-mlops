# Databricks notebook source
# MAGIC %md
# MAGIC ## Let's create an incoming datapoint

# COMMAND ----------

# Here we re-use our cleaned data
# In reality this will be data coming in from a data pipeline
input_data = spark.read.table("main.mlops_demo.customer_churn_cleaned").select('customer_id').limit(10)
display(input_data)

# COMMAND ----------

# MAGIC %md
# MAGIC ## We load the model to make the prediction

# COMMAND ----------

# We have the mandatory package imports
import mlflow
from mlflow import MlflowClient
import logging
logging.getLogger("mlflow").setLevel(logging.ERROR)
# Set UC Model Registry as default
mlflow.set_registry_uri("databricks-uc")
client = MlflowClient()
# Name your UC model
model_name = "main.mlops_demo.churn_model"
client = MlflowClient()

# COMMAND ----------

# Must be run on a cluster running Databricks Runtime for Machine Learning.
from databricks.feature_store import FeatureStoreClient

fs = FeatureStoreClient()
logged_model = f'models:/{model_name}/3'

# This model was packaged by Feature Store.
# To retrieve features prior to scoring, call FeatureStoreClient.score_batch.
fs.score_batch(logged_model, input_data)
