#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE DIRETO DA VOZ - BLOB Ultra Avançado
Testa apenas o sistema de voz sem interface
"""

import sys
sys.path.append(".")

def teste_voz_direta():
    """Teste direto da função speak"""
    print("🔊 TESTE DIRETO DA VOZ")
    print("=" * 30)
    
    try:
        # Importar apenas a classe necessária
        from blob_ultra_avancado import VozUltraAvancada
        import pyttsx3
        
        # Classe mock mínima
        class MockApp:
            def update_voice_status(self, status):
                print(f"Status: {status}")
            def update_conversation(self, text):
                print(f"Conversa: {text}")
        
        class MockBlob:
            def __init__(self):
                self.current_emotion = "neutro"
                self.mood_level = 70
        
        class MockMemory:
            def get_preference(self, key, default=None):
                return default
            def save_preference(self, key, value):
                pass
            def get_relationship_metric(self, key, default=0.0):
                return default
        
        class MockAI:
            def analyze_user_emotion(self, text):
                return {"dominant_emotion": "neutral"}
        
        # Criar instâncias mock
        app = MockApp()
        blob = MockBlob()
        memory = MockMemory()
        ai = MockAI()
        
        print("1. Criando sistema de voz...")
        voz = VozUltraAvancada(blob, app, memory, ai)
        
        if not voz.enabled:
            print("❌ Sistema de voz não habilitado!")
            return False
        
        print("2. Testando fala direta...")
        voz.speak("Olá! Este é um teste direto da voz do BLOB!")
        
        print("3. Testando segunda fala...")
        voz.speak("Se você está ouvindo isso, a voz está funcionando perfeitamente!")
        
        print("✅ Teste concluído!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = teste_voz_direta()
    if sucesso:
        print("🎉 Voz funcionando!")
    else:
        print("❌ Problemas na voz!")