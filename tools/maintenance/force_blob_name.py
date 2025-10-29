#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualização forçada do nome para BLOB e aplicação das correções
"""

import sqlite3
import os
import sys

def force_name_update():
    print("🔧 ATUALIZAÇÃO FORÇADA DO SISTEMA")
    print("=" * 50)
    
    # Lista de possíveis bancos de dados
    db_files = [
        'data/blob_memory.db',
        'blob_memory.db',
        'data/blob_3d.db',
        'blob_3d.db',
        'assistant_memory.db'
    ]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            print(f"🔍 Atualizando {db_file}...")
            
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Atualizar user_preferences
                cursor.execute("""
                    UPDATE user_preferences 
                    SET value = 'BLOB' 
                    WHERE key IN ('assistant_name', 'blob_name', 'ai_name')
                """)
                
                # Inserir se não existir
                cursor.execute("""
                    INSERT OR REPLACE INTO user_preferences (key, value)
                    VALUES ('assistant_name', 'BLOB')
                """)
                cursor.execute("""
                    INSERT OR REPLACE INTO user_preferences (key, value)
                    VALUES ('blob_name', 'BLOB')
                """)
                
                # Limpar conversas antigas com Bianca
                cursor.execute("""
                    DELETE FROM conversations 
                    WHERE message LIKE '%Bianca%'
                """)
                
                conn.commit()
                conn.close()
                
                print(f"✅ {db_file} atualizado!")
                
            except Exception as e:
                print(f"⚠️ Erro ao atualizar {db_file}: {e}")
        else:
            print(f"⚪ {db_file} não encontrado")
    
    print("\n🎯 FORÇANDO NOME PADRÃO NO SISTEMA")
    
    # Criar arquivo de configuração forçada
    config_override = {
        "blob_config": {
            "assistant_name": "BLOB",
            "blob_name": "BLOB",
            "default_name": "BLOB",
            "force_name": True
        }
    }
    
    import json
    with open('config/force_blob_name.json', 'w', encoding='utf-8') as f:
        json.dump(config_override, f, indent=2, ensure_ascii=False)
    
    print("✅ Configuração forçada criada!")
    
    print("\n🧹 LIMPANDO CACHE PYTHON")
    
    # Remover arquivos __pycache__
    import shutil
    for root, dirs, files in os.walk('.'):
        for d in dirs:
            if d == '__pycache__':
                cache_path = os.path.join(root, d)
                try:
                    shutil.rmtree(cache_path)
                    print(f"🗑️ Removido: {cache_path}")
                except:
                    pass
    
    print("\n🎉 ATUALIZAÇÃO FORÇADA CONCLUÍDA!")
    print("✅ Nome definido como: BLOB")
    print("✅ Cache limpo")
    print("✅ Configurações atualizadas")
    print("\n🚀 Pode iniciar o BLOB novamente!")

if __name__ == "__main__":
    force_name_update()