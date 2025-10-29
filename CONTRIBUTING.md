# 🤝 Contribuindo para o BLOB

Obrigado por seu interesse em contribuir com o projeto BLOB! Este documento fornece diretrizes para contribuições efetivas.

## 📋 Como Contribuir

### 1. Preparação do Ambiente

```bash
# Fork e clone o repositório
git clone https://github.com/SEU_USUARIO/blob-assistant.git
cd blob-assistant

# Crie um ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instale dependências de desenvolvimento
make install-dev
```

### 2. Fluxo de Desenvolvimento

1. **Crie uma branch** para sua feature/bugfix:
   ```bash
   git checkout -b feature/nova-funcionalidade
   # ou
   git checkout -b bugfix/correcao-importante
   ```

2. **Desenvolva** seguindo os padrões do projeto
3. **Teste** suas alterações:
   ```bash
   make test
   make lint
   ```
4. **Commit** com mensagens descritivas
5. **Push** e abra um Pull Request

### 3. Padrões de Commit

Use o formato [Conventional Commits](https://conventionalcommits.org/):

```
tipo(escopo): descrição curta

Descrição mais detalhada se necessário.

Closes #123
```

**Tipos aceitos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Alterações na documentação
- `style`: Formatação, sem mudanças funcionais
- `refactor`: Refatoração de código
- `test`: Adição ou correção de testes
- `chore`: Tarefas de manutenção

**Exemplos:**
```bash
feat(voice): adiciona suporte a novas vozes SAPI
fix(database): corrige problema de conexão SQLite
docs(readme): atualiza instruções de instalação
test(unit): adiciona testes para sistema de nomes
```

## 🏗️ Estrutura do Código

### Organização de Arquivos

```
src/
├── core/                 # Classes principais
│   └── blob_ultra_avancado.py
├── modules/             # Módulos especializados
│   ├── database_manager.py
│   ├── voice_system.py
│   └── personality_engine.py
└── __init__.py

tests/
├── unit/               # Testes unitários
├── integration/        # Testes de integração
└── __init__.py
```

### Padrões de Código

#### Python Style Guide
- Siga a **PEP 8**
- Use **Black** para formatação: `make format`
- Use **flake8** para linting: `make lint`
- Máximo 88 caracteres por linha (Black default)

#### Docstrings
Use formato Google style:

```python
def exemplo_funcao(param1: str, param2: int = 0) -> bool:
    """Breve descrição da função.
    
    Descrição mais detalhada se necessário.
    
    Args:
        param1: Descrição do primeiro parâmetro.
        param2: Descrição do segundo parâmetro com valor padrão.
        
    Returns:
        Descrição do valor retornado.
        
    Raises:
        ValueError: Quando param1 está vazio.
        
    Example:
        >>> exemplo_funcao("teste", 42)
        True
    """
    if not param1:
        raise ValueError("param1 não pode estar vazio")
    return len(param1) > param2
```

#### Type Hints
Use type hints sempre que possível:

```python
from typing import List, Dict, Optional, Union

def processar_dados(
    dados: List[Dict[str, Union[str, int]]], 
    filtro: Optional[str] = None
) -> Dict[str, int]:
    """Processa lista de dados com filtro opcional."""
    # implementação
    pass
```

## 🧪 Testes

### Escrevendo Testes

#### Testes Unitários
```python
# tests/unit/test_exemplo.py
import pytest
from src.modules.exemplo import ExemploClass

class TestExemploClass:
    def setup_method(self):
        """Configuração executada antes de cada teste."""
        self.exemplo = ExemploClass()
    
    def test_metodo_basico(self):
        """Testa funcionalidade básica."""
        resultado = self.exemplo.metodo_basico("input")
        assert resultado == "expected_output"
    
    def test_metodo_com_erro(self):
        """Testa tratamento de erro."""
        with pytest.raises(ValueError):
            self.exemplo.metodo_basico("")
```

#### Testes de Integração
```python
# tests/integration/test_sistema_completo.py
import pytest
from src.core.blob_ultra_avancado import BLOBUltraAvancado

class TestSistemaCompleto:
    def test_fluxo_conversacao(self):
        """Testa fluxo completo de conversação."""
        blob = BLOBUltraAvancado()
        resposta = blob.processar_mensagem("Oi!")
        assert resposta is not None
        assert len(resposta) > 0
```

### Executando Testes

```bash
# Todos os testes
make test

# Testes específicos
pytest tests/unit/test_exemplo.py -v

# Com cobertura
pytest --cov=src --cov-report=html

# Apenas testes que falharam
pytest --lf
```

### Cobertura de Testes
- Mantenha cobertura > **80%**
- Testes críticos devem ter > **95%**
- Use `pytest --cov` para verificar

## 📚 Documentação

### Atualizando Documentação

1. **README.md**: Funcionalidades principais
2. **docs/**: Documentação detalhada
3. **Docstrings**: Documentação inline
4. **Comentários**: Explicações de lógica complexa

### Gerando Documentação

```bash
# TODO: Adicionar geração automática de docs
make docs
```

## 🐛 Reportando Bugs

### Template de Issue

```markdown
**Descrição do Bug**
Descrição clara e concisa do problema.

**Para Reproduzir**
1. Vá para '...'
2. Clique em '....'
3. Role para baixo até '....'
4. Veja o erro

**Comportamento Esperado**
Descrição do que deveria acontecer.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
- OS: [e.g. Windows 11]
- Python: [e.g. 3.9.7]
- Versão do BLOB: [e.g. 2.0.0]

**Contexto Adicional**
Qualquer outra informação relevante.
```

## ✨ Solicitando Features

### Template de Feature Request

```markdown
**A feature está relacionada a um problema?**
Descrição clara do problema.

**Descreva a solução desejada**
Descrição clara da funcionalidade desejada.

**Descreva alternativas consideradas**
Outras soluções ou features consideradas.

**Contexto Adicional**
Screenshots, mockups, ou contexto relevante.
```

## 🎯 Áreas de Contribuição

### Prioridade Alta
- 🐛 Correção de bugs críticos
- 🧪 Aumento de cobertura de testes
- 📚 Melhoria da documentação
- 🚀 Otimização de performance

### Prioridade Média
- ✨ Novas funcionalidades
- 🎨 Melhorias de UI/UX
- 🔧 Refatorações de código
- 🌐 Internacionalização

### Prioridade Baixa
- 📦 Atualizações de dependências
- 🧹 Limpeza de código
- 💄 Melhorias estéticas
- 📖 Tutoriais e exemplos

## 👥 Código de Conduta

### Nossos Padrões

Comportamentos que contribuem para um ambiente positivo:
- Usar linguagem acolhedora e inclusiva
- Respeitar diferentes pontos de vista
- Aceitar críticas construtivas
- Focar no que é melhor para a comunidade
- Mostrar empatia com outros membros

Comportamentos inaceitáveis:
- Linguagem ou imagens sexualizadas
- Comentários insultuosos ou depreciativos
- Assédio público ou privado
- Publicar informações privadas sem permissão
- Outras condutas não profissionais

### Aplicação

Instâncias de comportamento inaceitável podem ser reportadas contactando a equipe do projeto em blob@example.com. Todas as queixas serão revisadas e investigadas.

## 🎉 Reconhecimento

Contribuidores são reconhecidos:
- 📝 **CONTRIBUTORS.md**: Lista de todos os contribuidores
- 🏆 **Badges**: Badges especiais para contribuições significativas
- 📢 **Release Notes**: Menção em notas de lançamento
- 💬 **Agradecimentos**: Posts em redes sociais

## 🤔 Precisa de Ajuda?

- 💬 **Discussões**: [GitHub Discussions](https://github.com/exemplo/blob/discussions)
- 📧 **Email**: blob@example.com
- 🐛 **Issues**: Para bugs e feature requests
- 📚 **Docs**: Consulte a documentação completa

---

**Obrigado por contribuir com o BLOB! 🤖❤️**