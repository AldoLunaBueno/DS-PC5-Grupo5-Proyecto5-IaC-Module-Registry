# DS-PC5-Grupo5-Proyecto5-IaC-Module-Registry
Proyecto 5. IaC Module Registry: catálogo seguro de módulos Terraform/K8s

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
