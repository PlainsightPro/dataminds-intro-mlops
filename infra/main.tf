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
    subscription_id = "${var.subscription_id}"
    features {}
}

resource "azurerm_resource_group" "rgname" {
    name = "rg-${var.project_name}"
    location  = "${var.region}"
}

# resource "azurerm_databricks_workspace" "example" {
#     name                = "databricks-test"
#     resource_group_name = azurerm_resource_group.rgname.name
#     location            = azurerm_resource_group.rgname.location
#     sku                 = "premium"
# }
    
# provider "databricks" {
#     host = azurerm_databricks_workspace.example.workspace_url
# }

# resource "azurerm_databricks_access_connector" "unity" {
#     name                = "venkatdatabricksmi1"
#     resource_group_name = azurerm_resource_group.rgname.name
#     location            = azurerm_resource_group.rgname.location
#     identity {
#     type = "SystemAssigned"
#     }
# }

# resource "azurerm_storage_account" "unity_catalog" {
#     name                     = "thejadatabricksdemo2"
#     resource_group_name      = azurerm_resource_group.rgname.name
#     location                 = azurerm_resource_group.rgname.location
#     account_tier             = "Standard"
#     account_replication_type = "GRS"
#     is_hns_enabled           = true
# }

# resource "azurerm_storage_container" "unity_catalog" {
#     name                  = "venkat-container2"
#     storage_account_name  = azurerm_storage_account.unity_catalog.name
#     container_access_type = "private"
# }

# resource "azurerm_role_assignment" "example" {
#     scope                = azurerm_storage_account.unity_catalog.id
#     role_definition_name = "Storage Blob Data Contributor"
#     principal_id         = azurerm_databricks_access_connector.unity.identity[0].principal_id
# }

# resource "databricks_metastore" "this" {
#     name     = "demometastoretest"
#     storage_root = format("abfss://%s@%s.dfs.core.windows.net/",
#     azurerm_storage_container.unity_catalog.name,
#     azurerm_storage_account.unity_catalog.name)
#     force_destroy = true
#     region        = "centralus"
# }

# resource "databricks_metastore_assignment" "this" {
#     provider             = databricks
#     workspace_id         = azurerm_databricks_workspace.example.workspace_id
#     metastore_id         = databricks_metastore.this.id
#     default_catalog_name = "hive_metastore"
# }

# resource "databricks_metastore_data_access" "this" {
#     metastore_id = databricks_metastore.this.id
#     name         = "mi_dac"
#     azure_managed_identity {
#     access_connector_id = azurerm_databricks_access_connector.unity.id
#     }
#     is_default = true
#     depends_on = [ databricks_metastore_assignment.this ]
# }