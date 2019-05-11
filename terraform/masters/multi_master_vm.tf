resource "azurerm_availability_set" "master_avaibility_set" {
  count               = "${local.is_multi_mater}"
  name                = "master_avaibility_set"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group_name}"
  managed             = true
}

resource "azurerm_network_interface" "master_network_interface" {
  count               = "${local.number_of_masters}"
  name                = "master${count.index}"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group_name}"

  ip_configuration {
    name                          = "masterip"
    subnet_id                     = "${var.azurerm_subnet_id}"
    private_ip_address_allocation = "Dynamic"
    load_balancer_backend_address_pools_ids = ["${azurerm_lb_backend_address_pool.master_lb_backend.id}"]
    load_balancer_inbound_nat_rules_ids = ["${azurerm_lb_nat_rule.ssh_nat_rule.*.id[count.index]}"]
  }
}

resource "azurerm_virtual_machine" "master_vm" {
  count                 = "${local.number_of_masters}"
  name                  = "master${count.index}"
  location              = "${var.location}"
  resource_group_name   = "${var.resource_group_name}"
  network_interface_ids = ["${azurerm_network_interface.master_network_interface.*.id[count.index]}"]
  vm_size               = "${var.master_vm_size}"
  availability_set_id   = "${azurerm_availability_set.master_avaibility_set.id}"

  delete_os_disk_on_termination = true
  delete_data_disks_on_termination = true

  storage_image_reference {
    publisher = "Canonical"
    offer     = "${var.os_name}"
    sku       = "${var.os_version}"
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
  }

  os_profile_linux_config {
    disable_password_authentication = true

    ssh_keys {
      path     = "/home/${var.vm_username}/.ssh/authorized_keys"
      key_data = "${file("${var.key_path}/${var.key_name}")}"
    }
  }
}