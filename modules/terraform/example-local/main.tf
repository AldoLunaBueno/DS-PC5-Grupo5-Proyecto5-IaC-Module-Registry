terraform {
  required_version = ">= 1.5.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "local_file" "mensaje" {
  content  = var.contenido
  filename = "${path.module}/${var.nombre_archivo}"
}