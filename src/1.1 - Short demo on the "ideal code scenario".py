# Databricks notebook source
# MAGIC %md
# MAGIC # Demo on good coding practices
# MAGIC This is not functional code. This is a high level demo.
# MAGIC
# MAGIC Note that your code gets easier to **share**, test and debug!
# MAGIC
# MAGIC > Additional note: I can work on the ChurnModel without changing a line of code in the app!

# COMMAND ----------

# MAGIC %md
# MAGIC ## A training pipeline

# COMMAND ----------

from utils.datalake import DataLake
from utils.features import FeatureHandler
from utils.mlmodels import MyChurnModel

def main():
    churn_data = DataLake().get_dataset("churn")
    FeatureHandler(churn_data).create_features()
    churn_model = MyChurnModel().get_model()
    churn_model.train(churn_data)
    return churn_model


# COMMAND ----------

# MAGIC %md
# MAGIC ## A predict pipeline

# COMMAND ----------

from utils.datalake import DataLake
from utils.features import FeatureHandler
from utils.mlmodels import MyChurnModel

def main():
    churn_data = DataLake().get_dataset("churn")
    FeatureHandler(churn_data).create_features()
    churn_model = MyChurnModel().get_model()
    churn_model.predict(churn_data)
    return churn_model

