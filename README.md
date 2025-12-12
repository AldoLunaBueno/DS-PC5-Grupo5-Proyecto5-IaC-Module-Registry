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

## Workflows

Pipeline que ejecuta lint y tests en cada push y PR.

### IaC Quality Check
Workflow que verifica la calidad de los módulos de infraestructura como código (Terraform y K8s).

**Trigger:**
- Pull requests a `develop` o `main`
- Push a ramas `feature/**`

**Herramientas instaladas:**
- Terraform (v1.5.0)
- TFLint
- Kubeval
- Conftest

**Proceso:**
1. Instala las herramientas necesarias
2. Ejecuta `tools/run_iac_checks.sh`
3. Genera reporte en `.evidence/iac-quality-report.json`
4. Sube el reporte como artefacto
5. Falla el pipeline si algún módulo tiene estado FAIL

**Estados posibles:**
- `OK`: Todas las verificaciones pasaron
- `WARN`: Hay advertencias pero no errores críticos
- `FAIL`: Errores que deben corregirse

El pipeline falla automáticamente si `summary.fail > 0`.

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

## Flujo de actualización de estados de calidad

A grandes razgos el flujo es así:

1. El workflow ejecuta validaciones y genera `.evidence/iac-quality-report.json`.
2. La API lee el reporte y actualiza el campo `quality_state` de cada módulo.
3. Los endpoints exponen este estado y permiten filtrado por calidad.

El archivo `.evidence/iac-quality-report.json` es generado automáticamente por el workflow [`iac_quality.yml`](.github/workflows/iac_quality.yml) cuando se ejecuta en GitHub Actions. Este archivo contiene el estado de calidad de cada módulo IaC (OK, WARN, FAIL).

La API lee este archivo (si existe) y expone el estado de calidad (`quality_state`) de cada módulo en los endpoints `/modules` y `/modules/{id}`.

- Se puede filtrar por estado de calidad usando:
  - `GET /modules?filter=quality_state:OK|WARN|FAIL`
- Si el archivo no existe, el campo `quality_state` será `UNKNOWN` o el valor presente en el índice.




