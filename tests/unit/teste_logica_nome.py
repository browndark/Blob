#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para verificar o reconhecimento do nome do usuário
(Versão simplificada sem GUI)
"""

import sys
import os
import re

def test_user_introduction_logic():
    """Testa apenas a lógica de reconhecimento de nome do usuário"""
    print("=== TESTE DE LÓGICA DE RECONHECIMENTO DE NOME ===")
    
    def simulate_user_introduction(text):
        """Simula a função _handle_user_introduction"""
        text_lower = text.lower()
        
        # Padrões para detectar apresentação do usuário
        introduction_patterns = [
            'meu nome é', 'me chamo', 'sou o', 'sou a', 'eu sou',
            'meu nome eh', 'me chamam de', 'pode me chamar de'
        ]
        
        for pattern in introduction_patterns:
            if pattern in text_lower:
                # Extrai o nome após o padrão
                try:
                    parts = text_lower.split(pattern)
                    if len(parts) > 1:
                        nome_part = parts[1].strip()
                        # Remove pontuação e pega a primeira palavra
                        nome = nome_part.split()[0] if nome_part.split() else ""
                        nome = ''.join(c for c in nome if c.isalpha()).capitalize()
                        
                        if nome and len(nome) > 1:
                            print(f"    ✅ Nome detectado: {nome}")
                            return True, nome
                            
                except Exception as e:
                    print(f"    ❌ Erro: {e}")
        
        return False, None
    
    def simulate_blob_naming(text):
        """Simula a detecção de nomeação do BLOB"""
        text_lower = text.lower()
        
        # Padrões para nomear o BLOB
        blob_patterns = [
            'seu nome é', 'você se chama', 'seu nome eh', 
            'te chamo de', 'chamar você de'
        ]
        
        for pattern in blob_patterns:
            if pattern in text_lower:
                parts = text_lower.split(pattern)
                if len(parts) > 1:
                    nome_part = parts[1].strip()
                    nome = nome_part.split()[0] if nome_part.split() else ""
                    nome = ''.join(c for c in nome if c.isalpha()).capitalize()
                    
                    if nome and len(nome) > 1:
                        print(f"    ✅ Nome do BLOB detectado: {nome}")
                        return True, nome
        
        return False, None
    
    # Testes de apresentação do usuário
    print("\n🧪 TESTES DE APRESENTAÇÃO DO USUÁRIO:")
    user_phrases = [
        "meu nome é Bruno",
        "me chamo Ana", 
        "sou o Carlos",
        "eu sou Maria",
        "pode me chamar de João",
        "meu nome eh Pedro"
    ]
    
    for phrase in user_phrases:
        print(f"\n  Testando: '{phrase}'")
        result, name = simulate_user_introduction(phrase)
        print(f"    Resultado: {result}")
    
    # Testes de nomeação do BLOB
    print("\n🧪 TESTES DE NOMEAÇÃO DO BLOB:")
    blob_phrases = [
        "seu nome é Bob",
        "você se chama Blob",
        "seu nome eh Buddy", 
        "te chamo de Amigo",
        "chamar você de Helper"
    ]
    
    for phrase in blob_phrases:
        print(f"\n  Testando: '{phrase}'")
        result, name = simulate_blob_naming(phrase)
        print(f"    Resultado: {result}")
    
    # Teste de diferenciação
    print("\n🧪 TESTE DE DIFERENCIAÇÃO:")
    mixed_phrases = [
        ("meu nome é Bruno", "USER"),
        ("seu nome é Bob", "BLOB"),
        ("me chamo Ana", "USER"),
        ("você se chama Helper", "BLOB")
    ]
    
    for phrase, expected_type in mixed_phrases:
        print(f"\n  Testando: '{phrase}' (esperado: {expected_type})")
        
        user_result, user_name = simulate_user_introduction(phrase)
        blob_result, blob_name = simulate_blob_naming(phrase)
        
        if user_result:
            print(f"    ✅ Detectado como apresentação do USUÁRIO: {user_name}")
        elif blob_result:
            print(f"    ✅ Detectado como nomeação do BLOB: {blob_name}")
        else:
            print(f"    ❌ Não reconhecido")
    
    print("\n=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    test_user_introduction_logic()