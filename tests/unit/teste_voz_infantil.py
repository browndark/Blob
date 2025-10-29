#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para a nova voz infantil fluida
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_child_voice():
    """Testa a nova configuração de voz infantil"""
    print("=== TESTE: VOZ INFANTIL FLUIDA ===")
    
    try:
        from core.blob_ultra_avancado import MemoryDatabase, EmotionalAI, VozUltraAvancada
        
        # Criar instâncias de teste
        db = MemoryDatabase()
        emotional_ai = EmotionalAI(db)
        
        # Criar um mock simples para o BLOB
        class MockBLOB:
            pass
        
        class MockApp:
            def update_conversation(self, text):
                pass
        
        mock_blob = MockBLOB()
        mock_app = MockApp()
        
        # Criar sistema de voz
        voz = VozUltraAvancada(mock_blob, mock_app, db, emotional_ai)
        
        print("✅ Sistema de voz infantil carregado!")
        
        # Teste de frases infantis
        frases_teste = [
            "Oi! Eu sou a Bianca e agora tenho uma voz mais fofa!",
            "Que legal te conhecer! Vamos ser amigos?",
            "Puxa, que pergunta interessante! Deixe-me pensar...",
            "Yay! Adoro quando você fala comigo!",
            "Hmm... isso é muito legal mesmo!"
        ]
        
        print("\n🎈 Testando frases com voz infantil:")
        for i, frase in enumerate(frases_teste, 1):
            print(f"\n{i}. Testando: '{frase}'")
            voz.speak(frase)
            input("  Pressione Enter para próxima frase...")
        
        print("\n=== TESTE DE VOZ INFANTIL CONCLUÍDO ===")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_child_voice()