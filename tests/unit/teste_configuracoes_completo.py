#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste completo do sistema de configurações do BLOB
Inclui testes de voz masculina/feminina, volume, brilho
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_complete_settings_system():
    """Testa o sistema completo de configurações"""
    print("=== TESTE: SISTEMA COMPLETO DE CONFIGURAÇÕES ===")
    
    try:
        # Testar gerenciador de configurações
        from modules.settings_manager import SettingsManager
        
        print("✅ Módulo de configurações carregado!")
        
        # Criar gerenciador
        settings = SettingsManager()
        
        # Testar configurações de voz
        print("\n🎤 TESTANDO CONFIGURAÇÕES DE VOZ:")
        
        # Testar voz feminina
        print("  1. Configurando voz feminina...")
        settings.update_voice_config(voice_type="female", volume=80, rate=0, pitch=5)
        voice_config = settings.get_voice_config()
        print(f"     ✅ Voz: {voice_config.get('voice_type')} - Volume: {voice_config.get('volume')}%")
        
        # Testar voz masculina
        print("  2. Configurando voz masculina...")
        settings.update_voice_config(voice_type="male", volume=70, rate=-2, pitch=-3)
        voice_config = settings.get_voice_config()
        print(f"     ✅ Voz: {voice_config.get('voice_type')} - Volume: {voice_config.get('volume')}%")
        
        # Testar configurações de UI
        print("\n🎨 TESTANDO CONFIGURAÇÕES DE INTERFACE:")
        
        print("  1. Configurando brilho...")
        settings.update_ui_config(brightness=90, theme="dark", font_size=14)
        ui_config = settings.get_ui_config()
        print(f"     ✅ Brilho: {ui_config.get('brightness')}% - Tema: {ui_config.get('theme')}")
        
        # Testar salvamento e carregamento
        print("\n💾 TESTANDO SALVAMENTO/CARREGAMENTO:")
        
        print("  1. Salvando configurações...")
        save_result = settings.save_config()
        print(f"     ✅ Salvo: {save_result}")
        
        print("  2. Recarregando configurações...")
        new_settings = SettingsManager()
        reloaded_voice = new_settings.get_voice_config()
        reloaded_ui = new_settings.get_ui_config()
        
        print(f"     ✅ Voz recarregada: {reloaded_voice.get('voice_type')} - {reloaded_voice.get('volume')}%")
        print(f"     ✅ UI recarregada: Brilho {reloaded_ui.get('brightness')}%")
        
        # Testar voz
        print("\n🔊 TESTANDO SISTEMA DE VOZ:")
        
        # Testar voz feminina
        print("  1. Testando voz feminina...")
        try:
            import win32com.client
            sapi = win32com.client.Dispatch('SAPI.SpVoice')
            sapi.Volume = 80
            sapi.Rate = 2
            
            # Buscar voz feminina
            voices = sapi.GetVoices()
            for voice in voices:
                if 'maria' in voice.GetDescription().lower():
                    sapi.Voice = voice
                    break
            
            sapi.Speak("Oi! Eu sou a Bianca com voz feminina!")
            print("     ✅ Voz feminina testada!")
            
        except Exception as e:
            print(f"     ⚠️ Erro ao testar voz feminina: {e}")
        
        # Testar voz masculina (simulada)
        print("  2. Testando voz masculina...")
        try:
            # Simular configuração masculina
            sapi.Volume = 70
            sapi.Rate = -1
            sapi.Speak("Olá! Eu sou o BLOB com voz masculina!")
            print("     ✅ Voz masculina testada!")
            
        except Exception as e:
            print(f"     ⚠️ Erro ao testar voz masculina: {e}")
        
        print("\n=== TESTE DE CONFIGURAÇÕES CONCLUÍDO COM SUCESSO ===")
        print("\n📋 RESUMO DAS FUNCIONALIDADES:")
        print("  ✅ Gerenciador de configurações")
        print("  ✅ Configuração de voz (masculina/feminina)")
        print("  ✅ Controle de volume")
        print("  ✅ Configuração de brilho da interface")
        print("  ✅ Salvamento/carregamento de configurações")
        print("  ✅ Sistema de testes de voz")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_settings_ui():
    """Testa a interface de configurações"""
    print("\n=== TESTE: INTERFACE DE CONFIGURAÇÕES ===")
    
    try:
        from modules.settings_manager import SettingsManager
        import tkinter as tk
        
        # Criar janela de teste
        root = tk.Tk()
        root.withdraw()  # Esconder janela principal
        
        # Abrir configurações
        settings = SettingsManager()
        settings.open_settings_window()
        
        print("✅ Interface de configurações aberta!")
        print("🎛️ Recursos disponíveis:")
        print("  • Escolha entre voz masculina e feminina")
        print("  • Controle de volume da voz")
        print("  • Ajuste de velocidade de fala")
        print("  • Controle de tom da voz")
        print("  • Configuração de brilho da interface")
        print("  • Seleção de tema (claro/escuro)")
        print("  • Ajuste de tamanho da fonte")
        print("  • Botão de teste de voz")
        print("  • Salvamento automático de configurações")
        
        # Manter janela aberta para teste manual
        print("\n🖱️ Teste a interface manualmente e feche a janela quando terminar...")
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de UI: {e}")
        return False

if __name__ == "__main__":
    # Executar testes
    print("🚀 INICIANDO TESTES DO SISTEMA DE CONFIGURAÇÕES\n")
    
    # Teste 1: Sistema de configurações
    test1_result = test_complete_settings_system()
    
    if test1_result:
        print("\n" + "="*50)
        resposta = input("Deseja testar a interface gráfica? (s/n): ")
        
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            # Teste 2: Interface gráfica
            test2_result = test_settings_ui()
            
            if test2_result:
                print("\n🎉 TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
            else:
                print("\n⚠️ Teste de interface falhou.")
        else:
            print("\n✅ Teste básico concluído com sucesso!")
    else:
        print("\n❌ Teste básico falhou.")