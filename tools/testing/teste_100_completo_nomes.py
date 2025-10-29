#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE COMPLETO 100% - Sistema de Interação com Nomes
====================================================

Este teste valida COMPLETAMENTE todas as funcionalidades do sistema de nomes:
1. Detecção de solicitações de nome
2. Confirmação com botões
3. Rejeições cômicas para nomes de cachorro  
4. Aceitação de nomes normais
5. Casos extremos e edge cases
6. Integração completa da interface
"""

import sys
import os
import time

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_100_percent_name_system():
    """Teste 100% completo do sistema de nomes"""
    print("🎯 TESTE 100% COMPLETO - Sistema de Interação com Nomes")
    print("=" * 80)
    
    try:
        from modules.ultra_advanced_ai import UltraAdvancedAI
        
        # Mock database mais completo
        class CompleteMockDB:
            def __init__(self):
                self.preferences = {
                    'assistant_name': 'BLOB',
                    'user_name': 'Bruno',
                    'blob_name': 'BLOB'
                }
                self.interactions = []
            
            def get_preference(self, key, default=None):
                return self.preferences.get(key, default)
            
            def save_preference(self, key, value):
                self.preferences[key] = value
                self.interactions.append(f"Salvou: {key} = {value}")
                print(f"    💾 {key} = {value}")
            
            def get_interactions(self):
                return self.interactions
        
        db = CompleteMockDB()
        ai = UltraAdvancedAI(db)
        
        print(f"🤖 BLOB Sistema: {ai.assistant_name}")
        print(f"👤 Usuário: {db.preferences['user_name']}")
        print()
        
        # === FASE 1: TESTE DE DETECÇÃO DE PADRÕES ===
        print("🔍 FASE 1: DETECÇÃO DE PADRÕES DE NOMENCLATURA")
        print("-" * 60)
        
        detection_patterns = [
            # Padrões básicos
            'seu nome é João',
            'seu nome agora é Pedro', 
            'nome é Maria',
            'te chamo de Carlos',
            'chamo de Ana',
            'te chamar de Bruno',
            'chamar de Sofia',
            'nome seja Lucas',
            'nome será Juliana',
            'agora se chama Gabriel',
            'se chama Isabella',
            'seu novo nome é Rafael',
            'novo nome é Valentina',
            
            # Variações de linguagem natural
            'quero que você se chame Miguel',
            'gostaria de te chamar de Helena',
            'vou te dar o nome de Diego',
            'seu nome vai ser Beatriz',
            'você vai se chamar Arthur',
            
            # Casos com pontuação
            'seu nome é João!',
            'te chamo de Pedro.',
            'nome é Maria?',
            
            # Casos que NÃO devem detectar
            'qual é seu nome?',
            'me diga seu nome',
            'como você se chama?',
            'você tem nome?',
            'nome bonito esse',
        ]
        
        detection_success = 0
        detection_total = len(detection_patterns)
        
        for i, pattern in enumerate(detection_patterns):
            should_detect = not any(question in pattern.lower() for question in 
                                  ['qual', 'como', 'me diga', 'você tem', 'bonito'])
            
            response = ai.process_input(pattern)
            detected = isinstance(response, dict) and response.get('type') == 'name_change_request'
            
            status = "✅" if detected == should_detect else "❌"
            expected = "DETECTAR" if should_detect else "IGNORAR"
            
            print(f"  {status} \"{pattern}\" → {expected}")
            
            if detected == should_detect:
                detection_success += 1
        
        detection_score = (detection_success / detection_total) * 100
        print(f"\n📊 Detecção de Padrões: {detection_success}/{detection_total} ({detection_score:.1f}%)")
        
        # === FASE 2: TESTE DE NOMES DE CACHORRO ===
        print(f"\n🐕 FASE 2: REJEIÇÃO CÔMICA DE NOMES DE CACHORRO")
        print("-" * 60)
        
        dog_names_complete = [
            # Inglês genéricos
            'Rex', 'Max', 'Buddy', 'Charlie', 'Jack', 'Rocky', 'Tucker',
            'Duke', 'Bear', 'Zeus', 'Thor', 'Hunter', 'Shadow', 'Lucky',
            'Cooper', 'Toby', 'Bobby', 'Spike', 'Bruno', 'Bolt',
            
            # Português comuns
            'Totó', 'Belinha', 'Mel', 'Nina', 'Fred', 'Bob', 'Lola',
            'Simba', 'Bruce', 'Branquinho', 'Farofa', 'Pipoca',
            'Chocolate', 'Café', 'Caramelo', 'Pituco', 'Fofinho',
            
            # Casos mistos
            'THOR', 'max', 'Rex Jr', 'Bobby II'
        ]
        
        dog_names_success = 0
        
        for dog_name in dog_names_complete:
            is_detected = ai.is_dog_name(dog_name)
            
            if is_detected:
                # Testar reação cômica
                reaction = ai.get_dog_name_reaction(dog_name, 'Bruno')
                
                # Verificar elementos cômicos
                comic_elements = [
                    'cachorro', 'nome de cachorro', 'vira-lata', 'golden retriever',
                    'ração', 'passear', 'genérico', 'sofisticado', '🐕', '🐶',
                    'não sou cachorro', 'eu sou uma ia'
                ]
                
                has_comedy = any(element in reaction.lower() for element in comic_elements)
                
                # Testar confirmação
                confirm_result = ai.confirm_name_change(dog_name, True)
                is_rejected = confirm_result.get('type') == 'dog_name_rejection'
                
                if has_comedy and is_rejected:
                    print(f"  ✅ {dog_name} → Rejeitado comicamente")
                    dog_names_success += 1
                else:
                    print(f"  ❌ {dog_name} → Falhou na rejeição cômica")
            else:
                print(f"  ❌ {dog_name} → Não detectado como nome de cachorro")
        
        dog_score = (dog_names_success / len(dog_names_complete)) * 100
        print(f"\n📊 Rejeição de Nomes de Cachorro: {dog_names_success}/{len(dog_names_complete)} ({dog_score:.1f}%)")
        
        # === FASE 3: TESTE DE NOMES NORMAIS ===
        print(f"\n✅ FASE 3: ACEITAÇÃO DE NOMES NORMAIS")
        print("-" * 60)
        
        normal_names = [
            # Nomes brasileiros comuns
            'João', 'Pedro', 'Maria', 'Ana', 'Carlos', 'Sofia',
            'Lucas', 'Juliana', 'Gabriel', 'Isabella', 'Rafael', 'Valentina',
            'Miguel', 'Helena', 'Diego', 'Beatriz', 'Arthur', 'Lorena',
            
            # Nomes modernos/únicos
            'Zion', 'Neo', 'Aria', 'Luna', 'Phoenix', 'Nova', 'Atlas',
            'Sage', 'River', 'Sky', 'Echo', 'Raven', 'Storm', 'Orion',
            
            # Nomes internacionais
            'Alexander', 'Sophia', 'William', 'Emma', 'James', 'Olivia',
            'Benjamin', 'Charlotte', 'Sebastian', 'Amelia',
            
            # Nomes criativos
            'Pixel', 'Quantum', 'Matrix', 'Cyber', 'Digital', 'Alpha',
            'Beta', 'Gamma', 'Omega', 'Prime'
        ]
        
        normal_names_success = 0
        
        for normal_name in normal_names:
            is_dog_name = ai.is_dog_name(normal_name)
            
            if not is_dog_name:
                # Testar aceitação
                confirm_result = ai.confirm_name_change(normal_name, True)
                is_accepted = confirm_result.get('type') == 'name_confirmed'
                
                if is_accepted:
                    print(f"  ✅ {normal_name} → Aceito normalmente")
                    normal_names_success += 1
                else:
                    print(f"  ❌ {normal_name} → Falhou na aceitação")
            else:
                print(f"  ⚠️ {normal_name} → Incorretamente detectado como nome de cachorro")
        
        normal_score = (normal_names_success / len(normal_names)) * 100
        print(f"\n📊 Aceitação de Nomes Normais: {normal_names_success}/{len(normal_names)} ({normal_score:.1f}%)")
        
        # === FASE 4: CASOS EXTREMOS ===
        print(f"\n🧪 FASE 4: CASOS EXTREMOS E EDGE CASES")
        print("-" * 60)
        
        edge_cases = [
            # Nomes muito curtos
            ('A', False, 'Nome muito curto'),
            ('Ai', False, 'Nome de 2 letras'),
            
            # Nomes com números/símbolos
            ('João123', False, 'Nome com números'),
            ('Pedro!', False, 'Nome com símbolos'),
            ('Ana-Maria', False, 'Nome composto com hífen'),
            
            # Nomes vazios/inválidos
            ('', False, 'Nome vazio'),
            ('   ', False, 'Nome só espaços'),
            
            # Nomes válidos limítrofes
            ('Lia', True, 'Nome curto válido'),
            ('Ion', True, 'Nome de 3 letras'),
            ('João Paulo', True, 'Nome composto com espaço'),
            
            # Capitalização
            ('joão', True, 'Nome minúsculo'),
            ('PEDRO', True, 'Nome maiúsculo'),
            ('mArIa', True, 'Nome capitalização mista'),
        ]
        
        edge_success = 0
        
        for test_name, should_work, description in edge_cases:
            try:
                # Simular input completo
                full_input = f"seu nome é {test_name}" if test_name.strip() else "seu nome é "
                response = ai.process_input(full_input)
                
                worked = isinstance(response, dict) and response.get('type') == 'name_change_request'
                
                if worked == should_work:
                    print(f"  ✅ {description}: \"{test_name}\" → {'Funcionou' if worked else 'Rejeitado'}")
                    edge_success += 1
                else:
                    print(f"  ❌ {description}: \"{test_name}\" → Comportamento inesperado")
                    
            except Exception as e:
                if not should_work:
                    print(f"  ✅ {description}: \"{test_name}\" → Erro esperado: {e}")
                    edge_success += 1
                else:
                    print(f"  ❌ {description}: \"{test_name}\" → Erro inesperado: {e}")
        
        edge_score = (edge_success / len(edge_cases)) * 100
        print(f"\n📊 Casos Extremos: {edge_success}/{len(edge_cases)} ({edge_score:.1f}%)")
        
        # === FASE 5: TESTE DE INTEGRAÇÃO COMPLETA ===
        print(f"\n🔄 FASE 5: INTEGRAÇÃO COMPLETA (FLUXO REAL)")
        print("-" * 60)
        
        integration_scenarios = [
            {
                'input': 'seu nome agora é Rex',
                'expected_flow': ['name_change_request', 'dog_name_rejection'],
                'description': 'Fluxo completo: nome de cachorro'
            },
            {
                'input': 'te chamo de Zion', 
                'expected_flow': ['name_change_request', 'name_confirmed'],
                'description': 'Fluxo completo: nome normal'
            },
            {
                'input': 'seu nome é Totó',
                'expected_flow': ['name_change_request', 'dog_name_rejection'], 
                'description': 'Rejeição cômica brasileira'
            },
            {
                'input': 'novo nome é Neo',
                'expected_flow': ['name_change_request', 'name_confirmed'],
                'description': 'Nome criativo aceito'
            }
        ]
        
        integration_success = 0
        
        for scenario in integration_scenarios:
            print(f"\n  🎬 Cenário: {scenario['description']}")
            print(f"       Input: \"{scenario['input']}\"")
            
            # Passo 1: Detecção
            step1_response = ai.process_input(scenario['input'])
            step1_ok = (isinstance(step1_response, dict) and 
                       step1_response.get('type') == scenario['expected_flow'][0])
            
            print(f"       Passo 1: {'✅' if step1_ok else '❌'} {scenario['expected_flow'][0]}")
            
            if step1_ok and len(scenario['expected_flow']) > 1:
                # Passo 2: Confirmação
                proposed_name = step1_response.get('new_name')
                step2_response = ai.confirm_name_change(proposed_name, True)
                step2_ok = step2_response.get('type') == scenario['expected_flow'][1]
                
                print(f"       Passo 2: {'✅' if step2_ok else '❌'} {scenario['expected_flow'][1]}")
                
                if step1_ok and step2_ok:
                    integration_success += 1
                    print(f"       Resultado: ✅ COMPLETO")
                else:
                    print(f"       Resultado: ❌ FALHOU")
            elif step1_ok:
                integration_success += 1
                print(f"       Resultado: ✅ COMPLETO")
            else:
                print(f"       Resultado: ❌ FALHOU")
        
        integration_score = (integration_success / len(integration_scenarios)) * 100
        print(f"\n📊 Integração Completa: {integration_success}/{len(integration_scenarios)} ({integration_score:.1f}%)")
        
        # === RESULTADO FINAL ===
        print(f"\n" + "=" * 80)
        print("🎯 RESULTADO FINAL - TESTE 100% COMPLETO")
        print("=" * 80)
        
        total_score = (detection_score + dog_score + normal_score + edge_score + integration_score) / 5
        
        print(f"📊 PONTUAÇÃO POR CATEGORIA:")
        print(f"   🔍 Detecção de Padrões:        {detection_score:6.1f}%")
        print(f"   🐕 Rejeição Nomes Cachorro:    {dog_score:6.1f}%")
        print(f"   ✅ Aceitação Nomes Normais:    {normal_score:6.1f}%")
        print(f"   🧪 Casos Extremos:             {edge_score:6.1f}%")
        print(f"   🔄 Integração Completa:        {integration_score:6.1f}%")
        print(f"   " + "-" * 40)
        print(f"   🎯 PONTUAÇÃO FINAL:            {total_score:6.1f}%")
        
        if total_score >= 95:
            print(f"\n🏆 EXCELENTE! Sistema funcionando em nível profissional!")
        elif total_score >= 85:
            print(f"\n✅ MUITO BOM! Sistema robusto com pequenos ajustes necessários.")
        elif total_score >= 70:
            print(f"\n⚠️ SATISFATÓRIO! Sistema funcional mas precisa de melhorias.")
        else:
            print(f"\n❌ INSATISFATÓRIO! Sistema precisa de correções significativas.")
        
        # Estatísticas detalhadas
        total_tests = detection_total + len(dog_names_complete) + len(normal_names) + len(edge_cases) + len(integration_scenarios)
        total_success = detection_success + dog_names_success + normal_names_success + edge_success + integration_success
        
        print(f"\n📈 ESTATÍSTICAS DETALHADAS:")
        print(f"   Total de Testes: {total_tests}")
        print(f"   Testes Passaram: {total_success}")
        print(f"   Taxa de Sucesso: {(total_success/total_tests)*100:.1f}%")
        print(f"   Tempo de Execução: {time.time() - start_time:.2f}s")
        
        return total_score >= 90
        
    except Exception as e:
        print(f"❌ Erro crítico no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    start_time = time.time()
    print("🚀 INICIANDO TESTE 100% COMPLETO DO SISTEMA DE NOMES")
    print("⏱️ Este teste pode levar alguns minutos...")
    print()
    
    success = test_100_percent_name_system()
    
    print(f"\n" + "=" * 80)
    if success:
        print("🎊 TESTE 100% CONCLUÍDO COM SUCESSO!")
        print("✅ Sistema de nomes está funcionando perfeitamente!")
        print("🤖 BLOB pronto para interação com nomes em produção!")
    else:
        print("⚠️ Teste identificou áreas que precisam de melhoria.")
        print("🔧 Verifique os resultados acima para ajustes necessários.")
    
    print(f"⏱️ Tempo total: {time.time() - start_time:.2f} segundos")