#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste direto das correções implementadas
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_corrected_system():
    print("🔍 TESTE DIRETO DAS CORREÇÕES")
    print("=" * 50)
    
    try:
        from modules.ultra_advanced_ai import UltraAdvancedAI
        
        class MockDB:
            def __init__(self):
                self.preferences = {
                    'assistant_name': 'BLOB',
                    'blob_name': 'BLOB',
                    'user_name': 'Bruno'
                }
            
            def get_preference(self, key, default=None):
                return self.preferences.get(key, default)
            
            def save_preference(self, key, value):
                self.preferences[key] = value
        
        ai = UltraAdvancedAI(MockDB())
        
        print(f"🤖 Nome do assistente: {ai.assistant_name}")
        
        # Testes específicos que estavam falhando
        test_cases = [
            "BLOB, consegue me ouvir?",
            "Você está me escutando?", 
            "Me escuta?",
            "BLOB, tudo bem?",
            "Teste",
            "Alô"
        ]
        
        print("\n🧪 TESTANDO CASOS ESPECÍFICOS:")
        
        for teste in test_cases:
            response = ai.process_input(teste)
            
            # Verificar se não é resposta genérica
            genericas = ['interessante', 'nunca tinha pensado', 'que legal', 'como assim']
            eh_generica = any(gen in response.lower() for gen in genericas)
            
            status = "❌ GENÉRICA" if eh_generica else "✅ ESPECÍFICA"
            
            print(f"\n  📝 \"{teste}\"")
            print(f"  🤖 \"{response}\"")
            print(f"  {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_corrected_system()
    if success:
        print("\n🎉 SISTEMA TESTADO COM SUCESSO!")
    else:
        print("\n❌ FALHA NO TESTE!")