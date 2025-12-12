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

### Deploy + Smoke Tests
Workflow que despliega la aplicación y ejecuta smoke tests.

**Trigger:**
- `workflow_dispatch` (manual)
- Push a `main`

**Dependencia:**
- Verifica calidad IaC como prerequisito (ejecuta `tools/run_iac_checks.sh`)
- Si hay fallos en IaC, el deploy se cancela

**Proceso:**
1. Verifica calidad IaC: ejecuta `tools/run_iac_checks.sh`
2. Levanta servicios con `docker-compose up -d`
3. Ejecuta smoke tests:
   - `curl /health` - Verifica que la API está activa
   - `curl /modules` - Verifica que se pueden obtener módulos
4. Genera `modules-summary.json` con timestamp y estado actual de módulos
5. Guarda evidencias en `.evidence/deploy-log.txt` y `.evidence/modules-summary.json`

**Uso:**
```bash
# Trigger manual desde GitHub Actions
# O automático en push a main
```

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
