import sqlite3

conn = sqlite3.connect('data/blob_memory.db')
c = conn.cursor()

# Atualizar nome para BLOB
c.execute("UPDATE user_preferences SET value = 'BLOB' WHERE key = 'blob_name'")
c.execute("INSERT OR REPLACE INTO user_preferences (key, value) VALUES ('assistant_name', 'BLOB')")

conn.commit()
print("✅ Nome atualizado para BLOB!")

# Verificar mudança
c.execute("SELECT key, value FROM user_preferences WHERE key LIKE '%name%'")
results = c.fetchall()

print("\nNomes atuais:")
for key, value in results:
    print(f"  {key}: {value}")

conn.close()