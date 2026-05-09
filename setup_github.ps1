# ============================================================
# setup_github.ps1
# Script de despliegue del proyecto a C:\Github
# Ejecutar desde PowerShell como administrador si es necesario
# ============================================================

$PROJECT_NAME = "laboratorio_drybean_ml"
$GITHUB_DIR   = "C:\Github"
$TARGET       = "$GITHUB_DIR\$PROJECT_NAME"
$SCRIPT_DIR   = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Despliegue: $PROJECT_NAME → C:\Github" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Crear C:\Github si no existe
if (-not (Test-Path $GITHUB_DIR)) {
    New-Item -ItemType Directory -Path $GITHUB_DIR | Out-Null
    Write-Host "✅ Creada carpeta: $GITHUB_DIR" -ForegroundColor Green
}

# 2. Copiar el proyecto completo
Write-Host "`n📁 Copiando proyecto a $TARGET ..."
Copy-Item -Path $SCRIPT_DIR -Destination $TARGET -Recurse -Force
Write-Host "✅ Proyecto copiado" -ForegroundColor Green

# 3. Entrar al directorio del proyecto
Set-Location $TARGET

# 4. Inicializar Git
Write-Host "`n🔧 Inicializando repositorio git..."
git init
git add .
git commit -m "feat: proyecto inicial — CRISP-DM + TDSP + Scrum ML — Dry Bean Dataset"
Write-Host "✅ Commit inicial creado" -ForegroundColor Green

# 5. Crear entorno virtual Python
Write-Host "`n🐍 Creando entorno virtual Python..."
python -m venv .venv
Write-Host "✅ Entorno virtual creado en .venv\" -ForegroundColor Green

# 6. Activar e instalar dependencias
Write-Host "`n📦 Instalando dependencias..."
& ".venv\Scripts\pip.exe" install -r requirements.txt
Write-Host "✅ Dependencias instaladas" -ForegroundColor Green

# 7. Instrucciones finales
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  ✅ PROYECTO LISTO EN: $TARGET" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Activar entorno virtual:"
Write-Host "     .venv\Scripts\Activate.ps1"
Write-Host ""
Write-Host "  2. Agregar remote GitHub:"
Write-Host "     git remote add origin https://github.com/TU_USUARIO/laboratorio_drybean_ml.git"
Write-Host "     git push -u origin main"
Write-Host ""
Write-Host "  3. Abrir el notebook:"
Write-Host "     jupyter notebook notebooks\01_laboratorio_drybean.ipynb"
Write-Host ""
Write-Host "  4. O ejecutar el script directamente:"
Write-Host "     python src\laboratorio_drybean.py"
Write-Host ""
