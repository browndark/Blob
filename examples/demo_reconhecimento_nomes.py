#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstração do Sistema de Reconhecimento de Nomes
Este script demonstra como o BLOB distingue entre:
- Apresentação do usuário: "meu nome é Bruno"
- Nomeação do BLOB: "seu nome é Bob"
"""

import sys
import os

def demo_name_recognition():
    """Demonstra o funcionamento do sistema de reconhecimento de nomes"""
    
    print("🎯 DEMONSTRAÇÃO: Sistema de Reconhecimento de Nomes")
    print("=" * 60)
    print("Este sistema permite ao BLOB distinguir entre:")
    print("👤 Quando o USUÁRIO se apresenta: 'meu nome é Bruno'")
    print("🤖 Quando o USUÁRIO nomeia o BLOB: 'seu nome é Bob'")
    print("=" * 60)
    
    print("\n📋 CENÁRIOS DE TESTE:")
    
    scenarios = [
        {
            "input": "meu nome é Bruno",
            "expected": "USUÁRIO",
            "description": "Usuário se apresenta"
        },
        {
            "input": "seu nome é Bob", 
            "expected": "BLOB",
            "description": "Usuário nomeia o BLOB"
        },
        {
            "input": "me chamo Ana",
            "expected": "USUÁRIO", 
            "description": "Usuário se apresenta (variação)"
        },
        {
            "input": "você se chama Helper",
            "expected": "BLOB",
            "description": "Usuário nomeia o BLOB (variação)"
        },
        {
            "input": "eu sou Carlos",
            "expected": "USUÁRIO",
            "description": "Usuário se apresenta (variação 2)"
        },
        {
            "input": "te chamo de Buddy",
            "expected": "BLOB", 
            "description": "Usuário nomeia o BLOB (variação 2)"
        }
    ]
    
    def is_user_introduction(text):
        """Detecta apresentação do usuário"""
        text_lower = text.lower()
        patterns = ['meu nome é', 'me chamo', 'sou o', 'sou a', 'eu sou', 'meu nome eh']
        return any(pattern in text_lower for pattern in patterns)
    
    def is_blob_naming(text):
        """Detecta nomeação do BLOB"""
        text_lower = text.lower()
        patterns = ['seu nome é', 'você se chama', 'seu nome eh', 'te chamo de', 'chamar você de']
        return any(pattern in text_lower for pattern in patterns)
    
    print(f"{'Entrada':<25} {'Esperado':<10} {'Detectado':<10} {'Resultado':<10} {'Descrição'}")
    print("-" * 80)
    
    correct = 0
    total = len(scenarios)
    
    for scenario in scenarios:
        text = scenario["input"]
        expected = scenario["expected"]
        description = scenario["description"]
        
        if is_user_introduction(text):
            detected = "USUÁRIO"
        elif is_blob_naming(text):
            detected = "BLOB"
        else:
            detected = "NENHUM"
        
        result = "✅ OK" if detected == expected else "❌ ERRO"
        if detected == expected:
            correct += 1
            
        print(f"{text:<25} {expected:<10} {detected:<10} {result:<10} {description}")
    
    print("-" * 80)
    print(f"📊 RESULTADO: {correct}/{total} cenários corretos ({(correct/total)*100:.1f}%)")
    
    if correct == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O sistema está funcionando perfeitamente!")
    else:
        print("⚠️  Alguns testes falharam. Verificar implementação.")
    
    print("\n🔧 COMO USAR NO BLOB:")
    print("1. Usuário diz: 'meu nome é Bruno'")
    print("   → BLOB detecta como apresentação do usuário")
    print("   → Salva 'Bruno' como user_name no banco")
    print("   → BLOB responde: 'Prazer te conhecer, Bruno!'")
    print("")
    print("2. Usuário diz: 'seu nome é Bob'") 
    print("   → BLOB detecta como nomeação própria")
    print("   → Salva 'Bob' como blob_name no banco")
    print("   → BLOB responde: 'Perfeito! Agora sou Bob!'")
    print("")
    print("3. Posteriormente:")
    print("   → BLOB pode usar: 'Oi Bruno!' (nome do usuário)")
    print("   → BLOB se identifica: 'Meu nome é Bob!' (nome próprio)")

if __name__ == "__main__":
    demo_name_recognition()