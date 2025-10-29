"""
BLOB - Sistema de Assistente Virtual Interativo
===============================================

Este é o pacote principal do sistema BLOB (Best Learning Optimized Bot),
um assistente virtual avançado com capacidades de:

- Reconhecimento e síntese de voz
- IA emocional com evolução de personalidade  
- Sistema de memória persistente
- Busca inteligente na internet
- Interface gráfica moderna
- Aprendizado de padrões conversacionais

Módulos Principais:
------------------
- core.blob_ultra_avancado: Classe principal do sistema BLOB
- modules.database_manager: Gerenciamento de banco de dados SQLite
- modules.voice_system: Sistema de reconhecimento e síntese de voz
- modules.personality_engine: Motor de evolução de personalidade

Versão: 2.0
Autor: Equipe BLOB
"""

__version__ = "2.0.0"
__author__ = "Equipe BLOB"
__email__ = "blob@example.com"

# Imports principais para facilitar o uso
try:
    from .core.blob_ultra_avancado import BLOBUltraAvancado, MemoryDatabase, EmotionalAI
    from .modules.database_manager import DatabaseManager
    from .modules.voice_system import VoiceSystem
    from .modules.personality_engine import PersonalityEngine
except ImportError:
    # Para quando executado diretamente sem instalação do pacote
    pass