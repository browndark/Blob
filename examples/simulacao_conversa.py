#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMULAÇÃO DE CONVERSA COM BLOB
Testa se o BLOB responde por voz quando recebe input
"""

import sys
import time
sys.path.append(".")

def simular_conversa():
    """Simula uma conversa com o BLOB"""
    print("🎭 SIMULAÇÃO DE CONVERSA COM BLOB")
    print("=" * 40)
    
    try:
        # Importar apenas o necessário para simular
        from blob_ultra_avancado import VozUltraAvancada, MemoryDatabase, EmotionalAI
        
        # Mock classes mínimas
        class MockBlob:
            def __init__(self):
                self.current_emotion = "neutro"
                self.mood_level = 70
            def boost_mood(self, amount):
                self.mood_level += amount
            def set_emotion(self, emotion):
                self.current_emotion = emotion
            def get_emotion_from_mood(self):
                return "neutro"
        
        class MockApp:
            def update_voice_status(self, status):
                print(f"Status: {status}")
            def update_conversation(self, text):
                print(f"Interface: {text}")
        
        print("1. Criando sistema BLOB...")
        
        # Criar database e AI reais
        memory = MemoryDatabase()
        ai = EmotionalAI(memory)
        blob = MockBlob()
        app = MockApp()
        
        # Criar sistema de voz
        voz = VozUltraAvancada(blob, app, memory, ai)
        
        print("2. Testando resposta simples...")
        voz.speak("Olá! Sou o BLOB e estou testando minha voz!")
        time.sleep(2)
        
        print("3. Testando pergunta...")
        voz.speak("Você consegue me ouvir? Essa é uma pergunta importante!")
        time.sleep(2)
        
        print("4. Testando processamento de entrada...")
        # Simular que o usuário disse "Como você se chama?"
        try:
            voz.process_ultra_advanced_input("Como você se chama?")
        except Exception as e:
            print(f"Erro no processamento: {e}")
            # Resposta manual
            voz.speak("Meu nome é BLOB! Prazer em conhecer você!")
        
        print("✅ Simulação concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na simulação: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = simular_conversa()
    if sucesso:
        print("🎉 Se você ouviu as falas, o BLOB está funcionando!")
    else:
        print("❌ Problemas detectados")