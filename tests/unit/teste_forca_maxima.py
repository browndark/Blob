#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE FORÇA MÁXIMA DA VOZ
Testa todos os métodos possíveis de áudio
"""

import pyttsx3
import os
import time

def teste_forca_maxima():
    """Teste com força máxima"""
    print("🔊 TESTE FORÇA MÁXIMA DA VOZ")
    print("=" * 40)
    
    # TESTE 1: pyttsx3 padrão
    print("\n1. Testando pyttsx3 padrão...")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'maria' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                print(f"Voz: {voice.name}")
                break
        
        print("🔊 FALANDO: Teste um - você consegue me ouvir?")
        engine.say("Teste um - você consegue me ouvir?")
        engine.runAndWait()
        time.sleep(1)
        
        del engine
        print("✅ Teste 1 concluído")
    except Exception as e:
        print(f"❌ Erro teste 1: {e}")
    
    # TESTE 2: Nova engine
    print("\n2. Testando nova engine...")
    try:
        engine2 = pyttsx3.init()
        engine2.setProperty('rate', 120)  # Mais devagar
        engine2.setProperty('volume', 1.0)
        
        print("🔊 FALANDO: Teste dois - consigo ser ouvido agora?")
        engine2.say("Teste dois - consigo ser ouvido agora?")
        engine2.runAndWait()
        time.sleep(1)
        
        del engine2
        print("✅ Teste 2 concluído")
    except Exception as e:
        print(f"❌ Erro teste 2: {e}")
    
    # TESTE 3: PowerShell como backup
    print("\n3. Testando PowerShell TTS...")
    try:
        print("🔊 FALANDO: Teste três via PowerShell")
        cmd = 'powershell -Command "Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak(\'Teste três via PowerShell - você me ouve?\')"'
        os.system(cmd)
        time.sleep(1)
        print("✅ Teste 3 concluído")
    except Exception as e:
        print(f"❌ Erro teste 3: {e}")
    
    print("\n🎯 TESTE CONCLUÍDO!")
    print("Se você NÃO ouviu NENHUM dos testes:")
    print("- Verifique o volume do sistema")
    print("- Conecte fones de ouvido")
    print("- Verifique se o áudio não está mutado")

if __name__ == "__main__":
    teste_forca_maxima()