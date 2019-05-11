output "worker_ip" {
  value = "${azurerm_public_ip.worker_ip.ip_address}"
}