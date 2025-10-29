#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE ESPECÍFICO - PERGUNTAS SOBRE NOME
Testa se o BLOB responde corretamente quando perguntamos seu nome
"""

import sys
sys.path.append(".")

def teste_perguntas_nome():
    """Testa diferentes formas de perguntar o nome"""
    print("🧪 TESTE ESPECÍFICO - PERGUNTAS SOBRE NOME")
    print("=" * 45)
    
    try:
        # Imports necessários
        from blob_ultra_avancado import VozUltraAvancada, MemoryDatabase, EmotionalAI
        
        # Mock classes
        class MockBlob:
            def __init__(self):
                self.current_emotion = "neutro"
                self.mood_level = 70
            def boost_mood(self, amount):
                self.mood_level += amount
        
        class MockApp:
            def update_voice_status(self, status):
                print(f"Status: {status}")
            def update_conversation(self, text):
                print(f"Interface: {text}")
        
        print("1. Criando sistema...")
        memory = MemoryDatabase()
        ai = EmotionalAI(memory)
        blob = MockBlob()
        app = MockApp()
        
        # Definir nome para teste
        memory.save_preference('blob_name', 'Bob')
        
        voz = VozUltraAvancada(blob, app, memory, ai)
        
        print(f"Nome salvo: {voz.blob_name}")
        
        # Lista de perguntas para testar
        perguntas = [
            "Qual é seu nome?",
            "Como você se chama?",
            "Qual seu nome?",
            "Me diz seu nome",
            "Como se chama?",
            "Seu nome é?",
            "Qual o seu nome?"
        ]
        
        print("\n2. Testando perguntas sobre nome...")
        for i, pergunta in enumerate(perguntas, 1):
            print(f"\n--- TESTE {i}: '{pergunta}' ---")
            
            # Verificar se detecta como pergunta sobre status/nome
            is_status = voz._is_asking_about_status(pergunta.lower())
            print(f"Detectou como pergunta sobre status: {is_status}")
            
            if is_status:
                # Simular resposta
                voz._respond_about_status_ultra({"dominant_emotion": "neutral"}, pergunta.lower())
            else:
                print("❌ NÃO detectou como pergunta sobre nome!")
        
        print("\n✅ Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    teste_perguntas_nome()