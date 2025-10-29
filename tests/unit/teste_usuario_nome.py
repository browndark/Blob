#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para verificar o reconhecimento do nome do usuário
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from blob_ultra_avancado import *

def test_user_name_recognition():
    """Testa o sistema de reconhecimento de nome do usuário"""
    print("=== TESTE DE RECONHECIMENTO DE NOME DO USUÁRIO ===")
    
    # Inicializar os componentes necessários
    db = MemoryDatabase()
    emotional_ai = EmotionalAI(db)
    blob = BLOBUltraAvancado(db, emotional_ai)
    
    print(f"👤 Nome do usuário inicial: {blob._get_user_name()}")
    
    # Teste 1: Usuário se apresenta
    print("\n🧪 TESTE 1: Usuário diz 'meu nome é Bruno'")
    result1 = blob._handle_user_introduction("meu nome é Bruno")
    print(f"✅ Reconhecido como introdução do usuário: {result1}")
    print(f"👤 Nome do usuário após introdução: {blob._get_user_name()}")
    
    # Teste 2: Usuário tenta nomear o BLOB
    print("\n🧪 TESTE 2: Usuário diz 'seu nome é Bob'")
    result2 = blob._handle_name_changes("seu nome é Bob", "neutro")
    print(f"✅ Reconhecido como mudança de nome do BLOB: {result2}")
    print(f"🤖 Nome do BLOB após mudança: {blob.memory.get_preference('blob_name')}")
    
    # Teste 3: Diferentes padrões de apresentação
    print("\n🧪 TESTE 3: Diferentes padrões de apresentação")
    test_phrases = [
        "me chamo Ana",
        "sou o Carlos", 
        "eu sou Maria",
        "pode me chamar de João"
    ]
    
    for phrase in test_phrases:
        print(f"\n  Testando: '{phrase}'")
        # Limpar nome anterior
        db.salvar_preferencia('user_name', None)
        blob.user_name = None
        
        result = blob._handle_user_introduction(phrase)
        user_name = blob._get_user_name()
        print(f"  ✅ Reconhecido: {result} | Nome: {user_name}")
    
    print("\n=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    test_user_name_recognition()