variable "rg_name" {
  default = "dev-swarm2-weuro"
}

variable "location" {
  default = "West Europe"
}

variable "ssh_master_source_address" {
    default = "89.64.49.27"
}

variable "master_vm_size" {
  default = "Standard_B2ms"
}

variable "worker_vm_size" {
  default = "Standard_B2ms"
}

variable "vm_username" {
  default = "mm"
}

variable "vm_password" {
  default = ""
}

variable "number_of_masters" {
  default = "2"
}

variable "number_of_workers" {
  default = "2"
}

variable "docker_port" {
  default = "2376"
}

