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

# Automatización Kanban (Projects v2)

Este repositorio implementa automatización del tablero Kanban usando el workflow `.github/workflows/kanban-automation.yml` y GitHub Projects v2.

**Reglas de automatización:**
- Al abrir o reabrir un Pull Request -> la tarjeta vinculada se mueve a **Doing**
- Al marcar el Pull Request como **Draft** -> la tarjeta vinculada se mueve a **Backlog**
- Al marcar el Pull Request como **Ready for review** -> la tarjeta vinculada se mueve a **Review**
- Al hacer *merge* del Pull Request -> la tarjeta vinculada se mueve a **Done**

**Funcionamiento:**
- El workflow se activa en eventos relevantes de Pull Request.
- Busca el issue vinculado al PR (por referencia API o por texto en el cuerpo del PR).
- Identifica el item en el proyecto Kanban y actualiza el campo "Status" según la regla correspondiente.
- Si no encuentra un issue vinculado, el workflow termina sin error.

**Requisitos:**
- Tener configurado un Project v2 con columnas: Backlog, Doing, Review, Done.
- Definir el número de proyecto en la variable `PROJECT_NUMBER` en GitHub Actions.
- Proveer el token `GH_TOKEN` con permisos para modificar Projects.

**Notas:**
- Las reglas y nombres de columnas están alineados con la Issue #2 del proyecto.
- Para más detalles, ver el archivo `.github/workflows/kanban-automation.yml`.
