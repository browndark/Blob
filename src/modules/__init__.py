"""
Módulos do Sistema BLOB
=======================

Este pacote contém os módulos especializados do sistema BLOB:

- database_manager: Gerenciamento de persistência de dados
- voice_system: Sistema de reconhecimento e síntese de voz  
- personality_engine: Motor de evolução de personalidade
- diagnostico_audio: Ferramentas de diagnóstico de áudio
"""

try:
    from .database_manager import DatabaseManager
    from .voice_system import VoiceSystem  
    from .personality_engine import PersonalityEngine
    from .diagnostico_audio import *
except ImportError:
    pass  # Módulos podem não estar disponíveis em todos os ambientes