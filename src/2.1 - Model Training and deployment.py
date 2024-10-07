# Databricks notebook source
# MAGIC %md
# MAGIC # Model training and deployment

# COMMAND ----------

# MAGIC %md
# MAGIC ## Generate train-test data split
# MAGIC We will fetch our data from the Feature store to re-use.

# COMMAND ----------

from databricks.feature_engineering import FeatureEngineeringClient, FeatureLookup
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score

# COMMAND ----------

features_table = fe.read_table(
  name='main.mlops_demo.churn_feature_store',
)

# COMMAND ----------

# Step 1: We make a lookup table (for the features) and link this to our feature store
prediction_lookup = (
    spark.read.table("main.mlops_demo.customer_churn_cleaned")
    .select("customer_id", "churn")
).collect() # Collect needed, otherwise you get recursion errors (as the feature store points to the same table)
model_feature_lookups = [
    FeatureLookup(
        table_name = "main.mlops_demo.churn_feature_store",
        lookup_key='customer_id' # Key used to match in the lookup table
    )
]
# Step 2: Now we are ready to use the feature store to merge features and labels
fe = FeatureEngineeringClient()
churn_dataset = spark.read.table("main.mlops_demo.customer_churn_cleaned").select("customer_id", "churn")
training_set = fe.create_training_set(
  df=churn_dataset,
  feature_lookups=model_feature_lookups,
  features=["monthly_charges", "total_charges"],
  label='churn',
  exclude_columns='customer_id'
)
# Step 3: We make the train-test split via pandas
training_pd = training_set.load_df().toPandas()
X = training_pd[["monthly_charges", "total_charges"]]
y = training_pd["churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# COMMAND ----------

X_train.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ## MLflow
# MAGIC Here we point MLFlow to the unity catalog in stead of the workspace. This will make the workspace less messy.

# COMMAND ----------

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

def train_model(X_train, X_test, y_train, y_test, training_set, fe):
    ## fit and log model
    with mlflow.start_run() as run:

        rf = RandomForestClassifier(max_depth=2, n_estimators=20, random_state=42)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)

        mlflow.log_metric("test_f1_score", f1_score(y_test, y_pred))
        mlflow.log_metric("test_roc_auc", roc_auc_score(y_test, y_pred))

        fe.log_model(
            model=rf,
            artifact_path="chrun_prediction",
            flavor=mlflow.sklearn,
            training_set=training_set,
            registered_model_name=model_name,
        )

train_model(X_train, X_test, y_train, y_test, training_set, fe)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Houston, we have a model!
# MAGIC Note that we used the test set in the model logging.
