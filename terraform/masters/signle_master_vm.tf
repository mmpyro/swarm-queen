resource "azurerm_network_interface" "single_master_network_interface" {
  count               = "${local.is_single_master}"
  name                = "master${count.index}"
  location            = "${var.location}"
  resource_group_name = "${var.resource_group_name}"

  ip_configuration {
    name                          = "masterip"
    subnet_id                     = "${var.azurerm_subnet_id}"
    public_ip_address_id          = "${azurerm_public_ip.main.id}"
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_virtual_machine" "signle_master_vm" {
  count                 = "${local.is_single_master}"
  name                  = "master${count.index}"
  location              = "${var.location}"
  resource_group_name   = "${var.resource_group_name}"
  network_interface_ids = ["${azurerm_network_interface.single_master_network_interface.id}"]
  vm_size               = "${var.master_vm_size}"

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
    admin_password = "${var.vm_password}"
  }
  os_profile_linux_config {
    disable_password_authentication = false
  }
}