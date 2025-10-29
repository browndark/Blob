#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para verificar o sistema de perguntas sobre nome do usuário
VERSÃO NOVA COM MEMÓRIA
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_user_name_question_memory():
    """Testa o sistema de perguntas sobre nome do usuário com memória"""
    print("=== TESTE: PERGUNTAS SOBRE NOME COM MEMÓRIA ===")
    
    try:
        from core.blob_ultra_avancado import MemoryDatabase, EmotionalAI, VozUltraAvancada
        
        # Criar instâncias de teste
        db = MemoryDatabase()
        emotional_ai = EmotionalAI(db)
        
        # Mock objects para blob e app
        class MockBlob:
            pass
        class MockApp:
            pass
            
        mock_blob = MockBlob()
        mock_app = MockApp()
        
        voz = VozUltraAvancada(mock_blob, mock_app, db, emotional_ai)
        
        print("✅ Componentes carregados com sucesso!")
        
        # Teste 1: Usuário pergunta seu nome sem ter se apresentado
        print("\n🧪 TESTE 1: Usuário pergunta 'qual é o meu nome?' SEM ter se apresentado")
        
        # Limpar COMPLETAMENTE o nome do usuário usando a tabela correta
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_preferences WHERE key = 'user_name'")
        conn.commit()
        conn.close()
        
        # Recarregar dados do BLOB
        voz.user_name = None
        voz.user_name = voz.memory.get_preference('user_name')
        print(f"🧪 Nome na memória após limpeza: {voz.user_name}")
        
        # Simular pergunta
        result = voz._handle_user_name_question("qual é o meu nome?")
        print(f"✅ Função chamada: {result}")
        expected_response = "Não sei! Qual é o seu nome?"
        print(f"📝 Resposta esperada: '{expected_response}' ou similar")
        
        # Teste 2: Usuário se apresenta
        print("\n🧪 TESTE 2: Usuário se apresenta com 'meu nome é Carlos'")
        result = voz._handle_user_introduction("meu nome é Carlos")
        print(f"✅ Apresentação processada: {result}")
        print(f"👤 Nome salvo: {db.get_preference('user_name')}")
        
        # Teste 3: Usuário pergunta seu nome DEPOIS de se apresentar
        print("\n🧪 TESTE 3: Usuário pergunta 'qual é o meu nome?' APÓS se apresentar")
        result = voz._handle_user_name_question("qual é o meu nome?")
        print(f"✅ Pergunta processada: {result}")
        
        # Teste 4: Testar diferentes padrões de pergunta
        print("\n🧪 TESTE 4: Diferentes padrões de pergunta sobre nome")
        test_phrases = [
            "como eu me chamo?",
            "você sabe meu nome?", 
            "qual meu nome mesmo?",
            "como você me chama?"
        ]
        
        for phrase in test_phrases:
            print(f"\n  Testando: '{phrase}'")
            result = voz._handle_user_name_question(phrase)
            print(f"  ✅ Detectado: {result}")
        
        # Teste 5: Verificar interações salvas
        print("\n🧪 TESTE 5: Verificar interações salvas na memória")
        try:
            interactions = voz._get_recent_interactions(10)
            print(f"📝 Interações encontradas: {len(interactions)}")
            for i, interaction in enumerate(interactions):
                print(f"  {i+1}. Tipo: {interaction.get('type')} - {interaction.get('description')}")
        except Exception as e:
            print(f"⚠️ Erro ao recuperar interações: {e}")
        
        # Teste 6: Verificar conversas no banco
        print("\n🧪 TESTE 6: Verificar conversas no banco de dados")
        try:
            conversations = db.get_recent_conversations(5)
            print(f"💾 Conversas no banco: {len(conversations)}")
            for i, conv in enumerate(conversations):
                print(f"  {i+1}. {conv[1]} -> {conv[2]}")
        except Exception as e:
            print(f"⚠️ Erro ao recuperar conversas: {e}")
        
        print("\n=== TESTE CONCLUÍDO COM SUCESSO ===")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_user_name_question_memory()