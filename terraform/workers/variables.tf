variable "resource_group_name" {
  default = ""
}

variable "location" {
  default = ""
}

variable "os_name" {
  default = "UbuntuServer"
}

variable "os_version" {
  default = "18.04-LTS"
}

variable "vm_username" {
  default = ""
}

variable "vm_password" {
  default = ""
}

variable "azurerm_subnet_id" {
  default = ""
}

variable "number_of_workers" {
  default = "3"
}

variable "worker_vm_size" {
  default = "Standard_B2ms"
}

variable "worker_vm_tier" {
  default = "Standard"
}
