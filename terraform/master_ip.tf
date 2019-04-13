resource "azurerm_public_ip" "main" {
  name                = "master-ip"
  location            = "${var.location}"
  resource_group_name = "${azurerm_resource_group.swarm_cluster_rg.name}"
  allocation_method   = "Dynamic"
}