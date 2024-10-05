# Databricks notebook source
# MAGIC %md
# MAGIC # Code and feature organization
# MAGIC
# MAGIC An ML model consists of two parts: Code and data.
# MAGIC
# MAGIC In this notebook we will introduce the means to share both accros multiple ML projects.
# MAGIC
# MAGIC Having re-usable components will accelerate ML adoption in your organization by increasing trust and development speed.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Code organization
# MAGIC
# MAGIC Packaging code in a uniform way will make it easier to share and collaborate on the code.
# MAGIC
# MAGIC In this notebook we simply demonstrate the different concepts.
# MAGIC
# MAGIC The actual code is packaged in a "utils" folder.
# MAGIC
# MAGIC Using a "utils folder" is just phase 0 of industrialization (see further in the presentation).

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. The Feature store
# MAGIC
# MAGIC Next to code, features
