#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNÓSTICO COMPLETO DE ÁUDIO
Verifica configurações de áudio do sistema
"""

import subprocess
import json

def diagnostico_audio():
    """Diagnóstico completo do sistema de áudio"""
    print("🔍 DIAGNÓSTICO COMPLETO DE ÁUDIO")
    print("=" * 40)
    
    # 1. Verificar dispositivos de áudio
    print("\n1. Verificando dispositivos de áudio...")
    try:
        # PowerShell para listar dispositivos de áudio
        ps_cmd = '''
        Get-WmiObject -Class Win32_SoundDevice | Select-Object Name, Status | ConvertTo-Json
        '''
        result = subprocess.run(['powershell', '-Command', ps_cmd], 
                               capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            devices = json.loads(result.stdout)
            if isinstance(devices, list):
                for device in devices:
                    print(f"   📱 {device['Name']} - Status: {device['Status']}")
            else:
                print(f"   📱 {devices['Name']} - Status: {devices['Status']}")
        else:
            print("   ❌ Não foi possível listar dispositivos")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # 2. Verificar volume do sistema
    print("\n2. Verificando volume do sistema...")
    try:
        ps_cmd = '''
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        public class Audio {
            [DllImport("winmm.dll")]
            public static extern int waveOutGetVolume(IntPtr hwo, out uint dwVolume);
        }
"@
        [Audio]::waveOutGetVolume([IntPtr]::Zero, [ref]$volume)
        $left = [int]($volume -band 0xFFFF)
        $right = [int](($volume -shr 16) -band 0xFFFF)
        "Volume: L=$left R=$right"
        '''
        result = subprocess.run(['powershell', '-Command', ps_cmd], 
                               capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"   🔊 {result.stdout.strip()}")
        else:
            print("   ❓ Não foi possível verificar volume")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # 3. Teste com beep do sistema
    print("\n3. Testando beep do sistema...")
    try:
        import winsound
        print("   🔔 Tocando beep...")
        winsound.Beep(1000, 500)  # 1000Hz por 500ms
        print("   ✅ Beep executado!")
        
    except Exception as e:
        print(f"   ❌ Erro no beep: {e}")
    
    # 4. Teste final com TTS simples
    print("\n4. Teste final de TTS...")
    try:
        import win32com.client
        sapi = win32com.client.Dispatch("SAPI.SpVoice")
        
        # Listar vozes disponíveis
        voices = sapi.GetVoices()
        print(f"   🗣️ Vozes disponíveis: {voices.Count}")
        
        for i in range(voices.Count):
            voice = voices.Item(i)
            print(f"      - {voice.GetDescription()}")
        
        # Falar com volume máximo
        sapi.Volume = 100
        sapi.Rate = 0
        print("   🔊 Falando: 'Este é o teste final de áudio'")
        sapi.Speak("Este é o teste final de áudio")
        
        print("   ✅ TTS executado!")
        
    except Exception as e:
        print(f"   ❌ Erro no TTS: {e}")
    
    print("\n📋 CHECKLIST DE DIAGNÓSTICO:")
    print("□ Verifique se alto-falantes estão conectados")
    print("□ Verifique se o volume do Windows está > 50%")
    print("□ Verifique se não está mutado (ícone do som)")
    print("□ Teste com fones de ouvido")
    print("□ Verifique se outros programas fazem som")
    print("□ Reinicie o serviço de áudio do Windows")

if __name__ == "__main__":
    diagnostico_audio()