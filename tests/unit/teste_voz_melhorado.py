#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste das Melhorias do Sistema de Voz - BLOB Ultra Avançado
Verifica se as correções da voz estão funcionando corretamente
"""

import sys
import time
from blob_ultra_avancado import AppUltraAvancada

def teste_voz_completo():
    """Teste completo das funcionalidades de voz"""
    print("🧪 TESTE DAS MELHORIAS DO SISTEMA DE VOZ")
    print("=" * 50)
    
    try:
        # Inicializar app
        print("1. Inicializando BLOB Ultra Avançado...")
        app = AppUltraAvancada()
        
        # Aguardar inicialização
        time.sleep(2)
        
        # Teste 1: Verificar se a voz está configurada
        print("\n2. Testando configuração da voz...")
        voice_system = app.voice_system
        
        if voice_system.enabled:
            print("✅ Sistema de voz ATIVADO")
            
            # Teste básico de fala
            print("3. Teste básico de fala...")
            voice_system.speak("Olá! Este é um teste do sistema de voz melhorado!")
            time.sleep(3)
            
            # Teste de pergunta que requer busca
            print("4. Teste de busca com resposta em voz...")
            voice_system.speak("Agora vou pesquisar algo na internet para você!")
            time.sleep(2)
            
            # Simular pergunta
            pergunta = "Por que o céu é azul?"
            print(f"Pergunta de teste: {pergunta}")
            
            # Processar resposta (simula o que acontece no app real)
            response_text = voice_system.process_voice_ultra(pergunta, "neutral")
            print(f"Resposta processada: {response_text[:100]}...")
            
            print("\n5. Teste de robustez da voz...")
            # Testar múltiplas falas seguidas
            for i in range(3):
                voice_system.speak(f"Teste número {i+1} - verificando consistência da voz")
                time.sleep(1)
            
            print("✅ TESTE CONCLUÍDO - Verifique se você ouviu todas as falas!")
            voice_system.speak("Teste de voz concluído! Se você está ouvindo isso, o sistema está funcionando perfeitamente!")
            
        else:
            print("❌ Sistema de voz DESATIVADO")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False
    
    return True

def teste_rapido_voz():
    """Teste rápido apenas da voz"""
    print("🔊 Teste Rápido de Voz")
    print("-" * 30)
    
    try:
        import pyttsx3
        
        # Teste direto do pyttsx3
        print("Testando pyttsx3 diretamente...")
        engine = pyttsx3.init()
        
        # Configurar voz em português se disponível
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'brazil' in voice.name.lower() or 'portuguese' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        # Configurar velocidade e volume
        engine.setProperty('rate', 200)
        engine.setProperty('volume', 0.9)
        
        print("✅ Engine inicializada")
        print("🔊 Falando teste...")
        
        engine.say("Olá! Este é um teste rápido da voz!")
        engine.runAndWait()
        
        engine.say("Se você está ouvindo isso, a voz está funcionando!")
        engine.runAndWait()
        
        print("✅ Teste rápido concluído")
        return True
            
    except Exception as e:
        print(f"❌ Erro no teste rápido: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTE DE MELHORIAS DO SISTEMA DE VOZ")
    print("="*50)
    
    # Escolher tipo de teste
    print("Escolha o tipo de teste:")
    print("1. Teste Completo (com app completo)")
    print("2. Teste Rápido (só voz)")
    
    try:
        escolha = input("Digite 1 ou 2: ").strip()
        
        if escolha == "1":
            sucesso = teste_voz_completo()
        elif escolha == "2":
            sucesso = teste_rapido_voz()
        else:
            print("Executando teste rápido por padrão...")
            sucesso = teste_rapido_voz()
        
        if sucesso:
            print("\n🎉 TESTE BEM-SUCEDIDO!")
            print("Se você ouviu as falas, o sistema de voz está funcionando!")
        else:
            print("\n❌ TESTE FALHOU")
            print("Verifique os alto-falantes e tente novamente.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")