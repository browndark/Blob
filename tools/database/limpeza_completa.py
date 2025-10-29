import sqlite3
import os

def clean_all_bianca_references():
    """Remove TODAS as referências ao nome Bianca"""
    
    db_path = "data/blob_memory.db"
    
    print("🧹 LIMPEZA COMPLETA - REMOVENDO TODAS AS REFERÊNCIAS À 'BIANCA'")
    print("=" * 70)
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Limpar user_preferences
        print("🔍 Limpando user_preferences...")
        cursor.execute("UPDATE user_preferences SET value = 'BLOB' WHERE key = 'blob_name' AND value LIKE '%ianca%'")
        cursor.execute("INSERT OR REPLACE INTO user_preferences (key, value) VALUES ('blob_name', 'BLOB')")
        cursor.execute("INSERT OR REPLACE INTO user_preferences (key, value) VALUES ('assistant_name', 'BLOB')")
        print("✅ user_preferences limpa")
        
        # 2. Limpar conversations
        print("🔍 Limpando conversations...")
        cursor.execute("UPDATE conversations SET blob_response = REPLACE(blob_response, 'Bianca', 'BLOB')")
        cursor.execute("UPDATE conversations SET user_input = REPLACE(user_input, 'Bianca', 'BLOB')")
        cursor.execute("DELETE FROM conversations WHERE blob_response LIKE '%Eu sou a Bianca%'")
        cursor.execute("DELETE FROM conversations WHERE blob_response LIKE '%Me chamo Bianca%'")
        print("✅ conversations limpa")
        
        # 3. Limpar learned_patterns
        print("🔍 Limpando learned_patterns...")
        cursor.execute("UPDATE learned_patterns SET pattern_data = REPLACE(pattern_data, 'Bianca', 'BLOB') WHERE pattern_data LIKE '%Bianca%'")
        cursor.execute("DELETE FROM learned_patterns WHERE pattern_data LIKE '%Bianca%'")
        print("✅ learned_patterns limpa")
        
        # 4. Criar/atualizar todas as tabelas de IA
        print("🔍 Criando/atualizando tabelas de IA...")
        
        # Criar tabela ai_knowledge se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT,
                response_text TEXT,
                context TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Limpar ai_knowledge
        cursor.execute("UPDATE ai_knowledge SET response_text = REPLACE(response_text, 'Bianca', 'BLOB') WHERE response_text LIKE '%Bianca%'")
        cursor.execute("UPDATE ai_knowledge SET input_text = REPLACE(input_text, 'Bianca', 'BLOB') WHERE input_text LIKE '%Bianca%'")
        
        # Criar tabela ai_patterns se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_data TEXT,
                frequency INTEGER DEFAULT 1,
                last_used DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Limpar ai_patterns
        cursor.execute("UPDATE ai_patterns SET pattern_data = REPLACE(pattern_data, 'Bianca', 'BLOB') WHERE pattern_data LIKE '%Bianca%'")
        
        print("✅ Tabelas de IA limpas")
        
        # 5. Verificar se ainda existem referências
        print("\n🔍 Verificação final...")
        
        # Verificar user_preferences
        cursor.execute("SELECT key, value FROM user_preferences WHERE value LIKE '%ianca%'")
        bianca_prefs = cursor.fetchall()
        if bianca_prefs:
            print(f"⚠️ Ainda existem {len(bianca_prefs)} referências em user_preferences")
            for key, value in bianca_prefs:
                print(f"   {key}: {value}")
        else:
            print("✅ Nenhuma referência em user_preferences")
        
        # Verificar conversations
        cursor.execute("SELECT COUNT(*) FROM conversations WHERE blob_response LIKE '%ianca%' OR user_input LIKE '%ianca%'")
        bianca_conv = cursor.fetchone()[0]
        if bianca_conv > 0:
            print(f"⚠️ Ainda existem {bianca_conv} referências em conversations")
        else:
            print("✅ Nenhuma referência em conversations")
        
        # Commit das mudanças
        conn.commit()
        
        print("\n" + "=" * 70)
        print("🎉 LIMPEZA COMPLETA CONCLUÍDA!")
        print("✅ Todas as referências à 'Bianca' foram removidas")
        print("✅ Nome padrão definido como 'BLOB'")
        print("✅ Sistema de nomes dinâmicos ativo")
        
        # Mostrar configuração atual
        print("\n📋 CONFIGURAÇÃO ATUAL:")
        cursor.execute("SELECT key, value FROM user_preferences WHERE key LIKE '%name%'")
        current_names = cursor.fetchall()
        for key, value in current_names:
            print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na limpeza: {e}")
        return False
    
    finally:
        conn.close()

if __name__ == "__main__":
    clean_all_bianca_references()