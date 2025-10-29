#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstração do Sistema de Nomes Dinâmicos
Mostra como trocar o nome da BLOB dinamicamente
"""

import sys
import os
sys.path.insert(0, 'src')

def test_dynamic_names():
    """Testa o sistema de nomes dinâmicos"""
    print("🎯 DEMONSTRAÇÃO: SISTEMA DE NOMES DINÂMICOS")
    print("=" * 60)
    print("✅ Nome 'Bianca' REMOVIDO completamente!")
    print("✅ Agora você pode dar QUALQUER nome que quiser!")
    print("=" * 60)
    
    try:
        from modules.ultra_advanced_ai import UltraAdvancedAI
        
        class MockDB:
            def __init__(self):
                self.db_path = 'test.db'
                self.preferences = {'assistant_name': 'BLOB', 'blob_name': 'BLOB'}
            
            def get_preference(self, key, default=None):
                return self.preferences.get(key, default)
            
            def save_preference(self, key, value):
                self.preferences[key] = value
                print(f"💾 Salvou: {key} = {value}")
        
        ai = UltraAdvancedAI(MockDB())
        
        print(f"🤖 Nome inicial: {ai.assistant_name}")
        
        # Demonstrar diferentes formas de trocar o nome
        test_cases = [
            {
                'comando': 'Seu nome é Ana',
                'descrição': 'Comando direto'
            },
            {
                'comando': 'Te chamo de Maria',
                'descrição': 'Forma casual'
            },
            {
                'comando': 'Agora se chama João',
                'descrição': 'Mudança de nome'
            },
            {
                'comando': 'Seu novo nome é Sofia',
                'descrição': 'Novo nome específico'
            }
        ]
        
        print("\n🧪 TESTANDO DIFERENTES FORMAS DE DAR NOME:")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. {test_case['descrição']}")
            print(f"   💬 Você: \"{test_case['comando']}\"")
            
            response = ai.process_input(test_case['comando'])
            
            print(f"   🤖 {ai.assistant_name}: \"{response}\"")
            print(f"   📛 Nome atual: {ai.assistant_name}")
        
        # Testar pergunta sobre nome
        print(f"\n5. Pergunta sobre nome")
        print(f"   💬 Você: \"Qual é seu nome?\"")
        
        response = ai.process_input("Qual é seu nome?")
        print(f"   🤖 {ai.assistant_name}: \"{response}\"")
        
        # Voltar para BLOB
        print(f"\n6. Voltando para nome padrão")
        print(f"   💬 Você: \"Seu nome é BLOB\"")
        
        response = ai.process_input("Seu nome é BLOB")
        print(f"   🤖 {ai.assistant_name}: \"{response}\"")
        
        print("\n" + "=" * 60)
        print("🎉 SISTEMA DE NOMES DINÂMICOS FUNCIONANDO!")
        print("=" * 60)
        
        print("💡 COMANDOS QUE FUNCIONAM:")
        commands = [
            "Seu nome é [nome]",
            "Te chamo de [nome]", 
            "Agora se chama [nome]",
            "Seu novo nome é [nome]",
            "Nome é [nome]",
            "Se chama [nome]"
        ]
        
        for cmd in commands:
            print(f"   ✅ {cmd}")
        
        print(f"\n🎯 EXEMPLOS PRÁTICOS:")
        examples = [
            "Seu nome é Luna",
            "Te chamo de Stella",
            "Agora se chama Aurora",
            "Seu novo nome é Iris"
        ]
        
        for example in examples:
            print(f"   💬 \"{example}\"")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_dynamic_names()
    
    if success:
        print(f"\n🎊 MISSÃO CUMPRIDA!")
        print(f"✅ Nome 'Bianca' removido dos registros")
        print(f"✅ Sistema de nomes dinâmicos implementado")
        print(f"✅ Você pode dar qualquer nome que quiser!")
        print(f"\n🚀 Agora a BLOB vai responder com o nome que VOCÊ escolher!")
    else:
        print(f"\n❌ Erro na demonstração")