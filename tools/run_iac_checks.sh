#!/bin/bash
set -euo pipefail

EVIDENCE_DIR=".evidence/iac-checks"
TERRAFORM_DIR="modules/terraform"
K8S_DIR="modules/k8s"

mkdir -p "$EVIDENCE_DIR"

echo "Iniciando validaciones IaC"

# --- TERRAFORM ---
if command -v terraform &> /dev/null; then
    echo "- Verificando Terraform..."
    shopt -s nullglob
    for dir in "$TERRAFORM_DIR"/*/; do
        if [ -d "$dir" ]; then
            dirname=$(basename "$dir")
            echo "  -> Módulo: $dirname"
            
            terraform -chdir="$dir" init -backend=false > /dev/null 2>&1 || { 
                echo " [ERROR] Falló 'terraform init' en $dirname"; 
                exit 1; 
            }
            terraform -chdir="$dir" fmt -check > "$EVIDENCE_DIR/tf-fmt-$dirname.txt" 2>&1 || { 
                echo " [ERROR] Falló 'terraform fmt' en $dirname"; 
                exit 1; 
            }
            terraform -chdir="$dir" validate > "$EVIDENCE_DIR/tf-validate-$dirname.txt" 2>&1 || { 
                echo " [ERROR] Falló 'terraform validate' en $dirname"; 
                exit 1; 
            }
        fi
    done
    shopt -u nullglob
else
    echo " [ERROR] Terraform no encontrado. Saltando validaciones."
    exit 1;
fi

# TFLint
if command -v tflint &> /dev/null; then
    echo "- Ejecutando TFLint..."
    tflint --init > /dev/null 2>&1
    tflint --recursive > "$EVIDENCE_DIR/tflint-report.txt" 2>&1
else
    echo "TFLint no encontrado. Saltando."
    exit 1;
fi

# --- KUBERNETES ---
if command -v kubeval &> /dev/null; then
    echo "- Verificando K8s con Kubeval..."
    shopt -s nullglob
    for dir in "$K8S_DIR"/*; do
        if [ -d "$dir" ]; then
            dirname=$(basename "$dir")
            echo "  -> Módulo: $dirname"
            kubeval "$dir"/deployment.yaml "$dir"/service.yaml > "$EVIDENCE_DIR/k8s-kubeval-$dirname.txt" 2>&1 || { 
                echo " [ERROR] Falló 'kubeval' en $dirname"; 
                exit 1; 
            }
        fi
    done
    shopt -u nullglob
else
    echo "Kubeval no encontrado. Saltando."
    exit 1;
fi

# conftest
if command -v conftest &> /dev/null; then
    echo "- Ejecutando Conftest..."
    
    # Validar metadata.yaml de módulos terraform
    for dir in "$TERRAFORM_DIR"/*/; do
        if [ -d "$dir" ] && [ -f "$dir/metadata.yaml" ]; then
            dirname=$(basename "$dir")
            echo " Validando metadata: $dirname"
            conftest test "$dir/metadata.yaml" -p policy/ >> .evidence/conftest-report.txt 2>&1 || true
        fi
    done
    
    # Validar metadata.yaml de módulos k8s
    for dir in "$K8S_DIR"/*; do
        if [ -d "$dir" ] && [ -f "$dir/metadata.yaml" ]; then
            dirname=$(basename "$dir")
            echo "  Validando metadata: $dirname"
            conftest test "$dir/metadata.yaml" -p policy/ >> .evidence/conftest-report.txt 2>&1 || true
        fi
    done
    
    # Validar archivos K8s
    for dir in "$K8S_DIR"/*; do
        if [ -d "$dir" ]; then
            dirname=$(basename "$dir")
            echo "  Validando K8s: $dirname"
            conftest test "$dir"/*.yaml -p policy/ >> .evidence/conftest-report.txt 2>&1 || true
        fi
    done
else
    echo "Conftest no encontrado. Saltando."
fi

echo "Validaciones completadas"
echo "Reportes generados en $EVIDENCE_DIR"