#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug específico para o cumprimento "BLOB, tudo bem?"
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def debug_cumprimento():
    print("🔍 DEBUG: Cumprimento 'BLOB, tudo bem?'")
    print("=" * 50)
    
    try:
        from modules.ultra_advanced_ai import UltraAdvancedAI
        
        class MockDB:
            def __init__(self):
                self.preferences = {'assistant_name': 'BLOB', 'blob_name': 'BLOB'}
            
            def get_preference(self, key, default=None):
                return self.preferences.get(key, default)
            
            def save_preference(self, key, value):
                self.preferences[key] = value
        
        ai = UltraAdvancedAI(MockDB())
        
        texto = "BLOB, tudo bem?"
        texto_lower = texto.lower()
        
        print(f"📝 Texto original: '{texto}'")
        print(f"📝 Texto lower: '{texto_lower}'")
        print(f"🤖 Nome do assistente: '{ai.assistant_name}'")
        print(f"🤖 Nome lower: '{ai.assistant_name.lower()}'")
        
        # Testar cada padrão individualmente
        patterns = [
            f'{ai.assistant_name.lower()},',
            f'oi {ai.assistant_name.lower()}',
            f'olá {ai.assistant_name.lower()}',
            'blob,',
            f'e aí {ai.assistant_name.lower()}',
            f'{ai.assistant_name.lower()}, oi',
            f'{ai.assistant_name.lower()}, tudo bem',
            f'{ai.assistant_name.lower()}, tudo'
        ]
        
        print("\n🔍 Testando padrões individuais:")
        for pattern in patterns:
            match = pattern in texto_lower
            print(f"  '{pattern}' in texto_lower: {match}")
        
        # Testar condição OR
        nome_no_texto = ai.assistant_name.lower() in texto_lower
        palavras_tudo = ['tudo bem', 'tudo', 'como vai']
        palavras_match = [word for word in palavras_tudo if word in texto_lower]
        
        print(f"\n🔍 Condição OR:")
        print(f"  Nome no texto: {nome_no_texto}")
        print(f"  Palavras encontradas: {palavras_match}")
        print(f"  Condição OR: {nome_no_texto and len(palavras_match) > 0}")
        
        # Testar resposta real
        print(f"\n🤖 Resposta atual:")
        resposta = ai.process_input(texto)
        print(f"  '{resposta}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_cumprimento()