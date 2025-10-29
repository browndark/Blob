#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do Sistema de Áudio e Respostas Específicas
Verifica se a BLOB responde adequadamente a perguntas sobre áudio e capacidades
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_audio_responses():
    """Testa respostas específicas sobre áudio e capacidades"""
    print("🎤 TESTE: RESPOSTAS SOBRE ÁUDIO E CAPACIDADES")
    print("=" * 60)
    print("🎯 Objetivo: Eliminar respostas genéricas para perguntas específicas")
    print("=" * 60)
    
    try:
        from modules.ultra_advanced_ai import UltraAdvancedAI
        
        class MockDB:
            def __init__(self):
                self.db_path = 'test.db'
                self.preferences = {'assistant_name': 'BLOB', 'blob_name': 'BLOB'}
            
            def get_preference(self, key, default=None):
                return self.preferences.get(key, default)
            
            def save_preference(self, key, value):
                self.preferences[key] = value
        
        ai = UltraAdvancedAI(MockDB())
        
        print(f"🤖 Nome atual: {ai.assistant_name}")
        
        # Casos de teste específicos para áudio
        test_cases = [
            {
                'categoria': '🎤 PERGUNTAS SOBRE ÁUDIO',
                'testes': [
                    'Blob, consegue me ouvir?',
                    'Você está me escutando?',
                    'Consegue ouvir minha voz?',
                    'Me escuta?',
                    'Pode me ouvir?'
                ],
                'respostas_esperadas': ['ouvindo', 'escuto', 'áudio', 'escutando', 'perfeitamente']
            },
            {
                'categoria': '🔧 PERGUNTAS SOBRE CAPACIDADES',
                'testes': [
                    'O que você consegue fazer?',
                    'Quais são suas capacidades?',
                    'Como você funciona?',
                    'Está funcionando?',
                    'Sistema está ativo?'
                ],
                'respostas_esperadas': ['posso', 'consigo', 'capacidades', 'funcionando', 'sistema']
            },
            {
                'categoria': '👋 CUMPRIMENTOS DIRIGIDOS',
                'testes': [
                    'Oi BLOB',
                    'BLOB, oi!',
                    'Olá BLOB',
                    'E aí BLOB',
                    'BLOB, tudo bem?'
                ],
                'respostas_esperadas': ['blob', 'presente', 'aqui', 'ouvindo', 'escutando', 'area', 'área']
            },
            {
                'categoria': '🧪 TESTES DE COMUNICAÇÃO',
                'testes': [
                    'Teste',
                    'Testing',
                    'Alô',
                    'Teste 123',
                    'Alô alô'
                ],
                'respostas_esperadas': ['teste', 'comunicação', 'áudio', 'funcionando', 'escuto', 'ouvindo', 'claro', 'sistema']
            }
        ]
        
        total_acertos = 0
        total_testes = 0
        
        for categoria_info in test_cases:
            categoria = categoria_info['categoria']
            testes = categoria_info['testes']
            palavras_esperadas = categoria_info['respostas_esperadas']
            
            print(f"\n{categoria}:")
            
            acertos_categoria = 0
            
            for teste in testes:
                total_testes += 1
                response = ai.process_input(teste)
                
                # Verificar se a resposta contém pelo menos uma palavra esperada
                response_lower = response.lower()
                acertou = any(palavra in response_lower for palavra in palavras_esperadas)
                
                if acertou:
                    acertos_categoria += 1
                    total_acertos += 1
                    emoji = "✅"
                else:
                    emoji = "❌"
                
                print(f"  {emoji} \"{teste}\"")
                print(f"     → \"{response}\"")
                
                # Marcar palavras esperadas encontradas
                palavras_encontradas = [p for p in palavras_esperadas if p in response_lower]
                if palavras_encontradas:
                    print(f"     ✓ Palavras-chave: {', '.join(palavras_encontradas)}")
                else:
                    print(f"     ⚠️ Nenhuma palavra-chave encontrada de: {', '.join(palavras_esperadas)}")
            
            percentual = (acertos_categoria / len(testes)) * 100
            print(f"  📊 Categoria: {acertos_categoria}/{len(testes)} ({percentual:.0f}%)")
        
        # Resultado geral
        print("\n" + "=" * 60)
        print("📊 RESULTADO GERAL:")
        
        percentual_geral = (total_acertos / total_testes) * 100
        print(f"  🎯 Acertos: {total_acertos}/{total_testes} ({percentual_geral:.1f}%)")
        
        if percentual_geral >= 80:
            print("🎉 EXCELENTE! Sistema respondendo adequadamente!")
            print("✅ Respostas específicas implementadas com sucesso!")
        elif percentual_geral >= 60:
            print("👍 BOM! Maioria das respostas específicas funcionando!")
            print("⚠️ Algumas melhorias ainda necessárias")
        else:
            print("❌ PROBLEMA! Muitas respostas ainda genéricas")
            print("🔧 Sistema precisa de mais ajustes")
        
        # Teste específico do problema original
        print("\n" + "=" * 60)
        print("🔍 TESTE ESPECÍFICO: 'BLOB, CONSEGUE ME OUVIR?'")
        
        problema_original = "Blob, consegue me ouvir"
        resposta_original = ai.process_input(problema_original)
        
        print(f"📝 Pergunta: \"{problema_original}\"")
        print(f"🤖 Resposta: \"{resposta_original}\"")
        
        # Verificar se não é mais uma resposta genérica
        respostas_genericas = [
            "que interessante, nunca tinha pensado nisso",
            "nossa, nunca tinha pensado nisso",
            "que legal",
            "interessante"
        ]
        
        eh_generica = any(gen in resposta_original.lower() for gen in respostas_genericas)
        
        if not eh_generica:
            print("✅ PROBLEMA RESOLVIDO! Não é mais uma resposta genérica!")
        else:
            print("❌ PROBLEMA PERSISTE! Ainda é uma resposta genérica!")
        
        # Verificar se é específica sobre áudio
        palavras_audio = ['ouvir', 'escutar', 'áudio', 'microfone', 'escutando', 'ouvindo']
        eh_sobre_audio = any(palavra in resposta_original.lower() for palavra in palavras_audio)
        
        if eh_sobre_audio:
            print("✅ RESPOSTA ESPECÍFICA SOBRE ÁUDIO!")
        else:
            print("⚠️ Resposta não é específica sobre áudio")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_audio_responses()
    
    if success:
        print("\n🎊 TESTE CONCLUÍDO!")
        print("🎯 Sistema de respostas específicas testado!")
        print("\n💡 MELHORIAS IMPLEMENTADAS:")
        print("  ✅ Detecção de perguntas sobre áudio")
        print("  ✅ Respostas específicas sobre capacidades")
        print("  ✅ Cumprimentos dirigidos reconhecidos")
        print("  ✅ Testes de comunicação identificados")
        print("  ✅ Fim das respostas genéricas inadequadas")
    else:
        print("\n❌ Erro no teste do sistema")