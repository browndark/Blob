import sqlite3

conn = sqlite3.connect('data/blob_memory.db')
c = conn.cursor()

print("Tabelas disponíveis:")
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()

for table in tables:
    print(f"  📋 {table[0]}")

# Verificar tabela user_preferences
if ('user_preferences',) in tables:
    print("\n🔍 Verificando user_preferences:")
    c.execute("SELECT key, value FROM user_preferences WHERE key LIKE '%name%'")
    results = c.fetchall()
    
    for key, value in results:
        print(f"  {key}: {value}")
        if 'bianca' in value.lower():
            print(f"    ❌ BIANCA ENCONTRADA - Removendo...")
            c.execute("UPDATE user_preferences SET value = 'BLOB' WHERE key = ? AND value = ?", (key, value))

    # Garantir que blob_name seja BLOB
    c.execute("INSERT OR REPLACE INTO user_preferences (key, value) VALUES ('blob_name', 'BLOB')")
    c.execute("INSERT OR REPLACE INTO user_preferences (key, value) VALUES ('assistant_name', 'BLOB')")
    
    conn.commit()
    print("✅ Nomes atualizados!")

conn.close()