param([string]$Mode = "normal")

Write-Host "BLOB Sistema de Execucao" -ForegroundColor Green

if ($Mode -eq "help") {
    Write-Host "Uso: .\run.ps1 [modo]"
    Write-Host "Modos: normal, dev, test, clean"
} elseif ($Mode -eq "dev") {
    Write-Host "Modo desenvolvimento..."
    $env:BLOB_ENV = "development"
    python blob.py --dev
} elseif ($Mode -eq "test") {
    Write-Host "Executando testes..."
    python -m pytest tests/ -v
} elseif ($Mode -eq "clean") {
    Write-Host "Limpando..."
    if (Test-Path "__pycache__") { Remove-Item "__pycache__" -Recurse -Force }
    Write-Host "Limpeza concluida!"
} else {
    Write-Host "Executando BLOB..."
    python blob.py
}