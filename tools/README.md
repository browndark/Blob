# 🛠️ Tools Directory

Este diretório contém ferramentas de desenvolvimento e manutenção do BLOB.

## 📁 Estrutura

### 🗄️ `database/`
Ferramentas para gerenciamento e manutenção do banco de dados:
- `atualizar_nome.py` - Atualização de nomes no banco
- `limpar_nome_bianca.py` - Remove referências antigas
- `limpeza_completa.py` - Limpeza completa do BD
- `verificar_nomes.py` - Verificação de consistência de nomes
- `verificar_tabelas.py` - Verificação de estrutura das tabelas

### 🔧 `maintenance/`
Scripts de manutenção do sistema:
- `force_blob_name.py` - Força atualização do nome para BLOB

### 🧪 `testing/`
Ferramentas de teste e debug:
- `teste_correcoes_direto.py` - Teste das correções implementadas
- `teste_debug_cumprimento.py` - Debug de cumprimentos
- `teste_rapido.py` - Testes rápidos do sistema

## 🎯 Uso

Todas as ferramentas devem ser executadas a partir da raiz do projeto:

```bash
# Exemplo: executar limpeza completa
python tools/database/limpeza_completa.py

# Exemplo: testar correções
python tools/testing/teste_correcoes_direto.py
```

## ⚠️ Importante

- **Sempre faça backup** antes de usar ferramentas de banco de dados
- **Teste em ambiente de desenvolvimento** antes de aplicar em produção
- **Revise logs** após execução das ferramentas