provider "azurerm" {
  version = "=1.22.0"
  subscription_id = "${var.subscription_id}"
  client_id       = "${var.client_id}"
  client_secret   = "${var.client_secret}"
  tenant_id       = "${var.tenant_id}"
}

module "masters" {
  source = "./masters"
  
  resource_group_name = "${azurerm_resource_group.swarm_cluster_rg.name}"
  location            = "${azurerm_resource_group.swarm_cluster_rg.location}"
  azurerm_subnet_id   = "${azurerm_subnet.internal.id}"
  vm_username         = "${var.vm_username}"
  vm_password         = "${var.vm_password}"
  number_of_masters   = "${var.number_of_masters}"
}

module "workers" {
  source = "./workers"
  
  resource_group_name = "${azurerm_resource_group.swarm_cluster_rg.name}"
  location            = "${azurerm_resource_group.swarm_cluster_rg.location}"
  azurerm_subnet_id   = "${azurerm_subnet.internal.id}"
  vm_username         = "${var.vm_username}"
  vm_password         = "${var.vm_password}"
  number_of_workers   = "${var.number_of_workers}"
}


variable "subscription_id" {}

variable "client_id" {}

variable "client_secret" {}

variable "tenant_id" {}