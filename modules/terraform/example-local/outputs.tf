output "archivo_generado" {
  description = "Ruta completa del archivo creado"
  value       = local_file.mensaje.filename
}