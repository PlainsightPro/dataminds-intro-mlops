# Set up the required providers
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
    databricks = {
      source = "databricks/databricks"
    }
  }
}

provider "azurerm" {
  subscription_id = var.subscription_id
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.prefix}-${var.project_name}"
  location = var.region
}

resource "azurerm_databricks_workspace" "databricks_workspace" {
    name                = "dbx-${var.prefix}-${var.project_name}"
    resource_group_name = azurerm_resource_group.rg.name
    location            = azurerm_resource_group.rg.location
    sku                 = "premium"
    managed_resource_group_name = "mrg-${var.prefix}-${var.project_name}"
}

provider "databricks" {
    host = azurerm_databricks_workspace.databricks_workspace.workspace_url
}

resource "azurerm_databricks_access_connector" "unity_connector" {
    name                = "dbc-${var.prefix}-${var.project_name}"
    resource_group_name = azurerm_resource_group.rg.name
    location            = azurerm_resource_group.rg.location
    identity {
    type = "SystemAssigned"
    }
}

resource "azurerm_storage_account" "storage" {
    name                     = lower("st${var.prefix}${var.project_name}")
    resource_group_name      = azurerm_resource_group.rg.name
    location                 = azurerm_resource_group.rg.location
    account_tier             = "Standard"
    account_replication_type = "LRS"
    is_hns_enabled           = true
}

resource "azurerm_storage_container" "unity_catalog_container" {
    name                  = "unity-catalog"
    storage_account_name  = azurerm_storage_account.storage.name
    container_access_type = "private"
}

resource "azurerm_role_assignment" "storage_access" {
    scope                = azurerm_storage_account.storage.id
    role_definition_name = "Storage Blob Data Contributor"
    principal_id         = azurerm_databricks_access_connector.unity_connector.identity[0].principal_id
}

resource "databricks_metastore" "unity_catalog" {
    name     = "${var.prefix}-${var.project_name}-metastore"
    storage_root = format("abfss://%s@%s.dfs.core.windows.net/",
        azurerm_storage_container.unity_catalog_container.name,
        azurerm_storage_account.storage.name)
    force_destroy = true
    region        = "${var.region}"
}

resource "databricks_metastore_assignment" "catalog_assignment" {
    provider             = databricks
    workspace_id         = azurerm_databricks_workspace.databricks_workspace.workspace_id
    metastore_id         = databricks_metastore.unity_catalog.id
    default_catalog_name = "hive_metastore"
}

resource "databricks_metastore_data_access" "catalog_access" {
    metastore_id = databricks_metastore.unity_catalog.id
    name         = "mi_dac"
    azure_managed_identity {
    access_connector_id = azurerm_databricks_access_connector.unity_connector.id
    }
    is_default = true
    depends_on = [ databricks_metastore_assignment.catalog_assignment ]
}
