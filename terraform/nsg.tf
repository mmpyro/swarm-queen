resource "azurerm_network_security_group" "master_nsg" {
  name                = "master_nsg"
  location            = "${azurerm_resource_group.swarm_cluster_rg.location}"
  resource_group_name = "${azurerm_resource_group.swarm_cluster_rg.name}"

}

resource "azurerm_network_security_rule" "master_nsg_rules_ssh" {
  name                        = "SSH"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = "${var.ssh_master_source_address}"
  destination_address_prefix  = "*"
  resource_group_name         = "${azurerm_resource_group.swarm_cluster_rg.name}"
  network_security_group_name = "${azurerm_network_security_group.master_nsg.name}"
}

resource "azurerm_network_security_rule" "master_nsg_rules_dockerAPI" {
  name                        = "DockerAPI"
  priority                    = 101
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "2376"
  source_address_prefix       = "${var.ssh_master_source_address}"
  destination_address_prefix  = "*"
  resource_group_name         = "${azurerm_resource_group.swarm_cluster_rg.name}"
  network_security_group_name = "${azurerm_network_security_group.master_nsg.name}"
}