import sqlite3

conn = sqlite3.connect('data/blob_memory.db')
c = conn.cursor()

print("Verificando preferências de nome:")
c.execute("SELECT key, value FROM preferences WHERE key LIKE '%name%'")
results = c.fetchall()

for key, value in results:
    print(f"  {key}: {value}")

print("\nVerificando todas as preferências:")
c.execute("SELECT key, value FROM preferences")
all_prefs = c.fetchall()

for key, value in all_prefs:
    if 'bianca' in value.lower():
        print(f"  ❌ BIANCA ENCONTRADA: {key}: {value}")

print("\nAtualizando nomes para BLOB:")
c.execute("UPDATE preferences SET value = 'BLOB' WHERE key = 'blob_name'")
c.execute("INSERT OR REPLACE INTO preferences (key, value) VALUES ('assistant_name', 'BLOB')")
conn.commit()

print("✅ Nomes atualizados!")
conn.close()