# Makefile para Projeto BLOB
# ===========================
# 
# Este Makefile automatiza tarefas comuns de desenvolvimento

.PHONY: help install install-dev test test-unit test-integration clean lint format run run-dev docs build

# Variáveis
PYTHON = python
PIP = pip
PYTEST = pytest
BLACK = black
FLAKE8 = flake8

# Ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  install      - Instala o projeto"
	@echo "  install-dev  - Instala dependências de desenvolvimento"
	@echo "  test         - Executa todos os testes"
	@echo "  test-unit    - Executa testes unitários"
	@echo "  test-integration - Executa testes de integração"
	@echo "  lint         - Verifica qualidade do código"
	@echo "  format       - Formata o código"
	@echo "  run          - Executa o BLOB"
	@echo "  run-dev      - Executa o BLOB em modo desenvolvimento"
	@echo "  clean        - Remove arquivos temporários"
	@echo "  docs         - Gera documentação"
	@echo "  build        - Constrói o pacote"

# Instalação
install:
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

install-dev:
	$(PIP) install -r requirements.txt
	$(PIP) install -e .[dev]

# Testes
test:
	$(PYTEST) tests/ -v --cov=src

test-unit:
	$(PYTEST) tests/unit/ -v

test-integration:
	$(PYTEST) tests/integration/ -v

# Qualidade de código
lint:
	$(FLAKE8) src/ tests/
	@echo "Lint completo!"

format:
	$(BLACK) src/ tests/
	@echo "Formatação completa!"

# Execução
run:
	$(PYTHON) src/core/blob_ultra_avancado.py

run-dev:
	set BLOB_ENV=development && $(PYTHON) src/core/blob_ultra_avancado.py

# Limpeza
clean:
	@echo "Removendo arquivos temporários..."
	@if exist "__pycache__" rmdir /s /q "__pycache__"
	@if exist "src\__pycache__" rmdir /s /q "src\__pycache__"
	@if exist "src\core\__pycache__" rmdir /s /q "src\core\__pycache__"
	@if exist "src\modules\__pycache__" rmdir /s /q "src\modules\__pycache__"
	@if exist "tests\__pycache__" rmdir /s /q "tests\__pycache__"
	@if exist ".pytest_cache" rmdir /s /q ".pytest_cache"
	@if exist "*.egg-info" rmdir /s /q "*.egg-info"
	@echo "Limpeza concluída!"

# Documentação
docs:
	@echo "Gerando documentação..."
	# Adicionar geração de docs aqui

# Build
build:
	$(PYTHON) setup.py sdist bdist_wheel
	@echo "Build concluído!"

# Verificação rápida
check: lint test
	@echo "Verificação completa aprovada!"