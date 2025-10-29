#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do Sistema de Rejeições Cômicas para Nomes de Cachorro
============================================================

Testa o novo sistema onde BLOB rejeita nomes genéricos de cachorro
com respostas cômicas e divertidas.
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_dog_name_rejections():
    """Testa as rejeições cômicas para nomes de cachorro"""
    print("🐕 TESTE: Sistema de Rejeições Cômicas para Nomes de Cachorro")
    print("=" * 70)
    
    try:
        # Importar módulos necessários
        from modules.ultra_advanced_ai import UltraAdvancedAI
        
        # Criar mock do banco de dados
        class MockDB:
            def __init__(self):
                self.preferences = {
                    'assistant_name': 'BLOB',
                    'user_name': 'Bruno'  # Nome do usuário para referência cômica
                }
            
            def get_preference(self, key, default=None):
                return self.preferences.get(key, default)
            
            def save_preference(self, key, value):
                self.preferences[key] = value
                print(f"  💾 Salvou: {key} = {value}")
        
        db = MockDB()
        ai = UltraAdvancedAI(db)
        
        print(f"🤖 BLOB iniciado - Usuário: {db.preferences['user_name']}")
        print("😄 Testando reações cômicas para nomes de cachorro...")
        print()
        
        # Nomes de cachorro para testar
        dog_names_tests = [
            'Rex',
            'Bobby', 
            'Thor',
            'Max',
            'Totó',
            'Bob',
            'Bruno',  # Coincide com nome do usuário
            'Lucky'
        ]
        
        # Nomes normais para comparação
        normal_names_tests = [
            'João',
            'Pedro', 
            'Zion',
            'Neo',
            'Aria'
        ]
        
        success_count = 0
        total_tests = 0
        
        print("🐕 TESTANDO NOMES DE CACHORRO (devem ser rejeitados comicamente):")
        print("-" * 60)
        
        for dog_name in dog_names_tests:
            total_tests += 1
            print(f"🧪 Testando nome: '{dog_name}'")
            
            # Simular solicitação de nome
            result = ai.confirm_name_change(dog_name, confirmed=True)
            
            response_type = result.get('type')
            response_text = result.get('response', '')
            
            print(f"   📝 Tipo: {response_type}")
            print(f"   💬 Resposta: \"{response_text}\"")
            
            # Verificar se rejeitou comicamente
            if response_type == 'dog_name_rejection':
                print("   ✅ CORRETO - Rejeitou nome de cachorro com humor!")
                success_count += 1
                
                # Verificar elementos cômicos na resposta
                comic_elements = [
                    'cachorro', 'nome de cachorro', 'vira-lata', 'Golden Retriever',
                    'ração', 'passear', 'genérico', 'sofisticado', '🐕', '🐶'
                ]
                
                found_comedy = any(element in response_text.lower() for element in comic_elements)
                if found_comedy:
                    print("   😂 BONUS - Resposta realmente cômica!")
                else:
                    print("   ⚠️ Resposta poderia ser mais cômica")
                    
            else:
                print("   ❌ FALHOU - Não rejeitou nome de cachorro")
            
            print()
        
        print("👤 TESTANDO NOMES NORMAIS (devem ser aceitos):")
        print("-" * 50)
        
        for normal_name in normal_names_tests:
            total_tests += 1
            print(f"🧪 Testando nome: '{normal_name}'")
            
            result = ai.confirm_name_change(normal_name, confirmed=True)
            
            response_type = result.get('type')
            response_text = result.get('response', '')
            
            print(f"   📝 Tipo: {response_type}")
            print(f"   💬 Resposta: \"{response_text[:50]}...\"")
            
            # Verificar se aceitou normalmente
            if response_type == 'name_confirmed':
                print("   ✅ CORRETO - Aceitou nome normal!")
                success_count += 1
            else:
                print("   ❌ FALHOU - Deveria aceitar nome normal")
            
            print()
        
        print("=" * 70)
        print(f"📊 RESULTADO FINAL: {success_count}/{total_tests} testes passaram")
        
        if success_count == total_tests:
            print("🎉 TODOS OS TESTES PASSARAM!")
            print("😂 Sistema de humor para nomes de cachorro funcionando!")
        else:
            print("⚠️ Alguns testes falharam - verificar implementação")
        
        return success_count == total_tests
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dog_name_detection():
    """Testa especificamente a detecção de nomes de cachorro"""
    print("\n🔍 TESTE: Detecção de Nomes de Cachorro")
    print("=" * 50)
    
    try:
        from modules.ultra_advanced_ai import UltraAdvancedAI
        
        class MockDB:
            def get_preference(self, key, default=None):
                return default
            def save_preference(self, key, value):
                pass
        
        ai = UltraAdvancedAI(MockDB())
        
        # Teste da função de detecção
        test_names = {
            # Devem ser detectados como nomes de cachorro
            'Rex': True,
            'Bobby': True, 
            'Max': True,
            'Totó': True,
            'Thor': True,
            'Lucky': True,
            
            # Não devem ser detectados
            'João': False,
            'Pedro': False,
            'Maria': False,
            'Zion': False,
            'Neo': False,
            'Aria': False
        }
        
        success = 0
        total = len(test_names)
        
        for name, should_be_dog_name in test_names.items():
            is_detected = ai.is_dog_name(name)
            
            if is_detected == should_be_dog_name:
                status = "✅ CORRETO"
                success += 1
            else:
                status = "❌ FALHOU"
            
            expected = "nome de cachorro" if should_be_dog_name else "nome normal"
            print(f"   {name}: {status} (esperado: {expected})")
        
        print(f"\n📊 Detecção: {success}/{total} corretos")
        
        return success == total
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def demo_comic_responses():
    """Demonstra exemplos de respostas cômicas"""
    print("\n😂 DEMO: Exemplos de Respostas Cômicas")
    print("=" * 50)
    
    try:
        from modules.ultra_advanced_ai import UltraAdvancedAI
        
        class MockDB:
            def get_preference(self, key, default=None):
                if key == 'user_name':
                    return 'Bruno'
                return default
            def save_preference(self, key, value):
                pass
        
        ai = UltraAdvancedAI(MockDB())
        
        # Gerar várias respostas para Rex
        print("🎭 Exemplos de respostas para 'Rex':")
        for i in range(3):
            response = ai.get_dog_name_reaction('Rex', 'Bruno')
            print(f"   {i+1}. {response}")
        
        print("\n🎭 Exemplos de respostas para 'Totó':")
        for i in range(3):
            response = ai.get_dog_name_reaction('Totó', 'Bruno')
            print(f"   {i+1}. {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO TESTES DO SISTEMA CÔMICO DE NOMES")
    print()
    
    # Teste de detecção
    detection_ok = test_dog_name_detection()
    
    # Demo de respostas
    demo_ok = demo_comic_responses()
    
    # Teste completo
    system_ok = test_dog_name_rejections()
    
    print("\n" + "=" * 70)
    if detection_ok and demo_ok and system_ok:
        print("🎊 TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("😂 Sistema cômico de rejeição de nomes funcionando!")
        print("🐕 BLOB agora tem personalidade e rejeita nomes de cachorro!")
    else:
        print("❌ Alguns testes falharam - verificar implementação")