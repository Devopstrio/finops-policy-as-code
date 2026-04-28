provider "azurerm" {
  features {}
}

# --- FinOps Policy Foundation (Institutional Hub) ---

resource "azurerm_resource_group" "fpac" {
  name     = "rg-${var.project_name}-foundation-${var.environment}"
  location = var.location
}

# --- Compliance Metadata Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "fpac" {
  name                   = "psql-${var.project_name}-governance-${var.environment}"
  resource_group_name    = azurerm_resource_group.fpac.name
  location               = azurerm_resource_group.fpac.location
  version                = "13"
  administrator_login    = "fpacadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Shared Governance Hub Network ---

resource "azurerm_virtual_network" "hub" {
  name                = "vnet-${var.project_name}-governance-hub-${var.environment}"
  location            = azurerm_resource_group.fpac.location
  resource_group_name = azurerm_resource_group.fpac.name
  address_space       = ["10.0.0.0/16"]

  tags = {
    Environment = var.environment
    CostCenter  = "Core-Governance"
  }
}

# --- Policy Execution Plane (AKS) ---

resource "azurerm_kubernetes_cluster" "fpac_k8s" {
  name                = "aks-${var.project_name}-policy-engine-${var.environment}"
  location            = azurerm_resource_group.fpac.location
  resource_group_name = azurerm_resource_group.fpac.name
  dns_prefix          = "fpac-engine"

  default_node_pool {
    name       = "fpacpool"
    node_count = 3
    vm_size    = "Standard_D4s_v3"
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }
}

# --- Secrets & Remediator Identity (Key Vault) ---

resource "azurerm_key_vault" "fpac" {
  name                        = "kv-fpac-maestro-${var.environment}"
  location                    = azurerm_resource_group.fpac.location
  resource_group_name         = azurerm_resource_group.fpac.name
  enabled_for_disk_encryption = true
  tenant_id                   = var.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = true

  sku_name = "standard"
}
