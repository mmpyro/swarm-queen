resource "azurerm_availability_set" "master_avaibility_set" {
  count               = "${var.number_of_masters > 1 ? 1 : 0}"
  name                = "master_avaibility_set"
  location            = "${azurerm_resource_group.swarm_cluster_rg.location}"
  resource_group_name = "${azurerm_resource_group.swarm_cluster_rg.name}"
  managed             = true
}

resource "azurerm_network_interface" "master_network_interface" {
  count               = "${var.number_of_masters > 1 ? var.number_of_masters : 0}"
  name                = "master${count.index}"
  location            = "${azurerm_resource_group.swarm_cluster_rg.location}"
  resource_group_name = "${azurerm_resource_group.swarm_cluster_rg.name}"

  ip_configuration {
    name                          = "masterip"
    subnet_id                     = "${azurerm_subnet.internal.id}"
    private_ip_address_allocation = "Dynamic"
    load_balancer_backend_address_pools_ids = ["${azurerm_lb_backend_address_pool.master_lb_backend.id}"]
    load_balancer_inbound_nat_rules_ids = ["${azurerm_lb_nat_rule.ssh_nat_rule.*.id[count.index]}"]
  }
}

resource "azurerm_virtual_machine" "master_vm" {
  count                 = "${var.number_of_masters > 1 ? var.number_of_masters : 0}"
  name                  = "master${count.index}"
  location              = "${azurerm_resource_group.swarm_cluster_rg.location}"
  resource_group_name   = "${azurerm_resource_group.swarm_cluster_rg.name}"
  network_interface_ids = ["${azurerm_network_interface.master_network_interface.*.id[count.index]}"]
  vm_size               = "${var.master_vm_size}"
  availability_set_id   = "${azurerm_availability_set.master_avaibility_set.id}"

  delete_os_disk_on_termination = true
  delete_data_disks_on_termination = true

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
  storage_os_disk {
    name              = "masterdisk${count.index}"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }
  os_profile {
    computer_name  = "master${count.index}"
    admin_username = "${var.vm_username}"
    admin_password = "${var.vm_password}"
  }
  os_profile_linux_config {
    disable_password_authentication = false
  }
}