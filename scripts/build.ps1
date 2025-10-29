# build.ps1 - Script de automação para Windows
# Substituto para Makefile em sistemas Windows

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "Comandos disponíveis:" -ForegroundColor Green
    Write-Host "  install      - Instala o projeto" -ForegroundColor Yellow
    Write-Host "  install-dev  - Instala dependências de desenvolvimento" -ForegroundColor Yellow
    Write-Host "  test         - Executa todos os testes" -ForegroundColor Yellow
    Write-Host "  test-unit    - Executa testes unitários" -ForegroundColor Yellow
    Write-Host "  test-integration - Executa testes de integração" -ForegroundColor Yellow
    Write-Host "  lint         - Verifica qualidade do código" -ForegroundColor Yellow
    Write-Host "  format       - Formata o código" -ForegroundColor Yellow
    Write-Host "  run          - Executa o BLOB" -ForegroundColor Yellow
    Write-Host "  run-dev      - Executa o BLOB em modo desenvolvimento" -ForegroundColor Yellow
    Write-Host "  clean        - Remove arquivos temporários" -ForegroundColor Yellow
    Write-Host "  build        - Constrói o pacote" -ForegroundColor Yellow
}

function Install-Project {
    Write-Host "📦 Instalando projeto..." -ForegroundColor Green
    pip install -r requirements.txt
    pip install -e .
    Write-Host "✅ Instalação concluída!" -ForegroundColor Green
}

function Install-Dev {
    Write-Host "🔧 Instalando dependências de desenvolvimento..." -ForegroundColor Green
    pip install -r requirements.txt
    pip install -e .[dev]
    Write-Host "✅ Instalação de desenvolvimento concluída!" -ForegroundColor Green
}

function Run-Tests {
    Write-Host "🧪 Executando todos os testes..." -ForegroundColor Green
    pytest tests/ -v --cov=src
}

function Run-UnitTests {
    Write-Host "🧪 Executando testes unitários..." -ForegroundColor Green
    pytest tests/unit/ -v
}

function Run-IntegrationTests {
    Write-Host "🧪 Executando testes de integração..." -ForegroundColor Green
    pytest tests/integration/ -v
}

function Run-Lint {
    Write-Host "🔍 Verificando qualidade do código..." -ForegroundColor Green
    flake8 src/ tests/
    Write-Host "✅ Lint completo!" -ForegroundColor Green
}

function Run-Format {
    Write-Host "🎨 Formatando código..." -ForegroundColor Green
    black src/ tests/
    Write-Host "✅ Formatação completa!" -ForegroundColor Green
}

function RunBLOB {
    Write-Host "🚀 Executando BLOB..." -ForegroundColor Green
    python blob.py
}

function RunBLOBDev {
    Write-Host "🔧 Executando BLOB em modo desenvolvimento..." -ForegroundColor Green
    $env:BLOB_ENV = "development"
    python blob.py --dev
}

function Clean-Project {
    Write-Host "🧹 Removendo arquivos temporários..." -ForegroundColor Green
    
    $dirsToClean = @("__pycache__", "src\__pycache__", "src\core\__pycache__", 
                     "src\modules\__pycache__", "tests\__pycache__", ".pytest_cache")
    
    foreach ($dir in $dirsToClean) {
        if (Test-Path $dir) {
            Remove-Item $dir -Recurse -Force
            Write-Host "  Removido: $dir" -ForegroundColor Yellow
        }
    }
    
    if (Test-Path "*.egg-info") {
        Remove-Item "*.egg-info" -Recurse -Force
        Write-Host "  Removido: *.egg-info" -ForegroundColor Yellow
    }
    
    Write-Host "✅ Limpeza concluída!" -ForegroundColor Green
}

function Build-Project {
    Write-Host "🏗️ Construindo pacote..." -ForegroundColor Green
    python setup.py sdist bdist_wheel
    Write-Host "✅ Build concluído!" -ForegroundColor Green
}

# Main switch
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "install" { Install-Project }
    "install-dev" { Install-Dev }
    "test" { Run-Tests }
    "test-unit" { Run-UnitTests }
    "test-integration" { Run-IntegrationTests }
    "lint" { Run-Lint }
    "format" { Run-Format }
    "run" { RunBLOB }
    "run-dev" { RunBLOBDev }
    "clean" { Clean-Project }
    "build" { Build-Project }
    default { 
        Write-Host "❌ Comando desconhecido: $Command" -ForegroundColor Red
        Show-Help 
    }
}