locals {
    config = yamldecode(file("${path.module}/config.yaml"))
}

output "config" {
    value = local.config
}