#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE FORÇA BRUTA - TODOS OS MÉTODOS DE TTS
Testa TODOS os métodos possíveis para fazer som sair
"""

import subprocess
import tempfile
import os
import time

def teste_todos_metodos():
    """Testa todos os métodos de TTS disponíveis"""
    print("🔊 TESTE FORÇA BRUTA - TODOS OS MÉTODOS")
    print("=" * 50)
    
    texto_teste = "Teste de áudio - você consegue me ouvir?"
    
    # MÉTODO 1: PowerShell direto
    print("\n1. Testando PowerShell direto...")
    try:
        ps_command = f'''
        Add-Type -AssemblyName System.Speech
        $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $synth.Volume = 100
        $synth.Rate = -2
        $synth.Speak("{texto_teste}")
        '''
        
        print("🔊 Executando PowerShell...")
        result = subprocess.run(['powershell', '-Command', ps_command], 
                               capture_output=False, timeout=15)
        print(f"✅ PowerShell concluído (código: {result.returncode})")
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ PowerShell falhou: {e}")
    
    # MÉTODO 2: Windows SAPI via COM
    print("\n2. Testando Windows SAPI...")
    try:
        import win32com.client
        
        print("🔊 Criando objeto SAPI...")
        sapi = win32com.client.Dispatch("SAPI.SpVoice")
        sapi.Volume = 100
        sapi.Rate = 0
        
        print("🔊 Falando via SAPI...")
        sapi.Speak(texto_teste)
        print("✅ SAPI concluído!")
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ SAPI falhou: {e}")
    
    # MÉTODO 3: VBScript
    print("\n3. Testando VBScript...")
    try:
        vbs_content = f'''
        Set speech = CreateObject("SAPI.SpVoice")
        speech.Volume = 100
        speech.Rate = 0
        speech.Speak "{texto_teste}"
        '''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vbs', delete=False) as f:
            f.write(vbs_content)
            vbs_file = f.name
        
        print("🔊 Executando VBScript...")
        os.system(f'cscript //nologo "{vbs_file}"')
        os.unlink(vbs_file)
        print("✅ VBScript concluído!")
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ VBScript falhou: {e}")
    
    # MÉTODO 4: pyttsx3 forçado
    print("\n4. Testando pyttsx3 forçado...")
    try:
        import pyttsx3
        
        print("🔊 Criando engine pyttsx3...")
        engine = pyttsx3.init('sapi5')
        engine.setProperty('rate', 120)
        engine.setProperty('volume', 1.0)
        
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
            print(f"Voz: {voices[0].name}")
        
        print("🔊 Falando via pyttsx3...")
        engine.say(texto_teste)
        engine.runAndWait()
        engine.stop()
        del engine
        print("✅ pyttsx3 concluído!")
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ pyttsx3 falhou: {e}")
    
    print("\n🎯 TESTE CONCLUÍDO!")
    print("Se você NÃO ouviu NENHUM método:")
    print("- O problema é hardware/configuração do sistema")
    print("- Verifique volume, drivers, dispositivos de áudio")

if __name__ == "__main__":
    teste_todos_metodos()