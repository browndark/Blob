# 📜 Scripts Directory

Este diretório contém scripts de automação e build do projeto BLOB.

## 📋 Scripts Disponíveis

### `build.ps1`
Script de build principal do projeto:
- Verifica dependências
- Executa testes
- Prepara ambiente de produção

### `run.ps1`
Script de execução rápida:
- Inicia o BLOB em modo desenvolvimento
- Aplica configurações padrão
- Monitora logs

## 🚀 Uso

Execute diretamente do PowerShell:

```powershell
# Build completo
./scripts/build.ps1

# Execução rápida
./scripts/run.ps1
```

## 🔧 Personalização

Os scripts podem ser modificados para incluir:
- Diferentes configurações de ambiente
- Parâmetros de inicialização customizados
- Hooks de pré/pós execução

## 📝 Logs

Todos os scripts geram logs em:
- `logs/build.log` (para build.ps1)
- `logs/run.log` (para run.ps1)