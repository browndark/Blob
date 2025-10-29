"""
Gerenciador de Banco de Dados - Persistência de memórias e aprendizado
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = "blob_memory.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Tabela de dados do usuário
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT,
                        blob_name TEXT,
                        first_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        total_conversations INTEGER DEFAULT 0,
                        user_preferences TEXT,  -- JSON
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabela de conversas
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT,
                        message TEXT,
                        response TEXT,
                        emotion_detected TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        session_id TEXT
                    )
                ''')
                
                # Tabela de personalidade
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS personality_traits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        trait_name TEXT UNIQUE,
                        trait_value REAL,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabela de padrões de conversa aprendidos
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversation_patterns (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pattern_type TEXT,
                        pattern_data TEXT,  -- JSON
                        frequency INTEGER DEFAULT 1,
                        last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabela de memórias importantes
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS memories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        memory_type TEXT,  -- 'fact', 'preference', 'event', 'emotion'
                        content TEXT,
                        importance_score REAL DEFAULT 1.0,
                        context TEXT,  -- JSON com contexto adicional
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        accessed_count INTEGER DEFAULT 0,
                        last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabela de configurações
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS settings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        setting_name TEXT UNIQUE,
                        setting_value TEXT,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabela de estatísticas de uso
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS usage_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        stat_name TEXT,
                        stat_value TEXT,
                        date DATE DEFAULT (date('now')),
                        UNIQUE(stat_name, date)
                    )
                ''')
                
                conn.commit()
                print("Banco de dados inicializado com sucesso!")
                
        except sqlite3.Error as e:
            print(f"Erro ao inicializar banco de dados: {e}")
            
    def save_user_data(self, user_name: str, blob_name: str, preferences: Dict = None):
        """Salva ou atualiza dados do usuário"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Verificar se usuário já existe
                cursor.execute("SELECT id FROM user_data WHERE user_name = ?", (user_name,))
                existing = cursor.fetchone()
                
                preferences_json = json.dumps(preferences or {})
                
                if existing:
                    # Atualizar usuário existente
                    cursor.execute('''
                        UPDATE user_data 
                        SET blob_name = ?, 
                            last_interaction = CURRENT_TIMESTAMP,
                            total_conversations = total_conversations + 1,
                            user_preferences = ?
                        WHERE user_name = ?
                    ''', (blob_name, preferences_json, user_name))
                else:
                    # Criar novo usuário
                    cursor.execute('''
                        INSERT INTO user_data (user_name, blob_name, user_preferences)
                        VALUES (?, ?, ?)
                    ''', (user_name, blob_name, preferences_json))
                    
                conn.commit()
                
        except sqlite3.Error as e:
            print(f"Erro ao salvar dados do usuário: {e}")
            
    def get_user_data(self) -> Optional[Dict]:
        """Obtém dados do usuário mais recente"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT user_name, blob_name, first_interaction, last_interaction, 
                           total_conversations, user_preferences
                    FROM user_data 
                    ORDER BY last_interaction DESC 
                    LIMIT 1
                ''')
                
                row = cursor.fetchone()
                if row:
                    return {
                        'user_name': row[0],
                        'blob_name': row[1],
                        'first_interaction': row[2],
                        'last_interaction': row[3],
                        'total_conversations': row[4],
                        'user_preferences': json.loads(row[5]) if row[5] else {}
                    }
                    
        except sqlite3.Error as e:
            print(f"Erro ao buscar dados do usuário: {e}")
            
        return None
        
    def save_conversation(self, user_name: str, message: str, response: str = "", 
                         emotion: str = "", session_id: str = ""):
        """Salva uma conversa"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO conversations (user_name, message, response, emotion_detected, session_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_name, message, response, emotion, session_id))
                
                conn.commit()
                
                # Atualizar estatísticas
                self.update_usage_stat("messages_today", 1)
                
        except sqlite3.Error as e:
            print(f"Erro ao salvar conversa: {e}")
            
    def get_recent_conversations(self, limit: int = 50) -> List[Dict]:
        """Obtém conversas recentes"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT user_name, message, response, emotion_detected, timestamp
                    FROM conversations 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
                
                conversations = []
                for row in cursor.fetchall():
                    conversations.append({
                        'user_name': row[0],
                        'message': row[1],
                        'response': row[2],
                        'emotion': row[3],
                        'timestamp': row[4]
                    })
                    
                return conversations
                
        except sqlite3.Error as e:
            print(f"Erro ao buscar conversas: {e}")
            return []
            
    def save_personality_data(self, personality_json: str):
        """Salva dados de personalidade"""
        try:
            personality_data = json.loads(personality_json)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for trait_name, trait_value in personality_data.items():
                    cursor.execute('''
                        INSERT OR REPLACE INTO personality_traits (trait_name, trait_value, last_updated)
                        VALUES (?, ?, CURRENT_TIMESTAMP)
                    ''', (trait_name, float(trait_value)))
                    
                conn.commit()
                
        except (sqlite3.Error, json.JSONDecodeError) as e:
            print(f"Erro ao salvar personalidade: {e}")
            
    def get_personality_data(self) -> Optional[str]:
        """Obtém dados de personalidade"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT trait_name, trait_value FROM personality_traits')
                
                traits = {}
                for row in cursor.fetchall():
                    traits[row[0]] = row[1]
                    
                return json.dumps(traits) if traits else None
                
        except sqlite3.Error as e:
            print(f"Erro ao buscar personalidade: {e}")
            return None
            
    def save_conversation_patterns(self, patterns: Dict):
        """Salva padrões de conversa aprendidos"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for pattern_type, pattern_data in patterns.items():
                    pattern_json = json.dumps(pattern_data)
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO conversation_patterns 
                        (pattern_type, pattern_data, last_used)
                        VALUES (?, ?, CURRENT_TIMESTAMP)
                    ''', (pattern_type, pattern_json))
                    
                conn.commit()
                
        except sqlite3.Error as e:
            print(f"Erro ao salvar padrões: {e}")
            
    def get_conversation_patterns(self) -> Dict:
        """Obtém padrões de conversa"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT pattern_type, pattern_data FROM conversation_patterns')
                
                patterns = {}
                for row in cursor.fetchall():
                    try:
                        patterns[row[0]] = json.loads(row[1])
                    except json.JSONDecodeError:
                        continue
                        
                return patterns
                
        except sqlite3.Error as e:
            print(f"Erro ao buscar padrões: {e}")
            return {}
            
    def save_memory(self, memory_type: str, content: str, importance: float = 1.0, 
                   context: Dict = None):
        """Salva uma memória importante"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                context_json = json.dumps(context or {})
                
                cursor.execute('''
                    INSERT INTO memories (memory_type, content, importance_score, context)
                    VALUES (?, ?, ?, ?)
                ''', (memory_type, content, importance, context_json))
                
                conn.commit()
                
        except sqlite3.Error as e:
            print(f"Erro ao salvar memória: {e}")
            
    def get_memories(self, memory_type: str = None, limit: int = 100) -> List[Dict]:
        """Obtém memórias salvas"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if memory_type:
                    cursor.execute('''
                        SELECT memory_type, content, importance_score, context, created_at
                        FROM memories 
                        WHERE memory_type = ?
                        ORDER BY importance_score DESC, created_at DESC
                        LIMIT ?
                    ''', (memory_type, limit))
                else:
                    cursor.execute('''
                        SELECT memory_type, content, importance_score, context, created_at
                        FROM memories 
                        ORDER BY importance_score DESC, created_at DESC
                        LIMIT ?
                    ''', (limit,))
                    
                memories = []
                for row in cursor.fetchall():
                    try:
                        context = json.loads(row[3]) if row[3] else {}
                    except json.JSONDecodeError:
                        context = {}
                        
                    memories.append({
                        'type': row[0],
                        'content': row[1],
                        'importance': row[2],
                        'context': context,
                        'created_at': row[4]
                    })
                    
                return memories
                
        except sqlite3.Error as e:
            print(f"Erro ao buscar memórias: {e}")
            return []
            
    def save_setting(self, setting_name: str, setting_value: str):
        """Salva uma configuração"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO settings (setting_name, setting_value, last_updated)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                ''', (setting_name, setting_value))
                
                conn.commit()
                
        except sqlite3.Error as e:
            print(f"Erro ao salvar configuração: {e}")
            
    def get_setting(self, setting_name: str) -> Optional[str]:
        """Obtém uma configuração"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT setting_value FROM settings WHERE setting_name = ?', 
                             (setting_name,))
                
                row = cursor.fetchone()
                return row[0] if row else None
                
        except sqlite3.Error as e:
            print(f"Erro ao buscar configuração: {e}")
            return None
            
    def update_usage_stat(self, stat_name: str, increment: int = 1):
        """Atualiza estatística de uso"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Tentar atualizar estatística existente
                cursor.execute('''
                    UPDATE usage_stats 
                    SET stat_value = CAST(stat_value AS INTEGER) + ?
                    WHERE stat_name = ? AND date = date('now')
                ''', (increment, stat_name))
                
                # Se não existe, criar nova
                if cursor.rowcount == 0:
                    cursor.execute('''
                        INSERT INTO usage_stats (stat_name, stat_value)
                        VALUES (?, ?)
                    ''', (stat_name, str(increment)))
                    
                conn.commit()
                
        except sqlite3.Error as e:
            print(f"Erro ao atualizar estatística: {e}")
            
    def get_usage_stats(self, days: int = 7) -> Dict[str, List[Tuple]]:
        """Obtém estatísticas de uso dos últimos dias"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT stat_name, stat_value, date
                    FROM usage_stats 
                    WHERE date >= date('now', '-{} days')
                    ORDER BY date DESC, stat_name
                '''.format(days))
                
                stats = {}
                for row in cursor.fetchall():
                    stat_name = row[0]
                    if stat_name not in stats:
                        stats[stat_name] = []
                    stats[stat_name].append((row[1], row[2]))
                    
                return stats
                
        except sqlite3.Error as e:
            print(f"Erro ao buscar estatísticas: {e}")
            return {}
            
    def reset_personality(self):
        """Reinicia dados de personalidade"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM personality_traits')
                cursor.execute('DELETE FROM conversation_patterns')
                conn.commit()
                print("Personalidade reiniciada!")
                
        except sqlite3.Error as e:
            print(f"Erro ao reiniciar personalidade: {e}")
            
    def cleanup_old_data(self, days_to_keep: int = 90):
        """Remove dados antigos para manter o banco limpo"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Remover conversas muito antigas
                cursor.execute('''
                    DELETE FROM conversations 
                    WHERE timestamp < datetime('now', '-{} days')
                '''.format(days_to_keep))
                
                # Remover estatísticas antigas
                cursor.execute('''
                    DELETE FROM usage_stats 
                    WHERE date < date('now', '-{} days')
                '''.format(days_to_keep))
                
                # Remover memórias de baixa importância antigas
                cursor.execute('''
                    DELETE FROM memories 
                    WHERE importance_score < 0.5 
                    AND created_at < datetime('now', '-{} days')
                '''.format(days_to_keep // 2))
                
                conn.commit()
                print(f"Dados antigos removidos (mais de {days_to_keep} dias)")
                
        except sqlite3.Error as e:
            print(f"Erro na limpeza de dados: {e}")
            
    def get_database_stats(self) -> Dict[str, int]:
        """Obtém estatísticas do banco de dados"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Contar registros em cada tabela
                tables = ['user_data', 'conversations', 'personality_traits', 
                         'conversation_patterns', 'memories', 'settings', 'usage_stats']
                
                for table in tables:
                    cursor.execute(f'SELECT COUNT(*) FROM {table}')
                    stats[table] = cursor.fetchone()[0]
                    
                return stats
                
        except sqlite3.Error as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {}
            
    def close(self):
        """Fecha conexão com o banco de dados"""
        # SQLite fecha automaticamente as conexões
        pass
        
    def backup_database(self, backup_path: str = None) -> bool:
        """Faz backup do banco de dados"""
        try:
            import shutil
            
            if not backup_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"blob_memory_backup_{timestamp}.db"
                
            shutil.copy2(self.db_path, backup_path)
            print(f"Backup criado: {backup_path}")
            return True
            
        except Exception as e:
            print(f"Erro ao fazer backup: {e}")
            return False
            
    def restore_database(self, backup_path: str) -> bool:
        """Restaura banco de dados do backup"""
        try:
            import shutil
            
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, self.db_path)
                print(f"Banco restaurado de: {backup_path}")
                return True
            else:
                print("Arquivo de backup não encontrado!")
                return False
                
        except Exception as e:
            print(f"Erro ao restaurar backup: {e}")
            return False