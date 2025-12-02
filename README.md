# DS-PC5-Grupo5-Proyecto5-IaC-Module-Registry

## Convención de Ramas

Formato: `<tipo>/<descripcion-corta>`

**feature/** - Nuevas funcionalidades  
**chore/** - Mantenimiento y configuración  
**hotfix/** - Correcciones urgentes

Ejemplos:
```bash
feature/api-module-search
chore/setup-ci-pipeline
hotfix/api-500-error
```

## Pull Requests

Formato del template: **Que**, **Por que**, **Como**  
Al final incluir: `Closes #X`

Requisitos:
- CI pass (tests, linting, validación IaC)
- 1 aprobación de code owner
- Convención de ramas respetada

Code Owners: @AldoLunaBueno, @Jharvichu, @AlbeCamp21

## Protección de main

Ver configuración completa en `.evidence/branch-protection.txt`

- Requiere PR con 1 aprobación
- Requiere CI pass
- No force push ni delete
