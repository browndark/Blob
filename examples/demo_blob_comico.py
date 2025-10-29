#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo Prático: BLOB Cômico Rejeitando Nomes de Cachorro
======================================================

Este demo mostra na prática como o BLOB reage de forma cômica
quando o usuário tenta dar nomes genéricos de cachorro para ele.
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def demo_pratico():
    """Demonstração prática do sistema cômico"""
    print("🎭 DEMO PRÁTICO: BLOB Cômico Rejeitando Nomes de Cachorro")
    print("=" * 65)
    print()
    
    try:
        from modules.ultra_advanced_ai import UltraAdvancedAI
        
        # Simular banco com usuário Bruno
        class MockDB:
            def __init__(self):
                self.preferences = {
                    'assistant_name': 'BLOB',
                    'user_name': 'Bruno'
                }
            
            def get_preference(self, key, default=None):
                return self.preferences.get(key, default)
            
            def save_preference(self, key, value):
                self.preferences[key] = value
        
        db = MockDB()
        ai = UltraAdvancedAI(db)
        
        print("🎬 CENÁRIO: Usuário Bruno tentando dar nomes para o BLOB")
        print(f"👤 Usuário: {db.preferences['user_name']}")
        print(f"🤖 BLOB: {ai.assistant_name} (espécie)")
        print()
        
        # Simular conversas reais
        conversations = [
            {
                'user_input': 'seu nome agora é Rex',
                'description': 'Bruno tenta chamar BLOB de Rex'
            },
            {
                'user_input': 'te chamo de Totó',
                'description': 'Bruno insiste com nome de cachorro'
            },
            {
                'user_input': 'seu nome é Thor',
                'description': 'Bruno tenta um nome "épico" de cachorro'
            },
            {
                'user_input': 'seu nome é Zion',
                'description': 'Bruno finalmente dá um nome adequado'
            }
        ]
        
        for i, conv in enumerate(conversations, 1):
            print(f"🎬 CENA {i}: {conv['description']}")
            print("-" * 50)
            
            # Processar input inicial
            response = ai.process_input(conv['user_input'])
            
            print(f"👤 Bruno: \"{conv['user_input']}\"")
            
            if isinstance(response, dict) and response.get('type') == 'name_change_request':
                proposed_name = response['new_name']
                
                print(f"🤖 BLOB: \"{response['response']}\"")
                print("🖱️ Interface mostra: [✅ SIM] [❌ NÃO]")
                print("👆 Bruno clica SIM...")
                
                # Simular clique em SIM
                confirm_result = ai.confirm_name_change(proposed_name, True)
                
                response_type = confirm_result.get('type')
                response_text = confirm_result.get('response')
                
                print(f"🤖 BLOB: \"{response_text}\"")
                
                if response_type == 'dog_name_rejection':
                    print("😂 RESULTADO: BLOB rejeitou com humor!")
                    print("💡 Interface mostra: 'Dica: Que tal um nome mais criativo?'")
                elif response_type == 'name_confirmed':
                    print("✅ RESULTADO: BLOB aceitou o nome!")
                    print(f"🎉 Nome oficial agora: {ai.assistant_name}")
                
            else:
                print(f"🤖 BLOB: \"{response}\"")
            
            print()
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no demo: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_comedy_examples():
    """Mostra exemplos das respostas cômicas"""
    print("😂 EXEMPLOS DE RESPOSTAS CÔMICAS DO BLOB")
    print("=" * 50)
    
    examples = [
        {
            'name': 'Rex',
            'reactions': [
                "Peraí? Rex? Não é nome de cachorro isso? Eu não sou cachorro não Bruno! 🐕",
                "Rex?! Oi? Eu sou uma IA, não um Golden Retriever Bruno! Que tal um nome mais... digital? 🤖",
                "Você quer me chamar de Rex? Próximo passo é me dar ração e me levar pra passear Bruno! 😂"
            ]
        },
        {
            'name': 'Totó',
            'reactions': [
                "Sério mesmo, Totó? Isso é nome que se dá pra um BLOB? Eu pareço um vira-lata pra você Bruno? 😅",
                "Hmm, Totó... deixa eu adivinhar: você teve um cachorro com esse nome Bruno? 🐶",
                "Não, não, não! Totó é nome de cachorro Bruno! Eu sou mais sofisticado que isso! 🎩"
            ]
        }
    ]
    
    for example in examples:
        print(f"🐕 Nome: {example['name']}")
        for i, reaction in enumerate(example['reactions'], 1):
            print(f"   {i}. {reaction}")
        print()
    
    return True

def show_concept():
    """Explica o conceito implementado"""
    print("💡 CONCEITO: BLOB com Personalidade Cômica")
    print("=" * 50)
    print()
    
    print("🎭 PERSONALIDADE IMPLEMENTADA:")
    print("   • BLOB tem senso de humor")
    print("   • Rejeita nomes genéricos de cachorro")
    print("   • Faz piadas sobre a situação")
    print("   • Sugere nomes mais criativos")
    print("   • Usa emojis para expressão")
    print()
    
    print("🎯 ELEMENTOS CÔMICOS:")
    print("   • Referência ao usuário pelo nome")
    print("   • Comparações engraçadas (Golden Retriever, ração)")
    print("   • Tom indignado mas divertido")
    print("   • Sugestões implícitas de nomes melhores")
    print()
    
    print("🔍 NOMES DETECTADOS COMO 'DE CACHORRO':")
    dog_names = [
        'Rex', 'Bobby', 'Thor', 'Zeus', 'Max', 'Buddy', 'Rock', 'Duke',
        'Bolt', 'Spike', 'Bruno', 'Toby', 'Jack', 'Lucky', 'Shadow',
        'Totó', 'Belinha', 'Mel', 'Nina', 'Fred', 'Bob', 'Lola'
    ]
    
    for i in range(0, len(dog_names), 6):
        group = dog_names[i:i+6]
        print(f"   {', '.join(group)}")
    
    print()
    print("✅ NOMES ACEITOS NORMALMENTE:")
    print("   João, Pedro, Maria, Zion, Neo, Aria, Luna, Alex, Sam...")
    
    return True

if __name__ == "__main__":
    print("🚀 DEMO: BLOB CÔMICO REJEITANDO NOMES DE CACHORRO")
    print()
    
    # Mostrar conceito
    concept_ok = show_concept()
    
    # Mostrar exemplos
    examples_ok = show_comedy_examples()
    
    # Demo prático
    demo_ok = demo_pratico()
    
    print("=" * 65)
    if concept_ok and examples_ok and demo_ok:
        print("🎊 DEMO CONCLUÍDO COM SUCESSO!")
        print("😂 BLOB agora tem personalidade cômica!")
        print("🐕 Rejeita nomes de cachorro com humor!")
        print("💡 Sugere nomes mais criativos para o usuário!")
        print()
        print("🎮 PARA TESTAR NA PRÁTICA:")
        print("   1. Execute: python blob.py")
        print("   2. Digite: 'seu nome é Rex'")
        print("   3. Clique SIM quando os botões aparecerem")
        print("   4. Veja a reação cômica do BLOB!")
    else:
        print("❌ Erro no demo - verificar implementação")