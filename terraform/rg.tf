resource "azurerm_resource_group" "swarm_cluster_rg" {
  name     = "${var.rg_name}"
  location = "${var.location}"
}