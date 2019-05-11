locals {
  is_multi_mater    = "${var.number_of_masters > 1 ? 1 : 0}"
  number_of_masters = "${var.number_of_masters > 1 ? var.number_of_masters : 0}"
  is_single_master  = "${var.number_of_masters == 1 ? 1 : 0}"
}

resource "azurerm_public_ip" "main" {
  name                = "master_ip"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group_name}"
  allocation_method   = "Dynamic"
}