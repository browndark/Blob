#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE SUPER SIMPLES DA VOZ
Testa apenas o pyttsx3 diretamente
"""

import pyttsx3
import time

def teste_voz_simples():
    """Teste básico do pyttsx3"""
    print("🔊 TESTE SIMPLES DA VOZ")
    print("=" * 30)
    
    try:
        print("1. Inicializando engine...")
        engine = pyttsx3.init()
        
        print("2. Configurando voz...")
        voices = engine.getProperty('voices')
        
        # Procurar voz brasileira
        for voice in voices:
            if 'maria' in voice.name.lower() or 'brazil' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                print(f"✅ Voz brasileira encontrada: {voice.name}")
                break
        
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 0.9)
        
        print("3. Testando fala 1...")
        engine.say("Olá! Este é um teste simples da voz!")
        engine.runAndWait()
        
        print("4. Testando fala 2...")
        engine.say("Se você está ouvindo isso, a voz está funcionando!")
        engine.runAndWait()
        
        print("5. Testando fala 3...")
        engine.say("O sistema de voz do BLOB está perfeito!")
        engine.runAndWait()
        
        print("✅ Teste concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    sucesso = teste_voz_simples()
    if sucesso:
        print("🎉 VOZ FUNCIONANDO PERFEITAMENTE!")
    else:
        print("❌ Problemas na voz!")