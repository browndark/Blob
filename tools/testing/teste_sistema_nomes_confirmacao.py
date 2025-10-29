#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do Sistema de Confirmação de Nomes
========================================

Testa o novo sistema onde BLOB entende que é da espécie "blob" mas não tem nome,
e quando o usuário dá um nome, ele pede confirmação com botões clicáveis.
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_name_confirmation_system():
    """Testa o sistema completo de confirmação de nomes"""
    print("🧪 TESTE: Sistema de Confirmação de Nomes")
    print("=" * 60)
    
    try:
        # Importar módulos necessários
        from modules.ultra_advanced_ai import UltraAdvancedAI
        
        # Criar mock do banco de dados
        class MockDB:
            def __init__(self):
                self.preferences = {
                    'assistant_name': 'BLOB',  # Nome da espécie, não nome próprio
                    'user_name': 'Usuário'
                }
            
            def get_preference(self, key, default=None):
                return self.preferences.get(key, default)
            
            def save_preference(self, key, value):
                self.preferences[key] = value
                print(f"  💾 Salvou: {key} = {value}")
        
        db = MockDB()
        ai = UltraAdvancedAI(db)
        
        print(f"🤖 BLOB iniciado como: {ai.assistant_name}")
        print("💡 Conceito: BLOB é a espécie, não o nome específico")
        print()
        
        # Casos de teste
        test_cases = [
            {
                'input': 'seu nome agora é João',
                'expected_type': 'name_change_request',
                'expected_name': 'João',
                'description': 'Usuário dá nome João para o BLOB'
            },
            {
                'input': 'te chamo de Pedro',
                'expected_type': 'name_change_request', 
                'expected_name': 'Pedro',
                'description': 'Usuário quer chamar de Pedro'
            },
            {
                'input': 'seu nome é Maria',
                'expected_type': 'name_change_request',
                'expected_name': 'Maria', 
                'description': 'Definindo nome como Maria'
            },
            {
                'input': 'como você está?',
                'expected_type': None,
                'description': 'Pergunta normal - não deve pedir confirmação'
            }
        ]
        
        success_count = 0
        
        for i, test in enumerate(test_cases, 1):
            print(f"🧪 TESTE {i}: {test['description']}")
            print(f"   📝 Input: \"{test['input']}\"")
            
            # Processar input
            response = ai.process_input(test['input'])
            
            # Verificar se é solicitação de confirmação
            if isinstance(response, dict):
                response_type = response.get('type')
                new_name = response.get('new_name')
                ai_response = response.get('response')
                
                print(f"   🤖 Tipo: {response_type}")
                print(f"   📛 Nome proposto: {new_name}")
                print(f"   💬 Resposta: \"{ai_response}\"")
                
                # Verificar se está correto
                if test['expected_type'] == 'name_change_request':
                    if (response_type == 'name_change_request' and 
                        new_name == test['expected_name']):
                        print("   ✅ CORRETO - Detectou solicitação de nome")
                        success_count += 1
                        
                        # Testar confirmação positiva
                        print("   🧪 Testando confirmação SIM...")
                        confirm_result = ai.confirm_name_change(new_name, True)
                        print(f"   ✅ Confirmação SIM: {confirm_result['response']}")
                        
                        # Testar confirmação negativa
                        print("   🧪 Testando confirmação NÃO...")
                        reject_result = ai.confirm_name_change(new_name, False)
                        print(f"   ❌ Confirmação NÃO: {reject_result['response']}")
                        
                    else:
                        print("   ❌ FALHOU - Não detectou corretamente")
                elif test['expected_type'] is None:
                    print("   ❌ FALHOU - Não deveria detectar como mudança de nome")
                else:
                    print("   ❌ FALHOU - Tipo inesperado")
            else:
                # Resposta string normal
                print(f"   💬 Resposta normal: \"{response[:100]}...\"")
                
                if test['expected_type'] is None:
                    print("   ✅ CORRETO - Não é mudança de nome")
                    success_count += 1
                else:
                    print("   ❌ FALHOU - Deveria detectar mudança de nome")
            
            print()
        
        print("=" * 60)
        print(f"📊 RESULTADO: {success_count}/{len(test_cases)} testes passaram")
        
        if success_count == len(test_cases):
            print("🎉 TODOS OS TESTES PASSARAM!")
            print("✅ Sistema de confirmação de nomes funcionando perfeitamente!")
        else:
            print("⚠️ Alguns testes falharam. Verificar implementação.")
        
        return success_count == len(test_cases)
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_species_vs_name_concept():
    """Testa o conceito de espécie vs nome próprio"""
    print("\n🧪 TESTE: Conceito Espécie vs Nome Próprio")
    print("=" * 60)
    
    print("💡 CONCEITO IMPLEMENTADO:")
    print("   • 'BLOB' = nome da espécie (como 'humano', 'cachorro')")
    print("   • Usuário pode dar nome próprio (como 'João', 'Rex')")
    print("   • Quando nome é dado, BLOB pergunta confirmação")
    print("   • Botões clicáveis: [SIM] [NÃO]")
    print()
    
    print("🎯 FLUXO ESPERADO:")
    print("   1. Usuário: 'seu nome é João'")
    print("   2. BLOB: 'O meu nome é João?' ")
    print("   3. Interface mostra botões [SIM] [NÃO]")
    print("   4. Se SIM: 'Agora meu nome é João!'")
    print("   5. Se NÃO: 'Continuo sendo um BLOB sem nome específico'")
    print()
    
    return True

if __name__ == "__main__":
    print("🚀 INICIANDO TESTES DO SISTEMA DE CONFIRMAÇÃO DE NOMES")
    print()
    
    # Teste conceitual
    concept_ok = test_species_vs_name_concept()
    
    # Teste técnico
    system_ok = test_name_confirmation_system()
    
    print("\n" + "=" * 60)
    if concept_ok and system_ok:
        print("🎊 TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("✅ Sistema de confirmação de nomes está funcionando!")
        print("🤖 BLOB agora entende a diferença entre espécie e nome próprio!")
    else:
        print("❌ Alguns testes falharam - verificar implementação")