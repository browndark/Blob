#!/usr/bin/env python3
"""
BLOB - Sistema de Assistente Virtual Interativo
===============================================

Este é o ponto de entrada principal para o sistema BLOB.
Execute este arquivo para iniciar o assistente virtual.

Uso:
    python blob.py [opções]

Opções:
    --dev       Executa em modo desenvolvimento
    --config    Especifica arquivo de configuração alternativo
    --verbose   Executa com logs detalhados
    --help      Mostra esta ajuda
"""

import sys
import os
import argparse
import json
from pathlib import Path

# Adiciona o diretório src ao path
project_root = Path(__file__).parent.absolute()
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def load_config(config_path=None, dev_mode=False):
    """Carrega configuração do arquivo JSON"""
    if config_path:
        config_file = Path(config_path)
    elif dev_mode:
        config_file = project_root / "config" / "config_dev.json"
    else:
        config_file = project_root / "config" / "config.json"
    
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"⚠️  Arquivo de configuração não encontrado: {config_file}")
        return {"blob_config": {}}

def setup_environment(config, verbose=False):
    """Configura o ambiente de execução"""
    # Configura nível de log
    log_level = config.get("blob_config", {}).get("log_level", "INFO")
    if verbose:
        log_level = "DEBUG"
    
    os.environ["BLOB_LOG_LEVEL"] = log_level
    
    # Configura outros parâmetros de ambiente
    if config.get("blob_config", {}).get("debug", False):
        os.environ["BLOB_DEBUG"] = "1"

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="BLOB - Sistema de Assistente Virtual Interativo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
    python blob.py                 # Execução normal
    python blob.py --dev           # Modo desenvolvimento  
    python blob.py --verbose       # Com logs detalhados
    python blob.py --config custom_config.json  # Config personalizada
        """
    )
    
    parser.add_argument(
        "--dev", 
        action="store_true", 
        help="Executa em modo desenvolvimento"
    )
    parser.add_argument(
        "--config", 
        type=str, 
        help="Caminho para arquivo de configuração personalizado"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Executa com logs detalhados"
    )
    
    args = parser.parse_args()
    
    print("🤖 BLOB - Best Learning Optimized Bot")
    print("=" * 50)
    
    # Carrega configuração
    config = load_config(args.config, args.dev)
    setup_environment(config, args.verbose)
    
    # Informações de inicialização
    version = config.get("blob_config", {}).get("version", "2.0.0")
    mode = "DESENVOLVIMENTO" if args.dev else "PRODUÇÃO"
    
    print(f"📋 Versão: {version}")
    print(f"🔧 Modo: {mode}")
    print(f"📁 Diretório: {project_root}")
    
    if args.verbose:
        print(f"🐛 Debug: Ativado")
        print(f"📝 Log Level: {os.environ.get('BLOB_LOG_LEVEL', 'INFO')}")
    
    print("=" * 50)
    
    try:
        # Importa e executa o BLOB
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        from core.blob_ultra_avancado import main as blob_main
        
        print("🚀 Iniciando BLOB Ultra Avançado...")
        blob_main()
        
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("💡 Verifique se todas as dependências estão instaladas:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n👋 BLOB encerrado pelo usuário.")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()