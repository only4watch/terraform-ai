output "vpc_name" {
  value = google_compute_network.vpc_network.name
}

output "vm_name" {
  value = google_compute_instance.vm_instance.name
}
