variable "resource_group_name" {
  default = ""
}

variable "location" {
  default = ""
}

variable "azurerm_subnet_id" {
  default = ""
}

variable "master_vm_size" {
  default  = "Standard_B2ms"
}

variable "vm_username" {
  default = ""
}

variable "vm_password" {
  default = ""
}

variable "docker_port" {
  default = "2376"
}

variable "number_of_masters" {
  default = "1"
}

variable "os_name" {
  default = "UbuntuServer"
}

variable "os_version" {
  default = "18.04-LTS"
}
