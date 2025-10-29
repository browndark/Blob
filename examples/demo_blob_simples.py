#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstração Simples - BLOB Ultra Avançado
Para testar se o sistema de voz melhorado está funcionando
"""

import time
from blob_ultra_avancado import VozUltraAvancada, BLOBUltraAvancado, MemoryDatabase, EmotionalAI
import tkinter as tk

def demo_blob_voz():
    """Demonstração das capacidades de voz do BLOB"""
    print("🎭 DEMONSTRAÇÃO DO BLOB ULTRA AVANÇADO")
    print("=" * 50)
    
    # Configurar interface mínima
    root = tk.Tk()
    root.title("Demo BLOB")
    root.geometry("400x400")
    root.configure(bg='#161B22')
    
    canvas = tk.Canvas(root, width=400, height=400, bg='#161B22')
    canvas.pack()
    
    # Criar sistemas
    memory_db = MemoryDatabase()
    emotional_ai = EmotionalAI(memory_db)
    blob = BLOBUltraAvancado(canvas, x=200, y=200)
    
    # Criar app mock simples
    class AppMock:
        def __init__(self):
            self.root = root
            
        def update_voice_status(self, status):
            print(f"Status: {status}")
            
        def update_mic_button_state(self, state):
            print(f"Mic: {'ON' if state else 'OFF'}")
    
    app_mock = AppMock()
    
    # Sistema de voz
    voz = VozUltraAvancada(blob, app_mock, memory_db, emotional_ai)
    
    if not voz.enabled:
        print("❌ Sistema de voz não disponível!")
        return
    
    print("✅ Sistema inicializado!")
    print("\n🎤 Demonstração de capacidades:")
    
    # Teste 1: Saudação
    print("\n1. Saudação:")
    voz.speak("Olá! Eu sou o BLOB Ultra Avançado!")
    time.sleep(2)
    
    # Teste 2: Personalidade
    print("2. Demonstração de personalidade:")
    voz.speak("Sou seu assistente virtual inteligente com busca na internet!")
    time.sleep(3)
    
    # Teste 3: Busca simulada
    print("3. Teste de busca na web:")
    voz.speak("Posso pesquisar qualquer coisa na internet para você!")
    time.sleep(2)
    
    # Teste de pergunta
    pergunta_teste = "Por que o céu é azul?"
    print(f"4. Respondendo: {pergunta_teste}")
    
    resposta = voz.process_voice_ultra(pergunta_teste, "curious")
    time.sleep(1)
    
    print("\n🎉 Demonstração concluída!")
    print("Se você ouviu todas as falas, o sistema está perfeito!")
    
    # Fechar depois de um tempo
    def fechar():
        print("Fechando demonstração...")
        root.quit()
    
    root.after(2000, fechar)  # Fechar após 2 segundos
    root.mainloop()

if __name__ == "__main__":
    try:
        demo_blob_voz()
    except Exception as e:
        print(f"Erro na demonstração: {e}")
        import traceback
        traceback.print_exc()