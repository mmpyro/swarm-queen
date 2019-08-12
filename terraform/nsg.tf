resource "azurerm_network_security_group" "swarm_nsg" {
  name                = "swarm_nsg"
  location            = "${azurerm_resource_group.swarm_cluster_rg.location}"
  resource_group_name = "${azurerm_resource_group.swarm_cluster_rg.name}"

}

resource "azurerm_network_security_rule" "signle_master_nsg_rules_ssh" {
  count                       = "${var.number_of_masters == 1 ? 1 : 0}"
  name                        = "single_master_SSH"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = "${var.ssh_allowed_source_address}"
  destination_address_prefix  = "*"
  resource_group_name         = "${azurerm_resource_group.swarm_cluster_rg.name}"
  network_security_group_name = "${azurerm_network_security_group.swarm_nsg.name}"
}

resource "azurerm_network_security_rule" "nodes_nsg_rules_ssh" {
  name                        = "nodes_SSH"
  priority                    = 101
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "50000-50200"
  source_address_prefix       = "${var.ssh_allowed_source_address}"
  destination_address_prefix  = "*"
  resource_group_name         = "${azurerm_resource_group.swarm_cluster_rg.name}"
  network_security_group_name = "${azurerm_network_security_group.swarm_nsg.name}"
}

resource "azurerm_network_security_rule" "master_nsg_rules_dockerAPI" {
  name                        = "DockerAPI"
  priority                    = 102
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "2376"
  source_address_prefix       = "${var.ssh_allowed_source_address}"
  destination_address_prefix  = "*"
  resource_group_name         = "${azurerm_resource_group.swarm_cluster_rg.name}"
  network_security_group_name = "${azurerm_network_security_group.swarm_nsg.name}"
}