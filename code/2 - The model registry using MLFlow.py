# Databricks notebook source
# MAGIC %md
# MAGIC # The model registry using MLFlow

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Introducing MLFlow
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Applying MLFlow in your ML pipelines

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Adding models to your MLFlow registry

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Fetching models from the registry for prediction
# MAGIC
# MAGIC The model is registered in different ways!
# MAGIC
# MAGIC If we go to the Experiments and Models tab we can actually see this!
# MAGIC
# MAGIC It's both as a python pickle file as well as a docker container.
# MAGIC
# MAGIC The big advantage of the latter is uniform deployment!
# MAGIC
# MAGIC Different strategies:
# MAGIC
# MAGIC - As code
# MAGIC - Via a serving endpoint
# MAGIC
# MAGIC The choice depends on how you want to integrate the model!
