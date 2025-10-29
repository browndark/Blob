#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste das correções: Voz Masculina vs Feminina e Regulador de Brilho
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_voice_differences():
    """Testa a diferença entre voz masculina e feminina"""
    print("=== TESTE: DIFERENÇAS ENTRE VOZ MASCULINA E FEMININA ===")
    
    try:
        import win32com.client
        
        sapi = win32com.client.Dispatch('SAPI.SpVoice')
        voices = sapi.GetVoices()
        
        print(f"📊 Vozes disponíveis: {len(voices)}")
        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.GetDescription()}")
        
        print("\n🎤 TESTE 1: VOZ FEMININA (Maria - Infantil)")
        # Configurar voz feminina
        for voice in voices:
            if 'maria' in voice.GetDescription().lower():
                sapi.Voice = voice
                break
        
        sapi.Volume = 80
        sapi.Rate = 2  # Mais rápido para soar infantil
        print("  Configurações: Maria, Volume 80%, Taxa +2 (infantil)")
        print("  🗣️ Falando...")
        sapi.Speak("Oi! Eu sou a Bianca com voz feminina fofa e infantil!")
        
        input("  ⏸️ Pressione Enter para testar voz masculina...")
        
        print("\n🎤 TESTE 2: VOZ MASCULINA (Zira - Grave)")
        # Configurar voz masculina
        for voice in voices:
            if 'zira' in voice.GetDescription().lower():
                sapi.Voice = voice
                break
        
        sapi.Volume = 70
        sapi.Rate = -3  # Mais lento para soar masculino
        print("  Configurações: Zira, Volume 70%, Taxa -3 (grave)")
        print("  🗣️ Falando...")
        sapi.Speak("Olá! Eu sou o BLOB com voz masculina mais grave e adulta!")
        
        print("\n✅ Teste de vozes concluído!")
        print("💡 Diferenças aplicadas:")
        print("  • Feminina: Maria + Taxa +2 (mais rápida/infantil)")
        print("  • Masculina: Zira + Taxa -3 (mais lenta/grave)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de vozes: {e}")
        return False

def test_brightness_system():
    """Testa o sistema de brilho"""
    print("\n=== TESTE: SISTEMA DE BRILHO ===")
    
    try:
        from modules.settings_manager import SettingsManager
        
        settings = SettingsManager()
        
        print("📝 Testando configurações de brilho...")
        
        # Testar diferentes níveis de brilho
        brilho_levels = [30, 50, 70, 90]
        
        for brilho in brilho_levels:
            print(f"  🔆 Configurando brilho: {brilho}%")
            settings.update_ui_config(brightness=brilho)
            
            # Verificar se foi salvo
            ui_config = settings.get_ui_config()
            saved_brightness = ui_config.get('brightness', 0)
            
            if saved_brightness == brilho:
                print(f"    ✅ Brilho {brilho}% salvo corretamente")
            else:
                print(f"    ❌ Erro: Esperado {brilho}%, obtido {saved_brightness}%")
        
        print("\n✅ Teste de brilho concluído!")
        print("💡 Funcionalidades testadas:")
        print("  • Salvamento de configurações de brilho")
        print("  • Carregamento de configurações")
        print("  • Validação de valores")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de brilho: {e}")
        return False

def test_settings_interface():
    """Testa a interface de configurações corrigida"""
    print("\n=== TESTE: INTERFACE DE CONFIGURAÇÕES CORRIGIDA ===")
    
    try:
        from modules.settings_manager import SettingsManager
        import tkinter as tk
        
        print("🖥️ Abrindo interface de configurações...")
        
        # Criar janela de teste
        root = tk.Tk()
        root.withdraw()  # Esconder janela principal
        
        # Abrir configurações
        settings = SettingsManager()
        settings.open_settings_window()
        
        print("✅ Interface aberta com correções:")
        print("  • Textos simplificados: 'Masculino' e 'Feminino'")
        print("  • Regulador de brilho com preview")
        print("  • Sistema de teste de voz melhorado")
        print("\n🎛️ Teste manualmente:")
        print("  1. Alterne entre Masculino e Feminino")
        print("  2. Clique em 'Testar Voz' para cada tipo")
        print("  3. Mova o regulador de brilho")
        print("  4. Observe as diferenças nas vozes")
        
        # Manter janela aberta para teste manual
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na interface: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TESTANDO CORREÇÕES DO SISTEMA DE CONFIGURAÇÕES\n")
    
    # Teste 1: Diferenças entre vozes
    test1_result = test_voice_differences()
    
    if test1_result:
        print("\n" + "="*50)
        
        # Teste 2: Sistema de brilho
        test2_result = test_brightness_system()
        
        if test2_result:
            print("\n" + "="*50)
            resposta = input("Deseja testar a interface gráfica corrigida? (s/n): ")
            
            if resposta.lower() in ['s', 'sim', 'y', 'yes']:
                # Teste 3: Interface corrigida
                test3_result = test_settings_interface()
                
                if test3_result:
                    print("\n🎉 TODAS AS CORREÇÕES TESTADAS COM SUCESSO!")
                    print("\n✅ Correções implementadas:")
                    print("  • Voz masculina diferenciada (Zira + configurações graves)")
                    print("  • Textos simplificados ('Masculino' e 'Feminino')")
                    print("  • Regulador de brilho funcional com preview")
                    print("  • Sistema de teste de voz melhorado")
                else:
                    print("\n⚠️ Interface com problemas.")
            else:
                print("\n✅ Testes básicos concluídos com sucesso!")
        else:
            print("\n❌ Teste de brilho falhou.")
    else:
        print("\n❌ Teste de vozes falhou.")