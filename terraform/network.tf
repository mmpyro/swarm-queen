resource "azurerm_virtual_network" "main" {
  name                = "swarm-network"
  address_space       = ["10.0.0.0/16"]
  location            = "${azurerm_resource_group.swarm_cluster_rg.location}"
  resource_group_name = "${azurerm_resource_group.swarm_cluster_rg.name}"
}

resource "azurerm_subnet" "internal" {
  name                 = "internal"
  resource_group_name  = "${azurerm_resource_group.swarm_cluster_rg.name}"
  virtual_network_name = "${azurerm_virtual_network.main.name}"
  address_prefix       = "10.0.2.0/24"
  network_security_group_id = "${azurerm_network_security_group.swarm_nsg.id}"
}