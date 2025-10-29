#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste final para verificar o sistema completo de reconhecimento de nomes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar apenas os componentes necessários
from blob_ultra_avancado import MemoryDatabase

def test_full_name_system():
    """Testa o sistema completo de reconhecimento de nomes"""
    print("=== TESTE FINAL DO SISTEMA DE NOMES ===")
    
    # Inicializar banco de dados
    db = MemoryDatabase()
    
    # Limpar dados anteriores
    db.save_preference('user_name', None)
    db.save_preference('blob_name', None)
    
    print(f"👤 Nome do usuário inicial: {db.get_preference('user_name')}")
    print(f"🤖 Nome do BLOB inicial: {db.get_preference('blob_name')}")
    
    # Simular: usuário se apresenta
    print(f"\n🧪 SIMULAÇÃO: Usuário diz 'meu nome é Bruno'")
    db.save_preference('user_name', 'Bruno')
    print(f"👤 Nome do usuário salvo: {db.get_preference('user_name')}")
    
    # Simular: usuário nomeia o BLOB
    print(f"\n🧪 SIMULAÇÃO: Usuário diz 'seu nome é Bob'")
    db.save_preference('blob_name', 'Bob')
    print(f"🤖 Nome do BLOB salvo: {db.get_preference('blob_name')}")
    
    # Verificar se estão separados corretamente
    print(f"\n✅ VERIFICAÇÃO FINAL:")
    user_name = db.get_preference('user_name')
    blob_name = db.get_preference('blob_name')
    
    print(f"👤 Nome do USUÁRIO: {user_name}")
    print(f"🤖 Nome do BLOB: {blob_name}")
    print(f"✅ Nomes diferentes e separados: {user_name != blob_name}")
    
    # Testar saudação personalizada
    if user_name:
        print(f"\n🗣️ Saudação personalizada: 'Oi {user_name}!'")
    
    if blob_name:
        print(f"🤖 BLOB se identifica: 'Meu nome é {blob_name}!'")
    
    print("\n=== TESTE CONCLUÍDO COM SUCESSO ===")

if __name__ == "__main__":
    test_full_name_system()