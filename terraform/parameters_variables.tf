variable "rg_name" {
  default = "dev-swarm2-weuro"
}

variable "location" {
  default = "West Europe"
}

variable "ssh_allowed_source_address" {
    default = "89.64.49.27"
}

variable "master_vm_size" {
  default = "Standard_B1ms"
}

variable "worker_vm_size" {
  default = "Standard_B1ms"
}

variable "vm_username" {
  default = "mm"
}

variable "number_of_masters" {
  default = "1"
}

variable "number_of_workers" {
  default = "2"
}

variable "docker_port" {
  default = "2376"
}

variable "key_name" {
  default = "swarm.pub"
}

variable "key_path" {
  default = ""
}

variable "node_exporter" {
  default = ""
}