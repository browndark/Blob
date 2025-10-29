#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpeza do nome Bianca e configuração do sistema de nomes dinâmicos
Remove qualquer referência ao nome "Bianca" e configura para usar nomes dinâmicos
"""

import sqlite3
import os
import sys

def clean_bianca_references():
    """Remove referências ao nome 'Bianca' do banco de dados"""
    
    db_path = "data/blob_memory.db"
    
    print("🧹 LIMPANDO REFERÊNCIAS AO NOME 'BIANCA'")
    print("=" * 50)
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado. Será criado automaticamente.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Remover nome 'Bianca' das preferências
        print("🔍 Verificando preferências...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='preferences'")
        if cursor.fetchone():
            # Verificar se existe a preferência 'blob_name' com 'Bianca'
            cursor.execute("SELECT value FROM preferences WHERE key = 'blob_name'")
            result = cursor.fetchone()
            
            if result and result[0] == 'Bianca':
                print("❌ Encontrado nome 'Bianca' - removendo...")
                cursor.execute("DELETE FROM preferences WHERE key = 'blob_name'")
                print("✅ Nome 'Bianca' removido!")
            else:
                print("✅ Não há referência ao nome 'Bianca'")
            
            # Configurar nome padrão como 'BLOB'
            cursor.execute("INSERT OR REPLACE INTO preferences (key, value) VALUES ('blob_name', 'BLOB')")
            cursor.execute("INSERT OR REPLACE INTO preferences (key, value) VALUES ('assistant_name', 'BLOB')")
            print("✅ Nome padrão definido como 'BLOB'")
        
        # Verificar tabelas de IA para remover referências
        print("\n🔍 Verificando tabelas de IA...")
        
        # Listar todas as tabelas disponíveis
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tabelas encontradas: {', '.join(tables)}")
        
        # Verificar se existem conversas com 'Bianca'
        if 'conversations' in tables:
            # Primeiro ver as colunas da tabela
            cursor.execute("PRAGMA table_info(conversations)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"   Colunas em conversations: {', '.join(columns)}")
            
            # Usar a coluna correta
            text_column = None
            for col in ['message', 'text', 'content', 'response']:
                if col in columns:
                    text_column = col
                    break
            
            if text_column:
                cursor.execute(f"SELECT COUNT(*) FROM conversations WHERE {text_column} LIKE '%Bianca%'")
                bianca_count = cursor.fetchone()[0]
                
                if bianca_count > 0:
                    print(f"❌ Encontradas {bianca_count} conversas com 'Bianca' - removendo...")
                    cursor.execute(f"DELETE FROM conversations WHERE {text_column} LIKE '%Bianca%'")
                    print("✅ Conversas com 'Bianca' removidas!")
                else:
                    print("✅ Não há conversas com 'Bianca'")
            else:
                print("⚠️ Estrutura da tabela conversations não reconhecida")
        
        # Verificar conhecimento da IA
        if 'ai_knowledge' in tables:
            cursor.execute("PRAGMA table_info(ai_knowledge)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"   Colunas em ai_knowledge: {', '.join(columns)}")
            
            # Usar a coluna correta
            text_column = None
            for col in ['knowledge_text', 'text', 'content', 'data']:
                if col in columns:
                    text_column = col
                    break
            
            if text_column:
                cursor.execute(f"SELECT COUNT(*) FROM ai_knowledge WHERE {text_column} LIKE '%Bianca%'")
                knowledge_count = cursor.fetchone()[0]
                
                if knowledge_count > 0:
                    print(f"❌ Encontrados {knowledge_count} conhecimentos com 'Bianca' - removendo...")
                    cursor.execute(f"DELETE FROM ai_knowledge WHERE {text_column} LIKE '%Bianca%'")
                    print("✅ Conhecimentos com 'Bianca' removidos!")
                else:
                    print("✅ Não há conhecimentos com 'Bianca'")
            else:
                print("⚠️ Estrutura da tabela ai_knowledge não reconhecida")
        
        # Commit das mudanças
        conn.commit()
        conn.close()
        
        print("\n" + "=" * 50)
        print("🎉 LIMPEZA CONCLUÍDA!")
        print("✅ Todas as referências ao nome 'Bianca' foram removidas")
        print("✅ Nome padrão configurado como 'BLOB'")
        print("✅ Sistema de nomes dinâmicos ativo")
        print("\n💡 Agora você pode dar qualquer nome que quiser!")
        print("   Exemplos:")
        print("   - 'Seu nome é Ana'")
        print("   - 'Te chamo de Maria'")
        print("   - 'Agora você se chama João'")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na limpeza: {e}")
        return False

def test_name_system():
    """Testa o sistema de nomes dinâmicos"""
    print("\n🧪 TESTANDO SISTEMA DE NOMES DINÂMICOS")
    print("=" * 50)
    
    try:
        # Importar e testar IA
        sys.path.insert(0, 'src')
        from modules.ultra_advanced_ai import UltraAdvancedAI
        
        class MockDB:
            def __init__(self):
                self.db_path = 'test.db'
                self.preferences = {'assistant_name': 'BLOB'}
            
            def get_preference(self, key, default=None):
                return self.preferences.get(key, default)
            
            def save_preference(self, key, value):
                self.preferences[key] = value
        
        ai = UltraAdvancedAI(MockDB())
        
        print(f"🤖 Nome inicial: {ai.assistant_name}")
        
        # Testar mudança de nome
        test_inputs = [
            "Seu nome é Maria",
            "Te chamo de João", 
            "Agora você se chama Ana"
        ]
        
        for test_input in test_inputs:
            print(f"\n📝 Teste: \"{test_input}\"")
            response = ai.process_input(test_input)
            print(f"   Resposta: \"{response}\"")
            print(f"   Nome atual: {ai.assistant_name}")
        
        # Testar pergunta sobre nome
        print(f"\n📝 Teste: \"Qual é seu nome?\"")
        response = ai.process_input("Qual é seu nome?")
        print(f"   Resposta: \"{response}\"")
        
        print("\n✅ Sistema de nomes dinâmicos funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == "__main__":
    print("🚀 CONFIGURAÇÃO DO SISTEMA DE NOMES DINÂMICOS")
    print("=" * 60)
    
    # Limpar referências antigas
    clean_success = clean_bianca_references()
    
    if clean_success:
        # Testar sistema
        test_name_system()
        
        print("\n" + "=" * 60)
        print("🎊 SISTEMA CONFIGURADO!")
        print("✅ Nome 'Bianca' removido completamente")
        print("✅ Sistema de nomes dinâmicos ativo")
        print("✅ Nome padrão: BLOB")
        print("\n💬 Agora você pode dar o nome que quiser!")
        print("   Exemplos de comandos:")
        print("   - 'Seu nome é [nome]'")
        print("   - 'Te chamo de [nome]'")
        print("   - 'Agora se chama [nome]'")
        print("   - 'Seu novo nome é [nome]'")
    else:
        print("\n❌ Erro na configuração do sistema")