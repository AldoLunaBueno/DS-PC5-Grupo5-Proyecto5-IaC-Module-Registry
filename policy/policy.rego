package main

# Validar convención de nombres de módulos
deny[msg] {
    input.kind == "metadata"
    name := input.name
    not regex.match("^[a-z][a-z0-9-]*$", name)
    msg := sprintf("Nombre de módulo inválido '%s': debe usar minúsculas, números y guiones", [name])
}

# Verificar existencia de campos obligatorios en metadata.yaml
deny[msg] {
    input.kind == "metadata"
    not input.name
    msg := "metadata.yaml debe contener el campo 'name'"
}

deny[msg] {
    input.kind == "metadata"
    not input.version
    msg := "metadata.yaml debe contener el campo 'version'"
}

deny[msg] {
    input.kind == "metadata"
    not input.maintainer
    msg := "metadata.yaml debe contener el campo 'maintainer'"
}

deny[msg] {
    input.kind == "metadata"
    not input.tags
    msg := "metadata.yaml debe contener el campo 'tags'"
}

# Verificar labels mínimos en recursos K8s
deny[msg] {
    input.kind == "Deployment"
    not input.metadata.labels.app
    msg := "Deployment debe tener label 'app' en metadata"
}

deny[msg] {
    input.kind == "Service"
    not input.spec.selector.app
    msg := "Service debe tener selector 'app'"
}
