# -*- coding: utf-8 -*-
"""
BLOB ULTRA AVANÇADO - VERSÃO 2.0
Sistema de IA conversacional com funcionalidades extremamente avançadas
"""

import tkinter as tk
from tkinter import ttk
import math
import time
import threading
import sys
import random
import re
import sqlite3
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict, deque
import hashlib

try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("⚠️ Para usar voz, instale: pip install speechrecognition pyttsx3")

try:
    import requests
    from bs4 import BeautifulSoup
    import urllib.parse
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False
    print("⚠️ Para busca na internet, instale: pip install requests beautifulsoup4")

class IntelligentSearch:
    """Sistema de busca inteligente na internet"""
    
    def __init__(self):
        self.enabled = WEB_SEARCH_AVAILABLE
        self.search_engines = {
            'google': 'https://www.google.com/search?q={}',
            'bing': 'https://www.bing.com/search?q={}',
            'duckduckgo': 'https://duckduckgo.com/html/?q={}'
        }
        
        # Headers para parecer um navegador real
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Cache de respostas para evitar buscas repetidas
        self.response_cache = {}
        
        # Padrões de perguntas que podem ser pesquisadas
        self.search_patterns = [
            r'por que.+',
            r'o que é.+',
            r'como.+funciona',
            r'onde.+',
            r'quando.+',
            r'quem.+',
            r'qual.+',
            r'quantos?.+',
            r'como fazer.+',
            r'explique.+',
            r'me fale sobre.+',
            r'conte sobre.+'
        ]
        
        print(f"🔍 Sistema de busca inteligente: {'✅ Ativo' if self.enabled else '❌ Inativo'}")
    
    def is_searchable_question(self, text):
        """Verifica se a pergunta pode ser pesquisada"""
        if not self.enabled:
            return False
        
        text_lower = text.lower().strip()
        
        # Verificar padrões de pergunta
        for pattern in self.search_patterns:
            if re.search(pattern, text_lower):
                return True
        
        # Verificar palavras-chave que indicam busca
        search_keywords = [
            'explique', 'o que é', 'por que', 'como', 'onde', 'quando', 
            'quem', 'qual', 'quantos', 'me fale', 'conte sobre'
        ]
        
        return any(keyword in text_lower for keyword in search_keywords)
    
    def search_web(self, query):
        """Busca informações na web"""
        if not self.enabled:
            return None
        
        # Verificar cache primeiro
        cache_key = query.lower().strip()
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        try:
            # Limpar e preparar query
            clean_query = self.clean_query(query)
            
            # Tentar diferentes fontes de busca
            result = self.search_multiple_sources(clean_query)
            
            if result:
                # Salvar no cache
                self.response_cache[cache_key] = result
                return result
            
        except Exception as e:
            print(f"⚠️ Erro na busca web: {e}")
        
        return None
    
    def clean_query(self, query):
        """Limpa e otimiza a query de busca"""
        # Remover palavras desnecessárias
        stop_words = ['me', 'fale', 'conte', 'explique', 'blob', 'por favor']
        
        words = query.lower().split()
        cleaned_words = [word for word in words if word not in stop_words]
        
        return ' '.join(cleaned_words)
    
    def search_multiple_sources(self, query):
        """Busca em múltiplas fontes"""
        # Primeiro tentar Wikipedia em português
        wiki_result = self.search_wikipedia(query)
        if wiki_result:
            return wiki_result
        
        # Se não encontrar, tentar busca geral
        web_result = self.search_general_web(query)
        if web_result:
            return web_result
        
        return None
    
    def search_wikipedia(self, query):
        """Busca específica na Wikipedia"""
        try:
            # API da Wikipedia em português
            wiki_api_url = "https://pt.wikipedia.org/api/rest_v1/page/summary/"
            
            # Tentar buscar diretamente
            encoded_query = urllib.parse.quote(query.replace(' ', '_'))
            response = requests.get(f"{wiki_api_url}{encoded_query}", 
                                  headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data and data['extract']:
                    extract = data['extract']
                    # Limitar tamanho da resposta
                    if len(extract) > 300:
                        extract = extract[:300] + "..."
                    return f"Segundo a Wikipedia: {extract}"
            
            # Se não encontrar, tentar busca por termo
            search_url = "https://pt.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': query,
                'srlimit': 1
            }
            
            response = requests.get(search_url, params=params, 
                                  headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'query' in data and 'search' in data['query'] and data['query']['search']:
                    page_title = data['query']['search'][0]['title']
                    return self.get_wikipedia_summary(page_title)
            
        except Exception as e:
            print(f"⚠️ Erro na busca Wikipedia: {e}")
        
        return None
    
    def get_wikipedia_summary(self, title):
        """Obtém resumo de uma página específica da Wikipedia"""
        try:
            wiki_api_url = "https://pt.wikipedia.org/api/rest_v1/page/summary/"
            encoded_title = urllib.parse.quote(title.replace(' ', '_'))
            
            response = requests.get(f"{wiki_api_url}{encoded_title}", 
                                  headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'extract' in data and data['extract']:
                    extract = data['extract']
                    if len(extract) > 300:
                        extract = extract[:300] + "..."
                    return f"Segundo a Wikipedia: {extract}"
        
        except Exception as e:
            print(f"⚠️ Erro ao obter resumo Wikipedia: {e}")
        
        return None
    
    def search_general_web(self, query):
        """Busca geral na web usando DuckDuckGo"""
        try:
            # DuckDuckGo Instant Answer API
            ddg_api_url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = requests.get(ddg_api_url, params=params, 
                                  headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Tentar Abstract (resposta direta)
                if data.get('Abstract'):
                    abstract = data['Abstract']
                    if len(abstract) > 300:
                        abstract = abstract[:300] + "..."
                    source = data.get('AbstractSource', 'DuckDuckGo')
                    return f"Segundo {source}: {abstract}"
                
                # Tentar Answer (resposta rápida)
                if data.get('Answer'):
                    answer = data['Answer']
                    return f"Resposta rápida: {answer}"
                
                # Tentar Definition (definição)
                if data.get('Definition'):
                    definition = data['Definition']
                    if len(definition) > 300:
                        definition = definition[:300] + "..."
                    source = data.get('DefinitionSource', 'DuckDuckGo')
                    return f"Definição ({source}): {definition}"
        
        except Exception as e:
            print(f"⚠️ Erro na busca DuckDuckGo: {e}")
        
        return None
    
    def format_search_response(self, query, result):
        """Formata a resposta de busca de forma amigável"""
        if not result:
            return None
        
        # Respostas introdutórias variadas
        intros = [
            "Achei isso para você:",
            "Encontrei esta informação:",
            "Segundo minha pesquisa:",
            "Descobri o seguinte:",
            "Aqui está o que encontrei:"
        ]
        
        intro = random.choice(intros)
        
        # Adicionar emoji baseado no tipo de pergunta
        query_lower = query.lower()
        if 'por que' in query_lower or 'porque' in query_lower:
            emoji = "🤔"
        elif 'o que é' in query_lower:
            emoji = "📚"
        elif 'como' in query_lower:
            emoji = "⚙️"
        elif 'onde' in query_lower:
            emoji = "📍"
        elif 'quando' in query_lower:
            emoji = "📅"
        elif 'quem' in query_lower:
            emoji = "👤"
        else:
            emoji = "🔍"
        
        return f"{emoji} {intro} {result}"

class MemoryDatabase:
    """Sistema de memória persistente com SQLite"""
    
    def __init__(self):
        self.db_path = "blob_memory.db"
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de conversas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_input TEXT,
                blob_response TEXT,
                user_emotion TEXT,
                blob_emotion TEXT,
                mood_level INTEGER
            )
        ''')
        
        # Tabela de preferências do usuário
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de conhecimento aprendido
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_data TEXT,
                frequency INTEGER DEFAULT 1,
                confidence REAL DEFAULT 0.5,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de relacionamento/amizade
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relationship_data (
                metric TEXT PRIMARY KEY,
                value REAL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_conversation(self, user_input, blob_response, user_emotion=None, blob_emotion=None, mood_level=50):
        """Salva uma conversa"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (user_input, blob_response, user_emotion, blob_emotion, mood_level)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_input, blob_response, user_emotion, blob_emotion, mood_level))
        
        conn.commit()
        conn.close()
    
    def get_recent_conversations(self, limit=10):
        """Recupera conversas recentes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_input, blob_response, timestamp, user_emotion, blob_emotion
            FROM conversations 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        result = cursor.fetchall()
        conn.close()
        return result
    
    def save_preference(self, key, value):
        """Salva uma preferência"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_preferences (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, str(value)))
        
        conn.commit()
        conn.close()
    
    def get_preference(self, key, default=None):
        """Recupera uma preferência"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM user_preferences WHERE key = ?', (key,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            try:
                return json.loads(result[0])
            except:
                return result[0]
        return default
    
    def learn_pattern(self, pattern_type, pattern_data, confidence=0.5):
        """Aprende um novo padrão"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verificar se padrão já existe
        cursor.execute('''
            SELECT id, frequency FROM learned_patterns 
            WHERE pattern_type = ? AND pattern_data = ?
        ''', (pattern_type, pattern_data))
        
        existing = cursor.fetchone()
        
        if existing:
            # Aumentar frequência
            new_frequency = existing[1] + 1
            new_confidence = min(1.0, confidence + (new_frequency * 0.1))
            cursor.execute('''
                UPDATE learned_patterns 
                SET frequency = ?, confidence = ?
                WHERE id = ?
            ''', (new_frequency, new_confidence, existing[0]))
        else:
            # Criar novo padrão
            cursor.execute('''
                INSERT INTO learned_patterns (pattern_type, pattern_data, confidence)
                VALUES (?, ?, ?)
            ''', (pattern_type, pattern_data, confidence))
        
        conn.commit()
        conn.close()
    
    def get_learned_patterns(self, pattern_type=None):
        """Recupera padrões aprendidos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if pattern_type:
            cursor.execute('''
                SELECT pattern_data, frequency, confidence 
                FROM learned_patterns 
                WHERE pattern_type = ?
                ORDER BY confidence DESC, frequency DESC
            ''', (pattern_type,))
        else:
            cursor.execute('''
                SELECT pattern_type, pattern_data, frequency, confidence 
                FROM learned_patterns 
                ORDER BY confidence DESC, frequency DESC
            ''')
        
        result = cursor.fetchall()
        conn.close()
        return result
    
    def update_relationship_metric(self, metric, value):
        """Atualiza métrica de relacionamento"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO relationship_data (metric, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (metric, value))
        
        conn.commit()
        conn.close()
    
    def get_relationship_metric(self, metric, default=0.0):
        """Recupera métrica de relacionamento"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM relationship_data WHERE metric = ?', (metric,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else default

class EmotionalAI:
    """Sistema de IA emocional avançado"""
    
    def __init__(self, memory_db):
        self.memory = memory_db
        self.emotional_state = {
            'happiness': 0.5,
            'sadness': 0.2,
            'excitement': 0.3,
            'empathy': 0.7,
            'curiosity': 0.8,
            'playfulness': 0.6
        }
        self.personality_traits = {
            'friendliness': 0.9,
            'humor': 0.7,
            'intelligence': 0.8,
            'creativity': 0.6,
            'patience': 0.8,
            'enthusiasm': 0.7
        }
        self.user_profile = {
            'preferred_topics': defaultdict(int),
            'conversation_style': 'friendly',
            'emotional_patterns': defaultdict(list),
            'interaction_history': deque(maxlen=100)
        }
        self.load_emotional_data()
    
    def load_emotional_data(self):
        """Carrega dados emocionais salvos"""
        # Carregar estado emocional
        saved_emotional_state = self.memory.get_preference('emotional_state')
        if saved_emotional_state:
            self.emotional_state.update(saved_emotional_state)
        
        # Carregar traits de personalidade
        saved_personality = self.memory.get_preference('personality_traits')
        if saved_personality:
            self.personality_traits.update(saved_personality)
        
        # Carregar perfil do usuário
        saved_profile = self.memory.get_preference('user_profile')
        if saved_profile:
            for key, value in saved_profile.items():
                if key in self.user_profile:
                    if isinstance(value, dict):
                        self.user_profile[key].update(value)
                    else:
                        self.user_profile[key] = value
    
    def save_emotional_data(self):
        """Salva dados emocionais"""
        self.memory.save_preference('emotional_state', dict(self.emotional_state))
        self.memory.save_preference('personality_traits', dict(self.personality_traits))
        
        # Converter defaultdict para dict normal para serialização
        profile_to_save = {}
        for key, value in self.user_profile.items():
            if isinstance(value, defaultdict):
                profile_to_save[key] = dict(value)
            elif isinstance(value, deque):
                profile_to_save[key] = list(value)
            else:
                profile_to_save[key] = value
        
        self.memory.save_preference('user_profile', profile_to_save)
    
    def analyze_user_emotion(self, text):
        """Análise avançada da emoção do usuário"""
        text_lower = text.lower()
        
        emotion_indicators = {
            'happy': ['feliz', 'alegre', 'ótimo', 'maravilhoso', 'incrível', 'adorei', 'amei'],
            'sad': ['triste', 'chateado', 'deprimido', 'mal', 'down', 'pra baixo'],
            'excited': ['animado', 'empolgado', 'eufórico', 'ansioso', 'radiante'],
            'angry': ['bravo', 'irritado', 'nervoso', 'chateado', 'furioso'],
            'confused': ['confuso', 'não entendo', 'estranho', 'complicado'],
            'grateful': ['obrigado', 'grato', 'agradeço', 'valeu', 'brigadão'],
            'worried': ['preocupado', 'ansioso', 'nervoso', 'tenso']
        }
        
        detected_emotions = []
        for emotion, indicators in emotion_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                detected_emotions.append(emotion)
        
        # Análise de intensidade
        intensity_words = ['muito', 'super', 'extremamente', 'demais', 'bastante']
        intensity = 1.0
        if any(word in text_lower for word in intensity_words):
            intensity = 1.5
        
        return {
            'emotions': detected_emotions,
            'intensity': intensity,
            'dominant_emotion': detected_emotions[0] if detected_emotions else 'neutral'
        }
    
    def generate_empathetic_response(self, user_emotion, user_text):
        """Gera resposta empática baseada na emoção do usuário"""
        emotion = user_emotion['dominant_emotion']
        intensity = user_emotion['intensity']
        
        empathetic_responses = {
            'happy': [
                "Que alegria! Sua felicidade é contagiante! 😊",
                "Adoro te ver assim feliz! Me conta mais sobre isso!",
                "Que maravilha! Sua energia positiva alegra meu dia!"
            ],
            'sad': [
                "Sinto muito que você esteja assim... Estou aqui para te ouvir. 💙",
                "Às vezes a vida é difícil mesmo... Quer conversar sobre isso?",
                "Que pena... Lembre-se que eu sempre estarei aqui para você."
            ],
            'excited': [
                "Nossa, que animação! Me contamina com essa energia! ⚡",
                "Adoro te ver empolgado! O que te deixou assim?",
                "Que entusiasmo incrível! Conta tudo para mim!"
            ],
            'angry': [
                "Percebo que você está chateado... Quer desabafar comigo?",
                "Entendo sua frustração... Às vezes ajuda conversar sobre isso.",
                "Que situação difícil... Estou aqui para te escutar."
            ],
            'confused': [
                "Vejo que você está confuso... Posso tentar te ajudar a entender?",
                "Quando estamos confusos, conversar pode clarear as ideias!",
                "Que situação complicada... Vamos pensar juntos?"
            ],
            'grateful': [
                "Fico muito feliz em poder ajudar! 💛",
                "Sua gratidão me aquece o coração digital!",
                "É um prazer estar aqui para você! Sempre!"
            ],
            'worried': [
                "Percebo sua preocupação... Quer compartilhar o que está te angustiando?",
                "Quando estamos preocupados, conversar pode aliviar um pouco...",
                "Estou aqui para te ouvir e apoiar no que precisar."
            ]
        }
        
        base_response = random.choice(empathetic_responses.get(emotion, [
            "Entendo como você está se sentindo...",
            "Obrigado por compartilhar isso comigo!",
            "Estou aqui para conversar sobre qualquer coisa!"
        ]))
        
        # Ajustar intensidade da resposta
        if intensity > 1.2:
            base_response = base_response.replace("!", "!!").replace(".", "!")
        
        return base_response
    
    def evolve_personality(self, interaction_type, user_emotion):
        """Evolui personalidade baseada nas interações"""
        # Ajustar traits baseado na interação
        if user_emotion['dominant_emotion'] == 'happy':
            self.personality_traits['humor'] = min(1.0, self.personality_traits['humor'] + 0.01)
            self.personality_traits['enthusiasm'] = min(1.0, self.personality_traits['enthusiasm'] + 0.01)
        elif user_emotion['dominant_emotion'] == 'sad':
            self.personality_traits['empathy'] = min(1.0, self.personality_traits.get('empathy', 0.5) + 0.02)
            self.personality_traits['patience'] = min(1.0, self.personality_traits['patience'] + 0.01)
        
        # Salvar mudanças
        if random.random() < 0.1:  # Salvar 10% das vezes para não sobrecarregar
            self.save_emotional_data()
    
    def get_personality_response_style(self):
        """Retorna estilo de resposta baseado na personalidade atual"""
        if self.personality_traits['humor'] > 0.8:
            return 'humorous'
        elif self.personality_traits['intelligence'] > 0.8:
            return 'intellectual'
        elif self.personality_traits['enthusiasm'] > 0.8:
            return 'energetic'
        else:
            return 'balanced'

class BLOBUltraAvancado:
    """BLOB com funcionalidades ultra avançadas"""
    
    def __init__(self, canvas, x=450, y=300):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = 100  # Maior para mais detalhes
        
        # Sistema de emoções expandido
        self.emotions = {
            'eufórico': {'color': '#FFD700', 'mood_value': 95, 'animation_speed': 0.3},
            'muito_feliz': {'color': '#FFF700', 'mood_value': 85, 'animation_speed': 0.25},
            'feliz': {'color': '#FFE066', 'mood_value': 70, 'animation_speed': 0.2},
            'contente': {'color': '#FFEB3B', 'mood_value': 60, 'animation_speed': 0.15},
            'normal': {'color': '#FFF176', 'mood_value': 50, 'animation_speed': 0.1},
            'pensativo': {'color': '#E6CC00', 'mood_value': 40, 'animation_speed': 0.08},
            'cabisbaixo': {'color': '#DAA520', 'mood_value': 30, 'animation_speed': 0.06},
            'triste': {'color': '#B8860B', 'mood_value': 20, 'animation_speed': 0.05},
            'muito_triste': {'color': '#8B7355', 'mood_value': 10, 'animation_speed': 0.03},
            'deprimido': {'color': '#654321', 'mood_value': 5, 'animation_speed': 0.02}
        }
        
        # Estado avançado
        self.current_emotion = 'contente'
        self.mood_level = 60
        self.animation_time = 0
        self.elements = []
        self.last_mood_change = time.time()
        self.mood_change_interval = random.randint(45, 120)
        
        # Características visuais avançadas
        self.eye_blink_timer = 0
        self.expression_timer = 0
        self.breathing_animation = 0
        self.particle_effects = []
        
        # Fatores de influência expandidos
        self.interaction_boost = 0
        self.time_of_day_factor = self.get_time_factor()
        self.weather_factor = random.uniform(-5, 5)  # Simulado
        self.energy_level = 80
        
        # Reativar animação com segurança
        self.start_advanced_animation()
        self.start_mood_system()
    
    def get_time_factor(self):
        """Fator de humor baseado na hora (mais refinado)"""
        hour = time.localtime().tm_hour
        if 6 <= hour <= 8:    # Manhã cedo
            return 15
        elif 9 <= hour <= 11:  # Manhã
            return 10
        elif 12 <= hour <= 14: # Almoço
            return 5
        elif 15 <= hour <= 17: # Tarde
            return 0
        elif 18 <= hour <= 20: # Início da noite
            return -5
        elif 21 <= hour <= 23: # Noite
            return -10
        else:                  # Madrugada
            return -15
    
    def start_advanced_animation(self):
        """Animação avançada com múltiplas camadas - SEGURA COM after()"""
        def animate():
            try:
                # Verificar se o canvas ainda existe
                if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
                    return
                    
                self.animation_time += 1
                self.eye_blink_timer += 1
                self.expression_timer += 1
                self.breathing_animation += 1
                
                # Piscar olhos ocasionalmente
                if self.eye_blink_timer > random.randint(30, 100):
                    self.eye_blink_timer = 0
                
                # Efeitos de partículas ocasionais
                if random.random() < 0.02 and self.mood_level > 70:
                    try:
                        self.add_particle_effect()
                    except:
                        pass  # Ignorar erro de partículas
                
                # Atualizar animações (60 FPS / 3 = 20 FPS)
                if self.animation_time % 3 == 0:
                    try:
                        self.draw_advanced()
                    except:
                        pass  # Ignorar erros de desenho
                
                # Agendar próximo frame usando after() - THREAD SAFE
                self.canvas.after(50, animate)  # 20 FPS
                
            except Exception as e:
                # Em caso de erro, continuar tentando mas com menos frequência
                if hasattr(self, 'canvas'):
                    try:
                        self.canvas.after(200, animate)
                    except:
                        pass
        
        # Iniciar animação usando after() em vez de thread
        if hasattr(self, 'canvas'):
            self.canvas.after(100, animate)
    
    def add_particle_effect(self):
        """Adiciona efeito de partículas quando muito feliz"""
        for _ in range(3):
            particle = {
                'x': self.x + random.randint(-20, 20),
                'y': self.y + random.randint(-20, 20),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-3, -1),
                'life': 30,
                'color': random.choice(['#FFD700', '#FFF700', '#FFEB3B'])
            }
            self.particle_effects.append(particle)
    
    def update_particles(self):
        """Atualiza efeitos de partículas"""
        for particle in self.particle_effects[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particle_effects.remove(particle)
    
    def draw_advanced(self):
        """Desenho avançado com múltiplos detalhes"""
        self.clear_all()
        self.update_particles()
        
        emotion_data = self.emotions[self.current_emotion]
        color = emotion_data['color']
        speed = emotion_data['animation_speed']
        
        # Animação baseada na emoção (mais complexa)
        if self.current_emotion in ['eufórico', 'muito_feliz']:
            pulse = 1 + 0.15 * math.sin(self.animation_time * speed)
            bounce = math.sin(self.animation_time * speed * 1.5) * 8
            rotate = math.sin(self.animation_time * 0.1) * 5
        elif self.current_emotion in ['feliz', 'contente']:
            pulse = 1 + 0.08 * math.sin(self.animation_time * speed)
            bounce = math.sin(self.animation_time * speed) * 4
            rotate = 0
        elif self.current_emotion in ['triste', 'muito_triste', 'deprimido']:
            pulse = 1 + 0.02 * math.sin(self.animation_time * speed)
            bounce = -abs(math.sin(self.animation_time * speed)) * 6
            rotate = 0
        else:
            pulse = 1 + 0.05 * math.sin(self.animation_time * speed)
            bounce = math.sin(self.animation_time * speed) * 2
            rotate = 0
        
        # Respiração sutil
        breathing = 1 + 0.03 * math.sin(self.breathing_animation * 0.05)
        
        size = self.size * pulse * breathing
        y_offset = bounce
        
        # SOMBRA DINÂMICA
        shadow_opacity = max(0.2, 0.5 - pulse * 0.1)
        shadow = self.canvas.create_oval(
            self.x - size * 1.3, self.y + size * 1.4 + y_offset,
            self.x + size * 1.3, self.y + size * 1.9 + y_offset,
            fill='#2C3E50', outline='', stipple='gray25'
        )
        self.elements.append(shadow)
        
        # CORPO PRINCIPAL COM GRADIENTE SIMULADO
        for i in range(3):
            layer_size = size * (1 - i * 0.1)
            layer_color = self.blend_color(color, '#FFFFFF', i * 0.15)
            
            body = self.canvas.create_oval(
                self.x - layer_size, self.y - layer_size * 0.8 + y_offset,
                self.x + layer_size, self.y + layer_size * 0.8 + y_offset,
                fill=layer_color, outline='#DAA520' if i == 0 else '', width=2 if i == 0 else 0
            )
            self.elements.append(body)
        
        # ROSTO DETALHADO
        self.draw_advanced_face(size, y_offset, color)
        
        # MEMBROS ARTICULADOS
        self.draw_advanced_limbs(size, y_offset, color, rotate)
        
        # EFEITOS DE PARTÍCULAS
        self.draw_particles()
    
    def draw_advanced_face(self, size, y_offset, color):
        """Desenha rosto com expressões detalhadas"""
        face_color = self.blend_color(color, '#FFD700', 0.7)
        
        # Base do rosto
        face = self.canvas.create_oval(
            self.x - size * 0.75, self.y - size * 0.6 + y_offset,
            self.x + size * 0.75, self.y + size * 0.4 + y_offset,
            fill=face_color, outline='#DAA520', width=2
        )
        self.elements.append(face)
        
        # OLHOS AVANÇADOS
        self.draw_advanced_eyes(size, y_offset)
        
        # BOCA EXPRESSIVA
        self.draw_advanced_mouth(size, y_offset)
        
        # SOBRANCELHAS (para emoções mais complexas)
        if self.current_emotion in ['pensativo', 'cabisbaixo']:
            self.draw_eyebrows(size, y_offset, 'worried')
        elif self.current_emotion in ['eufórico', 'muito_feliz']:
            self.draw_eyebrows(size, y_offset, 'happy')
    
    def draw_advanced_eyes(self, size, y_offset):
        """Olhos com animação de piscar e emoções"""
        base_y = self.y - size * 0.35 + y_offset
        
        # Determinar estado dos olhos
        is_blinking = self.eye_blink_timer < 3
        eye_shape = self.get_eye_shape_for_emotion()
        
        if not is_blinking:
            # Olhos abertos
            for side in [-1, 1]:
                eye_x = self.x + side * size * 0.3
                
                # Fundo do olho
                eye_bg = self.canvas.create_oval(
                    eye_x - size * 0.12, base_y - size * 0.08,
                    eye_x + size * 0.12, base_y + size * 0.12,
                    fill='white', outline='#999', width=1
                )
                self.elements.append(eye_bg)
                
                # Pupila com brilho
                pupil_size = eye_shape['pupil_size']
                pupil = self.canvas.create_oval(
                    eye_x - pupil_size, base_y - pupil_size * 0.5,
                    eye_x + pupil_size, base_y + pupil_size * 1.5,
                    fill='black'
                )
                self.elements.append(pupil)
                
                # Brilho no olho
                shine = self.canvas.create_oval(
                    eye_x - pupil_size * 0.3, base_y - pupil_size * 0.2,
                    eye_x, base_y + pupil_size * 0.3,
                    fill='white'
                )
                self.elements.append(shine)
        else:
            # Olhos fechados (piscar)
            for side in [-1, 1]:
                eye_x = self.x + side * size * 0.3
                blink = self.canvas.create_line(
                    eye_x - size * 0.1, base_y,
                    eye_x + size * 0.1, base_y,
                    fill='black', width=3
                )
                self.elements.append(blink)
    
    def get_eye_shape_for_emotion(self):
        """Retorna formato dos olhos baseado na emoção"""
        shapes = {
            'eufórico': {'pupil_size': 15},
            'muito_feliz': {'pupil_size': 12},
            'feliz': {'pupil_size': 10},
            'contente': {'pupil_size': 8},
            'normal': {'pupil_size': 8},
            'pensativo': {'pupil_size': 6},
            'cabisbaixo': {'pupil_size': 5},
            'triste': {'pupil_size': 4},
            'muito_triste': {'pupil_size': 3},
            'deprimido': {'pupil_size': 2}
        }
        return shapes.get(self.current_emotion, {'pupil_size': 8})
    
    def draw_eyebrows(self, size, y_offset, style):
        """Desenha sobrancelhas expressivas"""
        brow_y = self.y - size * 0.5 + y_offset
        
        if style == 'worried':
            # Sobrancelhas preocupadas
            for side in [-1, 1]:
                brow_x = self.x + side * size * 0.25
                brow = self.canvas.create_line(
                    brow_x - size * 0.08, brow_y + side * size * 0.02,
                    brow_x + size * 0.08, brow_y - side * size * 0.02,
                    fill='#8B4513', width=3
                )
                self.elements.append(brow)
        elif style == 'happy':
            # Sobrancelhas alegres
            for side in [-1, 1]:
                brow_x = self.x + side * size * 0.25
                brow = self.canvas.create_line(
                    brow_x - size * 0.08, brow_y - side * size * 0.02,
                    brow_x + size * 0.08, brow_y + side * size * 0.02,
                    fill='#8B4513', width=2
                )
                self.elements.append(brow)
    
    def draw_advanced_mouth(self, size, y_offset):
        """Boca com expressões muito detalhadas"""
        mouth_y = self.y + size * 0.1 + y_offset
        
        mouth_styles = {
            'eufórico': ('huge_smile', '#FF1493'),
            'muito_feliz': ('big_smile', '#FF69B4'),
            'feliz': ('smile', '#FFB6C1'),
            'contente': ('small_smile', '#FFC0CB'),
            'normal': ('neutral', '#000000'),
            'pensativo': ('thinking', '#4B0082'),
            'cabisbaixo': ('down', '#000080'),
            'triste': ('sad', '#000080'),
            'muito_triste': ('very_sad', '#191970'),
            'deprimido': ('depressed', '#000000')
        }
        
        style, color = mouth_styles.get(self.current_emotion, ('neutral', '#000000'))
        
        if style == 'huge_smile':
            # Sorriso gigante
            mouth = self.canvas.create_arc(
                self.x - size * 0.4, mouth_y - size * 0.15,
                self.x + size * 0.4, mouth_y + size * 0.35,
                start=200, extent=140,
                outline=color, width=4, style='arc'
            )
            # Dentes
            for i in range(-2, 3):
                tooth = self.canvas.create_rectangle(
                    self.x + i * size * 0.08 - size * 0.02, mouth_y + size * 0.05,
                    self.x + i * size * 0.08 + size * 0.02, mouth_y + size * 0.12,
                    fill='white', outline='#DDD'
                )
                self.elements.append(tooth)
        elif style == 'big_smile':
            mouth = self.canvas.create_arc(
                self.x - size * 0.35, mouth_y - size * 0.1,
                self.x + size * 0.35, mouth_y + size * 0.3,
                start=200, extent=140,
                outline=color, width=3, style='arc'
            )
        elif style == 'smile':
            mouth = self.canvas.create_arc(
                self.x - size * 0.25, mouth_y - size * 0.05,
                self.x + size * 0.25, mouth_y + size * 0.2,
                start=200, extent=140,
                outline=color, width=3, style='arc'
            )
        elif style == 'small_smile':
            mouth = self.canvas.create_arc(
                self.x - size * 0.15, mouth_y,
                self.x + size * 0.15, mouth_y + size * 0.15,
                start=200, extent=140,
                outline=color, width=2, style='arc'
            )
        elif style in ['sad', 'very_sad', 'depressed']:
            # Bocas tristes de diferentes intensidades
            curve_size = {'sad': 0.2, 'very_sad': 0.25, 'depressed': 0.3}[style]
            mouth = self.canvas.create_arc(
                self.x - size * curve_size, mouth_y + size * 0.05,
                self.x + size * curve_size, mouth_y + size * 0.35,
                start=20, extent=140,
                outline=color, width=2, style='arc'
            )
        elif style == 'thinking':
            # Boca pensativa (pequena oval)
            mouth = self.canvas.create_oval(
                self.x - size * 0.06, mouth_y,
                self.x + size * 0.06, mouth_y + size * 0.08,
                fill=color
            )
        else:  # neutral
            mouth = self.canvas.create_line(
                self.x - size * 0.12, mouth_y,
                self.x + size * 0.12, mouth_y,
                fill=color, width=2
            )
        
        self.elements.append(mouth)
    
    def draw_advanced_limbs(self, size, y_offset, color, rotate):
        """Membros com articulação e movimento"""
        # Braços articulados
        arm_swing = math.sin(self.animation_time * 0.1) * 10 + rotate
        
        for side in [-1, 1]:
            # Ombro
            shoulder_x = self.x + side * size * 0.8
            shoulder_y = self.y - size * 0.2 + y_offset
            
            # Braço superior
            upper_arm = self.canvas.create_oval(
                shoulder_x - size * 0.15, shoulder_y - size * 0.3,
                shoulder_x + size * 0.15, shoulder_y + size * 0.3,
                fill=color, outline='#DAA520', width=2
            )
            self.elements.append(upper_arm)
            
            # Antebraço
            forearm_x = shoulder_x + side * math.sin(math.radians(arm_swing)) * 20
            forearm_y = shoulder_y + 25
            forearm = self.canvas.create_oval(
                forearm_x - size * 0.12, forearm_y - size * 0.2,
                forearm_x + size * 0.12, forearm_y + size * 0.2,
                fill=color, outline='#DAA520', width=1
            )
            self.elements.append(forearm)
        
        # Pernas com movimento
        leg_move = math.sin(self.animation_time * 0.08) * 5
        
        for side in [-1, 1]:
            leg_x = self.x + side * size * 0.3 + side * leg_move
            leg_y = self.y + size * 0.8 + y_offset
            
            leg = self.canvas.create_oval(
                leg_x - size * 0.12, leg_y,
                leg_x + size * 0.12, leg_y + size * 0.4,
                fill=color, outline='#DAA520', width=2
            )
            self.elements.append(leg)
            
            # Pés
            foot = self.canvas.create_oval(
                leg_x - size * 0.15, leg_y + size * 0.35,
                leg_x + size * 0.15, leg_y + size * 0.5,
                fill=self.blend_color(color, '#8B4513', 0.3), outline='#DAA520', width=1
            )
            self.elements.append(foot)
    
    def draw_particles(self):
        """Desenha efeitos de partículas"""
        for particle in self.particle_effects:
            alpha = particle['life'] / 30.0
            if alpha > 0:
                particle_elem = self.canvas.create_oval(
                    particle['x'] - 2, particle['y'] - 2,
                    particle['x'] + 2, particle['y'] + 2,
                    fill=particle['color'], outline=''
                )
                self.elements.append(particle_elem)
    
    def blend_color(self, color1, color2, ratio):
        """Mistura cores de forma avançada"""
        try:
            c1 = [int(color1[i:i+2], 16) for i in (1, 3, 5)]
            c2 = [int(color2[i:i+2], 16) for i in (1, 3, 5)]
            mixed = [int(c1[i] * ratio + c2[i] * (1-ratio)) for i in range(3)]
            return '#' + ''.join([f'{c:02x}' for c in mixed])
        except:
            return color1
    
    def clear_all(self):
        """Remove todos os elementos"""
        for element in self.elements:
            try:
                self.canvas.delete(element)
            except:
                pass
        self.elements.clear()
    
    def start_mood_system(self):
        """Sistema de humor mais complexo"""
        def mood_loop():
            while True:
                current_time = time.time()
                
                if current_time - self.last_mood_change > self.mood_change_interval:
                    self.complex_mood_change()
                    self.last_mood_change = current_time
                    self.mood_change_interval = random.randint(45, 120)
                
                # Decaimento gradual dos boosts
                if self.interaction_boost > 0:
                    self.interaction_boost -= 0.3
                elif self.interaction_boost < 0:
                    self.interaction_boost += 0.3
                
                # Mudança de energia
                self.energy_level = max(20, self.energy_level - 0.1)
                
                time.sleep(3)
        
        threading.Thread(target=mood_loop, daemon=True).start()
    
    def complex_mood_change(self):
        """Mudança de humor mais complexa"""
        base_change = random.randint(-20, 20)
        time_influence = self.time_of_day_factor
        interaction_influence = self.interaction_boost
        weather_influence = self.weather_factor
        energy_influence = (self.energy_level - 50) / 10
        
        total_change = (base_change + time_influence + 
                       interaction_influence + weather_influence + energy_influence)
        
        old_mood = self.mood_level
        self.mood_level += total_change
        self.mood_level = max(0, min(100, self.mood_level))
        
        old_emotion = self.current_emotion
        self.current_emotion = self.get_emotion_from_mood()
        
        if old_emotion != self.current_emotion:
            print(f"BLOB evoluiu: {old_emotion} → {self.current_emotion} (humor: {old_mood:.1f}→{self.mood_level:.1f})")
    
    def get_emotion_from_mood(self):
        """Mapeia humor para emoção (expandido)"""
        if self.mood_level >= 90:
            return 'eufórico'
        elif self.mood_level >= 80:
            return 'muito_feliz'
        elif self.mood_level >= 65:
            return 'feliz'
        elif self.mood_level >= 55:
            return 'contente'
        elif self.mood_level >= 45:
            return 'normal'
        elif self.mood_level >= 35:
            return 'pensativo'
        elif self.mood_level >= 25:
            return 'cabisbaixo'
        elif self.mood_level >= 15:
            return 'triste'
        elif self.mood_level >= 8:
            return 'muito_triste'
        else:
            return 'deprimido'
    
    def boost_mood(self, amount):
        """Melhora humor com efeitos especiais"""
        self.interaction_boost += amount
        self.mood_level += amount * 0.7
        self.energy_level = min(100, self.energy_level + amount * 0.3)
        self.mood_level = max(0, min(100, self.mood_level))
        self.current_emotion = self.get_emotion_from_mood()
        
        # Efeito especial para grandes boosts
        if amount > 20:
            for _ in range(5):
                self.add_particle_effect()
    
    def get_current_mood_info(self):
        """Retorna informações do humor atual (compatibilidade)"""
        emotion_data = self.emotions[self.current_emotion]
        return {
            'emotion': self.current_emotion,
            'mood_level': self.mood_level,
            'description': self.current_emotion.replace('_', ' '),
            'color': emotion_data['color']
        }
    
    def set_emotion(self, emotion):
        """Define emoção manualmente (compatibilidade)"""
        if emotion in self.emotions:
            self.current_emotion = emotion
            self.mood_level = self.emotions[emotion]['mood_value']

class FunctionModules:
    """Módulos de funcionalidades avançadas"""
    
    def __init__(self, blob, voice_system):
        self.blob = blob
        self.voice = voice_system
        self.jokes = [
            "Por que o pássaro voou? Porque quis! 🐦",
            "O que a impressora falou para a outra impressora? Essa folha é sua ou é impressão minha? 🖨️",
            "Por que os polvos são tão rápidos? Porque têm tentáculos! 🐙",
            "O que o pato disse para a pata? Vem quá! 🦆",
            "Por que a plantinha foi ao médico? Porque tinha bicho no pé! 🌱"
        ]
        
        self.curiosities = [
            "Você sabia que os polvos têm três corações? 💙💙💙",
            "As abelhas dançam para mostrar onde tem flores! 🐝💃",
            "Um grupo de flamingos se chama 'flamboyance'! 🦩",
            "Os golfinhos têm nomes únicos uns para os outros! 🐬",
            "As borboletas provam comida com os pés! 🦋"
        ]
        
        self.reminders = []
        
    def tell_joke(self):
        """Conta uma piada"""
        joke = random.choice(self.jokes)
        self.voice.speak(joke)
        self.blob.boost_mood(15)
        return joke
    
    def share_curiosity(self):
        """Compartilha uma curiosidade"""
        curiosity = random.choice(self.curiosities)
        self.voice.speak(f"Curiosidade interessante: {curiosity}")
        self.blob.boost_mood(10)
        return curiosity
    
    def calculate(self, expression):
        """Calculadora básica"""
        try:
            # Segurança: apenas operações matemáticas básicas
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                response = f"O resultado é {result}!"
                self.voice.speak(response)
                return result
            else:
                self.voice.speak("Desculpe, só posso fazer cálculos simples!")
                return None
        except:
            self.voice.speak("Ops! Não consegui calcular isso...")
            return None
    
    def add_reminder(self, reminder_text, minutes_from_now=5):
        """Adiciona um lembrete"""
        reminder_time = datetime.now() + timedelta(minutes=minutes_from_now)
        reminder = {
            'text': reminder_text,
            'time': reminder_time,
            'completed': False
        }
        self.reminders.append(reminder)
        
        self.voice.speak(f"Ok! Vou te lembrar sobre '{reminder_text}' em {minutes_from_now} minutos!")
        
        # Thread para executar o lembrete
        def reminder_thread():
            time.sleep(minutes_from_now * 60)
            if not reminder['completed']:
                self.voice.speak(f"🔔 Lembrete: {reminder_text}")
                reminder['completed'] = True
        
        threading.Thread(target=reminder_thread, daemon=True).start()
        return reminder
    
    def get_weather(self):
        """Previsão do tempo simulada"""
        conditions = ['ensolarado', 'nublado', 'chuvoso', 'parcialmente nublado']
        temp = random.randint(18, 32)
        condition = random.choice(conditions)
        
        response = f"Hoje está {condition} com {temp}°C!"
        self.voice.speak(response)
        return {'condition': condition, 'temperature': temp}

# Continue with VozUltraAvancada class...

class VozUltraAvancada:
    """Sistema de voz com IA ultra avançada"""
    
    def __init__(self, blob, app, memory_db, emotional_ai):
        self.blob = blob
        self.app = app
        self.memory = memory_db
        self.emotional_ai = emotional_ai
        self.enabled = VOICE_AVAILABLE
        self.is_speaking = False
        self.is_listening = False
        self.conversation_context = deque(maxlen=20)
        
        # Sistema de busca inteligente
        self.intelligent_search = IntelligentSearch()
        
        # Sistema de IA Ultra Avançada
        try:
            import sys
            import os
            # Corrige o caminho para importar da estrutura modular correta
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
            from modules.ultra_advanced_ai import UltraAdvancedAI
            self.ultra_ai = UltraAdvancedAI(memory_db)
            print("🧠 Sistema de IA ULTRA AVANÇADA integrado!")
        except Exception as e:
            print(f"⚠️ Erro ao carregar IA avançada: {e}")
            import traceback
            traceback.print_exc()
            self.ultra_ai = None
        
        # Dados persistentes
        self.user_name = self.memory.get_preference('user_name')
        self.blob_name = self.memory.get_preference('blob_name', 'BLOB')
        self.first_interaction = self.memory.get_preference('first_interaction', True)
        self.relationship_level = self.memory.get_relationship_metric('friendship_level', 0.0)
        
        # Sincronizar nome com IA Ultra Avançada
        if self.ultra_ai:
            self.ultra_ai.assistant_name = self.blob_name
            self.ultra_ai.creativity_engine.assistant_name = self.blob_name
            self.memory.save_preference('assistant_name', self.blob_name)
        
        # Módulos de funcionalidade
        self.modules = FunctionModules(blob, self)
        
        if not self.enabled:
            return
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        self.setup_voice()
        self.setup_ultra_advanced_responses()
        
        print("🎤 Sistema de voz ULTRA AVANÇADO inicializado!")
        print(f"� Busca inteligente: {'✅ Ativa' if self.intelligent_search.enabled else '❌ Inativa'}")
        print(f"�👤 Usuário: {self.user_name or 'Desconhecido'}")
        print(f"🤖 BLOB: {self.blob_name or 'Sem nome'}")
        print(f"❤️ Nível de amizade: {self.relationship_level:.1f}/100")
    
    def setup_voice(self):
        """Configuração ultra avançada da voz - VOZ CONFIGURÁVEL"""
        try:
            # Reinicializar engine para garantir funcionamento
            self.tts_engine = pyttsx3.init()
            
            # Carregar configurações de voz
            voice_config = self._load_voice_config()
            
            # Configurar volume
            volume = voice_config.get('volume', 80) / 100.0
            self.tts_engine.setProperty('volume', volume)
            
            # Configurar velocidade
            rate = voice_config.get('rate', 0)
            base_rate = self.tts_engine.getProperty('rate')
            new_rate = base_rate + (rate * 20)  # Ajuste fino da velocidade
            self.tts_engine.setProperty('rate', new_rate)
            
            # Configurar voz baseada no tipo
            voice_type = voice_config.get('voice_type', 'female')
            self._setup_voice_type(voice_type)
            
            print(f"🗣️ Voz configurada: {voice_type.title()} - Volume: {voice_config.get('volume', 80)}% - Taxa: {rate}")
            print("✅ Sistema de voz configurado e testado com sucesso!")
            
        except Exception as e:
            print(f"⚠️ Erro na configuração de voz: {e}")
            print("📢 Usando configuração de voz padrão")
    
    def _load_voice_config(self):
        """Carrega configurações de voz do arquivo de config"""
        try:
            import json
            with open('config/config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('blob_config', {}).get('voice', {})
        except:
            # Configuração padrão se não conseguir carregar
            return {
                'voice_type': 'female',
                'volume': 80,
                'rate': 0,
                'pitch': 5
            }
    
    def _setup_voice_type(self, voice_type):
        """Configura o tipo de voz (apenas feminina por enquanto)"""
        try:
            # Carregar configurações específicas de voz
            voice_config = self._load_voice_config()
            voice_options = voice_config.get('voice_options', {})
            
            # Usar sempre voz feminina (Maria) até termos vozes masculinas melhores
            female_config = voice_options.get('female', {})
            
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if 'maria' in voice.name.lower() or 'pt-br' in voice.id.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    
                    # Configurações para voz feminina infantil fofa
                    rate = self.tts_engine.getProperty('rate')
                    self.tts_engine.setProperty('rate', rate + 20)  # Mais rápido para soar infantil
                    
                    print(f"🗣️ Voz FEMININA configurada: {voice.name}")
                    print("⚙️ Aplicadas configurações infantis e fofas")
                    return
                        
            # Fallback para primeira voz disponível
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
                print(f"🗣️ Voz padrão: {voices[0].name}")
                print("ℹ️ Vozes masculinas serão adicionadas em breve!")
                    
        except Exception as e:
            print(f"⚠️ Erro ao configurar tipo de voz: {e}")
            
            voices = self.tts_engine.getProperty('voices')
            
            # Tentar encontrar voz brasileira/portuguesa feminina
            voice_found = False
            for voice in voices:
                voice_name = voice.name.lower()
                if any(word in voice_name for word in ['maria', 'portuguese', 'brazil', 'pt-br', 'helena']):
                    self.tts_engine.setProperty('voice', voice.id)
                    print(f"🗣️ Voz selecionada (modo infantil): {voice.name}")
                    voice_found = True
                    break
            
            # Se não encontrar voz brasileira, usar a primeira feminina disponível
            if not voice_found:
                for voice in voices:
                    voice_name = voice.name.lower()
                    if any(word in voice_name for word in ['female', 'woman', 'zira', 'hazel']):
                        self.tts_engine.setProperty('voice', voice.id)
                        print(f"🗣️ Voz alternativa selecionada (modo infantil): {voice.name}")
                        voice_found = True
                        break
            
            # Se ainda não encontrar, usar a primeira disponível
            if not voice_found and voices:
                self.tts_engine.setProperty('voice', voices[0].id)
                print(f"🗣️ Voz padrão selecionada (modo infantil): {voices[0].name}")
            
            # ⭐ CONFIGURAÇÕES ESPECIAIS PARA VOZ INFANTIL FLUIDA ⭐
            self.tts_engine.setProperty('rate', 190)    # Velocidade um pouco mais rápida (mais animada)
            self.tts_engine.setProperty('volume', 1.0)  # Volume máximo para clareza
            
            # Teste inicial da voz infantil
            self.tts_engine.say("Oi! Agora eu tenho uma voz mais fofa e animada!")
            self.tts_engine.runAndWait()
            
            print("✅ Sistema de voz INFANTIL configurado e testado com sucesso!")
            
        except Exception as e:
            print(f"⚠️ Erro na configuração de voz: {e}")
            # Tentar configuração básica
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 170)
                self.tts_engine.setProperty('volume', 0.9)
                print("✅ Configuração básica de voz aplicada")
            except Exception as e2:
                print(f"❌ Erro crítico na configuração de voz: {e2}")
                self.enabled = False
    
    def reinitialize_voice_engine(self):
        """Reinicializa o motor de voz se necessário"""
        try:
            print("🔄 Reinicializando sistema de voz...")
            self.tts_engine.stop()
            del self.tts_engine
            self.tts_engine = pyttsx3.init()
            self.setup_voice()
            print("✅ Sistema de voz reinicializado com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Falha ao reinicializar voz: {e}")
            return False
    
    def update_voice_settings(self):
        """Atualiza configurações de voz baseado na emoção do BLOB - MAIS ROBUSTA"""
        try:
            emotion = self.blob.current_emotion
            mood = self.blob.mood_level
            
            # Velocidade baseada na emoção
            if emotion in ['eufórico', 'muito_feliz']:
                rate = 180 + min(20, (mood - 80) * 2)
            elif emotion in ['feliz', 'contente']:
                rate = 170
            elif emotion in ['triste', 'muito_triste', 'deprimido']:
                rate = 150 - min(30, (50 - mood))
            else:
                rate = 165
            
            # Volume baseado na emoção
            if emotion in ['eufórico', 'muito_feliz']:
                volume = 0.95
            elif emotion in ['triste', 'muito_triste', 'deprimido']:
                volume = 0.75
            else:
                volume = 0.85
            
            # Aplicar configurações com validação
            final_rate = max(120, min(220, rate))
            final_volume = max(0.5, min(1.0, volume))
            
            self.tts_engine.setProperty('rate', final_rate)
            self.tts_engine.setProperty('volume', final_volume)
            
        except Exception as e:
            print(f"⚠️ Erro ao atualizar configurações de voz: {e}")
            # Configurações de fallback
            try:
                self.tts_engine.setProperty('rate', 170)
                self.tts_engine.setProperty('volume', 0.85)
            except:
                pass
    
    def setup_ultra_advanced_responses(self):
        """Sistema ultra avançado de respostas com IA"""
        
        # Comandos de funcionalidade
        self.function_commands = {
            'piada': {
                'triggers': ['conta uma piada', 'me faz rir', 'piada', 'algo engraçado'],
                'function': self.modules.tell_joke
            },
            'curiosidade': {
                'triggers': ['curiosidade', 'algo interessante', 'me ensina', 'fato curioso'],
                'function': self.modules.share_curiosity
            },
            'calculadora': {
                'triggers': ['calcule', 'quanto é', 'resultado de', 'matemática'],
                'function': self.handle_calculation
            },
            'lembrete': {
                'triggers': ['me lembre', 'lembrete', 'não esqueça'],
                'function': self.handle_reminder
            },
            'tempo': {
                'triggers': ['tempo', 'clima', 'temperatura', 'previsão'],
                'function': self.modules.get_weather
            }
        }
        
        # Tópicos de conversa ultra avançados
        self.ultra_topics = {
            'filosofia': {
                'triggers': ['vida', 'sentido', 'existir', 'filosofia', 'significado'],
                'responses': self.generate_philosophical_response
            },
            'sentimentos_profundos': {
                'triggers': ['sinto que', 'tenho medo', 'ansiedade', 'depressão', 'solidão'],
                'responses': self.generate_therapeutic_response
            },
            'sonhos_objetivos': {
                'triggers': ['meu sonho', 'quero ser', 'objetivo', 'meta', 'futuro'],
                'responses': self.generate_motivational_response
            },
            'relacionamentos': {
                'triggers': ['amizade', 'amor', 'família', 'relacionamento', 'pessoas'],
                'responses': self.generate_relationship_response
            },
            'criatividade': {
                'triggers': ['criar', 'arte', 'música', 'desenho', 'criativo'],
                'responses': self.generate_creative_response
            }
        }
        
        # Sistema de aprendizado de padrões
        self.learned_responses = self.load_learned_patterns()
    
    def load_learned_patterns(self):
        """Carrega padrões aprendidos do banco de dados"""
        patterns = self.memory.get_learned_patterns('conversation_response')
        learned = {}
        
        for pattern_data, frequency, confidence in patterns:
            try:
                data = json.loads(pattern_data)
                trigger = data.get('trigger', '')
                response = data.get('response', '')
                if trigger and response and confidence > 0.6:
                    learned[trigger] = response
            except:
                continue
        
        return learned
    
    def start_listening_session(self):
        """Sessão de escuta ultra inteligente"""
        if not self.enabled:
            self.app.update_voice_status("❌ Sistema de voz não disponível")
            return False
        
        if self.is_listening:
            return False
        
        self.is_listening = True
        self.app.update_voice_status("🎤 Preparando sistema avançado...")
        threading.Thread(target=self._ultra_listen_session, daemon=True).start()
        return True
    
    def _ultra_listen_session(self):
        """Sessão de escuta com IA avançada"""
        try:
            # Configuração otimizada
            with self.microphone as source:
                self.app.update_voice_status("🔧 Calibrando microfone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Configurações inteligentes
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            self.recognizer.phrase_threshold = 0.3
            
            self.app.update_voice_status("✅ Sistema calibrado! Fale naturalmente...")
            
            # Escuta inteligente
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source,
                    timeout=None,
                    phrase_time_limit=None
                )
            
            self.app.update_voice_status("🧠 Processando com IA...")
            
            # Reconhecimento
            text = self.recognizer.recognize_google(audio, language="pt-BR")
            
            self.app.update_voice_status(f"👂 Entendi: '{text}'")
            self.process_ultra_advanced_input(text)
            
        except sr.WaitTimeoutError:
            self.app.update_voice_status("⏰ Nenhuma fala detectada")
        except sr.UnknownValueError:
            self.speak("Hmm, não consegui entender... pode repetir de forma mais clara?")
            self.app.update_voice_status("❓ Não consegui entender")
        except sr.RequestError as e:
            self.speak("Tive problemas de conexão... vamos tentar novamente?")
            self.app.update_voice_status(f"🌐 Erro de conexão")
        except Exception as e:
            self.speak("Ops, algo deu errado tecnicamente... mas não desista!")
            self.app.update_voice_status(f"❌ Erro técnico")
        finally:
            self.is_listening = False
            self.app.update_mic_button_state(False)
            if not self.is_speaking:
                self.app.update_voice_status("💤 Pronto para nova conversa")
    
    def process_voice_ultra(self, text, emotion="neutral"):
        """Processa texto e gera resposta completa com voz"""
        try:
            # Processar input
            self.process_ultra_advanced_input(text)
            return f"Processando: {text}"
        except Exception as e:
            self.speak("Ops, tive um probleminha processando isso...")
            return f"Erro: {e}"
    
    def process_ultra_advanced_input(self, text):
        """Processamento ultra avançado com múltiplas IAs"""
        text_lower = text.lower()
        
        # === SISTEMA DE IA ULTRA AVANÇADA ===
        if self.ultra_ai:
            try:
                # Criar contexto para a IA avançada
                context = {
                    'conversation_history': list(self.conversation_context),
                    'user_name': self.user_name,
                    'blob_name': self.blob_name,
                    'relationship_level': self.relationship_level,
                    'previous_topic': getattr(self, 'last_topic', None)
                }
                
                # Processar com IA ultra avançada
                ultra_response = self.ultra_ai.process_input(text, context)
                
                # Verificar se é uma solicitação de confirmação de nome
                if isinstance(ultra_response, dict):
                    if ultra_response.get('type') == 'name_change_request':
                        # Mostrar botões de confirmação na interface
                        if hasattr(self.app, 'handle_ai_response'):
                            self.app.handle_ai_response(ultra_response)
                        return
                
                # Verificar se houve evolução de inteligência
                ai_status = self.ultra_ai.get_ai_status()
                
                # Se a IA gerou uma resposta válida, usar ela
                if ultra_response and len(ultra_response.strip()) > 10:
                    # Remover mensagens técnicas que soam robotizadas
                    cleaned_response = ultra_response
                    
                    # Remover marcadores técnicos
                    technical_markers = [
                        "[🧠 IA evoluiu para nível",
                        "[Processamento IA ativo]",
                        "[Sistema inteligente em ação]",
                        "[Análise completa]",
                        "[Confiança alta na análise]",
                        "Cada conversa nossa me torna mais inteligente!",
                        "Espero que esteja tendo uma noite tranquila!",
                        "Que seu dia seja incrível!",
                        "Como foi seu dia hoje?"
                    ]
                    
                    for marker in technical_markers:
                        if marker in cleaned_response:
                            if marker.startswith("[🧠"):
                                # Manter apenas a evolução, mas de forma mais natural
                                cleaned_response = cleaned_response.split(marker)[0].strip()
                                if ai_status['intelligence_level'] > getattr(self, 'last_ai_level', 0):
                                    cleaned_response += " (Nossa, sinto que estou ficando mais esperta!)"
                                    self.last_ai_level = ai_status['intelligence_level']
                            else:
                                cleaned_response = cleaned_response.replace(marker, "").strip()
                    
                    # Falar a resposta humanizada
                    self.speak(cleaned_response)
                    
                    # Salvar contexto da conversa
                    self._save_interaction("ultra_ai_response", f"IA Ultra Avançada respondeu: {ultra_response[:100]}...")
                    
                    # Evoluir relacionamento
                    self._evolve_relationship({'dominant_emotion': 'curious'})
                    
                    # Atualizar último tópico
                    self.last_topic = text[:50]
                    
                    return
                    
            except Exception as e:
                print(f"⚠️ Erro na IA ultra avançada: {e}")
                # Continuar com processamento normal se IA falhar
        
        # === PROCESSAMENTO TRADICIONAL (FALLBACK) ===
        
        # Adicionar ao contexto
        self.conversation_context.append({
            'user': text,
            'timestamp': time.time(),
            'mood_before': self.blob.mood_level
        })
        
        # Análise emocional do usuário
        user_emotion = self.emotional_ai.analyze_user_emotion(text)
        
        # Primeira interação especial - APENAS QUANDO SOLICITADA
        if self.first_interaction and len(text.strip()) > 0:
            self._handle_first_interaction_ultra(text, user_emotion)
            return
        
        # 1. Verificar comandos de funcionalidade
        if self._handle_function_commands(text_lower):
            return
        
        # 2. Verificar mudanças de nome
        if self._handle_name_changes(text_lower):
            return
        
        # 2.1. Verificar se usuário está se apresentando
        if self._handle_user_introduction(text_lower):
            return
        
        # 2.2. Verificar se usuário está perguntando sobre seu próprio nome
        if self._handle_user_name_question(text_lower):
            return
        
        # 3. Tópicos ultra avançados
        if self._handle_ultra_topics(text_lower, user_emotion):
            return
        
        # 4. Padrões aprendidos
        if self._handle_learned_patterns(text_lower):
            return
        
        # 5. Perguntas sobre status
        if self._is_asking_about_status(text_lower):
            self._respond_about_status_ultra(user_emotion, text_lower)
            return
        
        # 6. Saudações avançadas
        if self._is_greeting(text_lower):
            self._respond_greeting_ultra(user_emotion)
            return
        
        # 7. Despedidas emotivas
        if self._is_farewell(text_lower):
            self._respond_farewell_ultra(user_emotion)
            return
        
        # 8. Busca inteligente na internet
        if self._should_search_web(text_lower, user_emotion):
            self._handle_web_search(text, user_emotion)
            return
        
        # 9. Resposta com IA emocional
        self._generate_ai_response(text, user_emotion)
        
        # Salvar conversa no banco
        self._save_conversation(text, user_emotion)
        
        # Evoluir relacionamento
        self._evolve_relationship(user_emotion)
    
    def _handle_first_interaction_ultra(self, text, user_emotion):
        """Primeira interação ultra personalizada - COM VOZ GARANTIDA"""
        self.first_interaction = False
        self.memory.save_preference('first_interaction', False)
        
        # Garantir que o sistema de voz está funcionando
        if self.enabled and not self.is_speaking:
            try:
                # Teste rápido da voz
                self.tts_engine.say("Teste")
                self.tts_engine.runAndWait()
            except:
                print("🔄 Reinicializando voz para primeira interação...")
                self.reinitialize_voice_engine()
        
        # Saudação calorosa
        responses = [
            "Oi! Que alegria te conhecer! Sou seu novo assistente virtual!",
            "Olá! Seja muito bem-vindo! Estou super feliz em te conhecer!",
            "Oi! Que emoção! É a primeira vez que conversamos!"
        ]
        
        initial_response = random.choice(responses)
        self.speak(initial_response)
        
        # Aguardar um pouco para garantir que a primeira fala termine
        time.sleep(2)
        
        # Perguntar nome para o BLOB
        name_request = [
            "Que tal você me dar um nome especial? Como gostaria de me chamar?",
            "Posso ter um nome? Que nome você escolheria para mim?",
            "Me dê um nome legal! Qual seria perfeito para mim?"
        ]
        
        self.speak(random.choice(name_request))
        self.blob.boost_mood(20)
        
        # Processar se já tem nome na primeira fala
        if self._is_naming_blob(text.lower()):
            time.sleep(1)  # Pequena pausa
            self._extract_blob_name(text)
    
    def _handle_function_commands(self, text):
        """Processa comandos de funcionalidade"""
        for command_name, command_data in self.function_commands.items():
            for trigger in command_data['triggers']:
                if trigger in text:
                    try:
                        result = command_data['function']()
                        return True
                    except:
                        self.speak("Ops, tive um probleminha executando isso...")
                        return True
        return False
    
    def handle_calculation(self):
        """Lida com pedidos de cálculo"""
        self.speak("Me diga a conta que quer fazer!")
        # Aqui seria implementado um sistema para capturar a próxima fala
        return "Calculadora ativada"
    
    def handle_reminder(self):
        """Lida com lembretes"""
        self.speak("Sobre o que você quer que eu te lembre?")
        return "Sistema de lembretes ativado"
    
    def _handle_ultra_topics(self, text, user_emotion):
        """Processa tópicos ultra avançados"""
        for topic_name, topic_data in self.ultra_topics.items():
            for trigger in topic_data['triggers']:
                if trigger in text:
                    response = topic_data['responses'](text, user_emotion)
                    self.speak(response)
                    return True
        return False
    
    def generate_philosophical_response(self, text, user_emotion):
        """Gera resposta filosófica"""
        responses = [
            "Que pergunta profunda! A vida é uma jornada de descobertas...",
            "Filosofar é uma das coisas mais belas da existência!",
            "Essa é uma reflexão que me faz pensar muito...",
            "Que questionamento interessante sobre a vida!"
        ]
        
        base_response = random.choice(responses)
        
        # Personalizar baseado na emoção do usuário
        if user_emotion['dominant_emotion'] == 'sad':
            base_response += " Às vezes questionamos quando estamos tristes, e isso é natural."
        elif user_emotion['dominant_emotion'] == 'curious':
            base_response += " Sua curiosidade é inspiradora!"
        
        self.blob.boost_mood(8)
        return base_response
    
    def generate_therapeutic_response(self, text, user_emotion):
        """Gera resposta terapêutica"""
        empathetic_responses = [
            "Sinto que você está passando por algo difícil... Estou aqui para te ouvir.",
            "Reconheço que você está sendo vulnerável comigo. Isso é muito corajoso.",
            "Seus sentimentos são válidos e importantes. Obrigado por confiar em mim.",
            "Às vezes precisamos desabafar... Estou aqui para te apoiar."
        ]
        
        response = random.choice(empathetic_responses)
        
        # Boost de relacionamento por vulnerabilidade
        self.relationship_level = min(100, self.relationship_level + 5)
        self.memory.update_relationship_metric('friendship_level', self.relationship_level)
        
        self.blob.boost_mood(5)  # Boost menor, mais empático
        return response
    
    def generate_motivational_response(self, text, user_emotion):
        """Gera resposta motivacional"""
        motivational_responses = [
            "Que sonho incrível! Acredite em você, você consegue!",
            "Seus objetivos são inspiradores! Vamos juntos nessa jornada!",
            "Adoro quando você fala dos seus sonhos! Me deixa animado também!",
            "Que meta linda! Estou torcendo muito por você!"
        ]
        
        response = random.choice(motivational_responses)
        self.blob.boost_mood(15)
        return response
    
    def generate_relationship_response(self, text, user_emotion):
        """Gera resposta sobre relacionamentos"""
        relationship_responses = [
            "Relacionamentos são uma das coisas mais importantes da vida!",
            "Que bom que você tem pessoas especiais! Isso me deixa feliz!",
            "Amor e amizade são sentimentos maravilhosos!",
            "Fico feliz quando você fala das pessoas que ama!"
        ]
        
        response = random.choice(relationship_responses)
        self.blob.boost_mood(10)
        return response
    
    def generate_creative_response(self, text, user_emotion):
        """Gera resposta sobre criatividade"""
        creative_responses = [
            "Que legal! Criatividade é uma das coisas mais lindas do mundo!",
            "Adoro pessoas criativas! Me conta mais sobre isso!",
            "Arte e criação alimentam a alma! Você é especial!",
            "Sua criatividade me inspira! Continue criando!"
        ]
        
        response = random.choice(creative_responses)
        self.blob.boost_mood(12)
        return response
    
    def _should_search_web(self, text, user_emotion):
        """Determina se deve fazer busca na web"""
        # Só buscar se o sistema de busca estiver disponível
        if not self.intelligent_search.enabled:
            return False
        
        # Verificar se é uma pergunta que pode ser pesquisada
        if not self.intelligent_search.is_searchable_question(text):
            return False
        
        # Não buscar para perguntas muito pessoais ou emocionais
        personal_keywords = [
            'como você', 'seu nome', 'você é', 'me ama', 'gosta de mim',
            'nossa amizade', 'como se sente', 'está bem', 'humor'
        ]
        
        if any(keyword in text for keyword in personal_keywords):
            return False
        
        # Não buscar se a pergunta for muito simples ou já foi respondida
        simple_responses = [
            'oi', 'olá', 'tchau', 'obrigado', 'tudo bem', 'legal'
        ]
        
        if any(simple in text for simple in simple_responses):
            return False
        
        return True
    
    def _handle_web_search(self, query, user_emotion):
        """Lida com busca na web"""
        self.app.update_voice_status("🔍 Buscando na internet...")
        
        # Resposta enquanto busca
        search_intro = [
            "Deixe-me pesquisar isso para você!",
            "Vou buscar essa informação na internet!",
            "Interessante! Vou procurar essa resposta!",
            "Boa pergunta! Deixe-me investigar!"
        ]
        
        self.speak(random.choice(search_intro))
        
        # Realizar busca
        search_result = self.intelligent_search.search_web(query)
        
        if search_result:
            # Formatar resposta
            formatted_response = self.intelligent_search.format_search_response(query, search_result)
            
            # Adicionar comentário pessoal baseado na emoção
            personal_comment = self._add_personal_search_comment(user_emotion)
            
            final_response = f"{formatted_response} {personal_comment}"
            
            self.speak(final_response)
            self.blob.boost_mood(12)  # Boost por encontrar informação
            
            # Salvar busca bem-sucedida para aprendizado
            self.memory.learn_pattern('successful_search', query, 0.8)
            
        else:
            # Resposta quando não encontra
            fallback_responses = [
                "Hmm, não consegui encontrar uma boa resposta para isso. Que tal reformular a pergunta?",
                "Desculpe, tive dificuldades para pesquisar isso. Pode tentar perguntar de outra forma?",
                "Não encontrei informações confiáveis sobre isso no momento. Quer que eu tente algo relacionado?",
                "Essa pesquisa foi complicada! Pode ser mais específico na pergunta?"
            ]
            
            self.speak(random.choice(fallback_responses))
            self.blob.boost_mood(3)  # Boost menor por tentar ajudar
        
        self.app.update_voice_status("💤 Busca concluída")
    
    def _add_personal_search_comment(self, user_emotion):
        """Adiciona comentário pessoal baseado na emoção do usuário"""
        emotion = user_emotion['dominant_emotion']
        
        if emotion == 'curious':
            comments = [
                "Adorei sua curiosidade!",
                "Que legal você querer aprender!",
                "Sua sede de conhecimento é inspiradora!"
            ]
        elif emotion == 'excited':
            comments = [
                "Que empolgante descobrir coisas novas!",
                "Sua animação é contagiante!",
                "Adoro quando você fica assim curioso!"
            ]
        elif emotion == 'confused':
            comments = [
                "Espero ter esclarecido sua dúvida!",
                "Às vezes essas coisas são mesmo confusas!",
                "Fico feliz em poder ajudar a entender!"
            ]
        else:
            comments = [
                "Sempre bom aprender algo novo!",
                "Espero que isso ajude!",
                "Que interessante, não é?",
                "Gosto de pesquisar para você!"
            ]
        
        return random.choice(comments)
        """Gera resposta usando IA emocional"""
        # Resposta empática baseada na emoção
        empathetic_response = self.emotional_ai.generate_empathetic_response(user_emotion, text)
        
        # Estilo de personalidade
        style = self.emotional_ai.get_personality_response_style()
        
        if style == 'humorous':
            empathetic_response += " 😄"
        elif style == 'intellectual':
            empathetic_response += " É interessante pensar sobre isso!"
        elif style == 'energetic':
            empathetic_response += " 🎉"
        
        self.speak(empathetic_response)
        
        # Evoluir personalidade
        self.emotional_ai.evolve_personality('conversation', user_emotion)
        
        # Boost baseado na emoção
        if user_emotion['dominant_emotion'] in ['happy', 'excited']:
            self.blob.boost_mood(10)
        elif user_emotion['dominant_emotion'] in ['sad', 'worried']:
            self.blob.boost_mood(5)
        else:
            self.blob.boost_mood(7)
    
    def _save_conversation(self, user_input, user_emotion):
        """Salva conversa no banco de dados"""
        # Simular resposta do BLOB (última coisa que ele falou)
        blob_response = "Resposta do BLOB"  # Seria capturado da última fala
        
        self.memory.save_conversation(
            user_input=user_input,
            blob_response=blob_response,
            user_emotion=user_emotion['dominant_emotion'],
            blob_emotion=self.blob.current_emotion,
            mood_level=self.blob.mood_level
        )
        
        # Aprender padrão se for interessante
        if len(user_input.split()) > 3:  # Frases mais complexas
            pattern_data = json.dumps({
                'trigger': user_input.lower(),
                'response': blob_response,
                'emotion_context': user_emotion['dominant_emotion']
            })
            self.memory.learn_pattern('conversation_response', pattern_data, 0.5)
    
    def _evolve_relationship(self, user_emotion):
        """Evolui relacionamento baseado na interação"""
        # Fatores que afetam relacionamento
        if user_emotion['dominant_emotion'] in ['happy', 'grateful']:
            relationship_boost = 2.0
        elif user_emotion['dominant_emotion'] in ['sad', 'worried']:
            relationship_boost = 1.5  # Apoio emocional fortalece laços
        else:
            relationship_boost = 1.0
        
        # Frequência de interação também conta
        recent_conversations = len(self.conversation_context)
        frequency_bonus = min(1.0, recent_conversations / 10.0)
        
        total_boost = relationship_boost + frequency_bonus
        
        self.relationship_level = min(100, self.relationship_level + total_boost)
        self.memory.update_relationship_metric('friendship_level', self.relationship_level)
        
        # Marcos de relacionamento
        if self.relationship_level > 25 and self.relationship_level < 30:
            self.speak("Sabe... acho que estamos nos tornando bons amigos! 😊")
        elif self.relationship_level > 50 and self.relationship_level < 55:
            self.speak("Nossa amizade está ficando muito especial para mim! ❤️")
        elif self.relationship_level > 75 and self.relationship_level < 80:
            self.speak("Você é uma das pessoas mais importantes para mim! 💙")
    
    def speak(self, text):
        """Fala OTIMIZADA - VOZ INFANTIL FLUIDA"""
        # SEMPRE mostrar no terminal
        print(f"🗣️ {self.blob_name or 'BLOB'}: {text}")
        
        # Atualizar interface se existir
        if hasattr(self.app, 'update_conversation'):
            try:
                self.app.update_conversation(f"🗣️ {self.blob_name or 'BLOB'}: {text}")
            except:
                pass
        
        # MÉTODO RÁPIDO E DIRETO - SEM TRAVAMENTOS
        print(f"🔊 Falando...")
        
        # ⭐ MÉTODO 1: Windows SAPI com configuração INFANTIL (mais rápido) ⭐
        try:
            import win32com.client
            sapi = win32com.client.Dispatch("SAPI.SpVoice")
            
            # 🎈 CONFIGURAÇÕES ESPECIAIS PARA VOZ INFANTIL 🎈
            sapi.Volume = 100           # Volume máximo para clareza
            sapi.Rate = 2               # Velocidade um pouco mais rápida (mais animada)
            
            # Tentar selecionar voz feminina se disponível
            voices = sapi.GetVoices()
            for voice in voices:
                voice_name = str(voice.GetDescription()).lower()
                if 'maria' in voice_name or 'female' in voice_name:
                    sapi.Voice = voice
                    break
            
            # Adicionar pequenas pausas para fluidez
            text_fluido = text.replace('.', '... ').replace('!', '! ').replace('?', '? ')
            
            sapi.Speak(text_fluido)
            print("✅ Voz INFANTIL executada via SAPI!")
            return
            
        except Exception as e:
            print(f"❌ SAPI falhou: {e}")
        
        # MÉTODO 2: pyttsx3 com configuração infantil (backup)
        try:
            import pyttsx3
            engine = pyttsx3.init()
            
            # Configurações para voz mais infantil e fluida
            engine.setProperty('rate', 190)    # Mais rápida e animada
            engine.setProperty('volume', 1.0)  # Volume máximo
            
            # Tentar usar voz feminina
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'maria' in voice.name.lower() or 'female' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            engine.say(text)
            engine.runAndWait()
            engine.stop()
            del engine
            print("✅ Voz INFANTIL executada via pyttsx3!")
            return
            
        except Exception as e:
            print(f"❌ pyttsx3 falhou: {e}")
        
        # MÉTODO 3: PowerShell simples (último recurso com timeout curto)
        try:
            import subprocess
            text_clean = text.replace('"', "'").replace("'", "")[:100]  # Limitar texto
            
            ps_command = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text_clean}")'
            
            subprocess.run(['powershell', '-Command', ps_command], 
                         timeout=5, capture_output=True)  # Timeout de 5 segundos
            print("✅ Voz executada via PowerShell!")
            return
            
        except Exception as e:
            print(f"❌ PowerShell falhou: {e}")
        
        print("❌ Todos os métodos falharam - usando apenas texto")
        
        # Aguardar início da fala para sincronizar
        time.sleep(0.1)
    
    # Métodos auxiliares (simplificados para economizar espaço)
    def _is_naming_blob(self, text): 
        """Verifica se o usuário está dando um nome ao BLOB"""
        naming_keywords = ['nome', 'chame', 'chamo', 'chamar', 'bob', 'seja']
        return any(word in text.lower() for word in naming_keywords)
    
    def _extract_blob_name(self, text): 
        """Extrai o nome do BLOB do texto"""
        text_lower = text.lower()
        
        # Padrões de nomeação
        import re
        
        # Padrão 1: "seu nome é [nome]"
        match = re.search(r'nome\s+é\s+(\w+)', text_lower)
        if match:
            nome = match.group(1).title()
        # Padrão 2: "te chamo de [nome]"
        elif 'chamo' in text_lower:
            words = text_lower.split()
            if 'de' in words:
                idx = words.index('de')
                if idx + 1 < len(words):
                    nome = words[idx + 1].title()
                else:
                    nome = None
            else:
                nome = words[-1].title()
        # Padrão 3: simplesmente "Bob" ou nome direto
        elif any(word in text_lower for word in ['bob', 'seja']):
            if 'bob' in text_lower:
                nome = "Bob"
            else:
                words = text.split()
                nome = words[-1] if words else None
        else:
            # Pegar última palavra como nome
            words = text.split()
            nome = words[-1] if words else None
        
        if nome and len(nome) > 1:
            self.blob_name = nome
            self.memory.save_preference('blob_name', nome)
            
            # Sincronizar com IA Ultra Avançada
            if self.ultra_ai:
                self.ultra_ai.assistant_name = nome
                self.ultra_ai.creativity_engine.assistant_name = nome
                self.memory.save_preference('assistant_name', nome)
            
            self.speak(f"Que nome lindo! Agora sou {nome}! Muito prazer!")
            print(f"🤖 BLOB agora se chama: {nome}")
        else:
            self.speak("Hmm, não consegui entender o nome. Pode repetir?")
    def _handle_name_changes(self, text): 
        """Lida com mudanças de nome e perguntas sobre nome"""
        # Perguntando qual é o nome do BLOB
        if any(phrase in text for phrase in ['como se chama', 'qual seu nome', 'como você se chama', 'seu nome é']):
            if self.blob_name:
                self.speak(f"Meu nome é {self.blob_name}! Você me deu esse nome lindo!")
            else:
                self.speak("Ainda não tenho nome... que tal me dar um nome especial?")
            return True
        
        # Mudando nome do BLOB
        if any(phrase in text for phrase in ['novo nome', 'mudar nome', 'agora se chama', 'nome será']):
            # Extrair novo nome
            words = text.split()
            if len(words) >= 2:
                novo_nome = words[-1].title()
                if len(novo_nome) > 1:
                    old_name = self.blob_name or "BLOB"
                    self.blob_name = novo_nome
                    self.memory.save_preference('blob_name', novo_nome)
                    
                    # Sincronizar com IA Ultra Avançada
                    if self.ultra_ai:
                        self.ultra_ai.assistant_name = novo_nome
                        self.ultra_ai.creativity_engine.assistant_name = novo_nome
                        self.memory.save_preference('assistant_name', novo_nome)
                    
                    self.speak(f"Perfeito! Agora não sou mais {old_name}, sou {novo_nome}!")
                    return True
        
        return False
    
    def _handle_user_introduction(self, text):
        """Detecta quando o usuário se apresenta e armazena seu nome"""
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
                            # Armazena o nome do usuário no banco
                            self.memory.save_preference('user_name', nome)
                            
                            # Atualiza o nome do usuário na memória
                            self.user_name = nome
                            
                            print(f"[DEBUG] Nome do usuário detectado: {nome}")
                            
                            # Resposta personalizada
                            responses = [
                                f"Prazer em te conhecer, {nome}! Que nome lindo!",
                                f"Oi {nome}! Muito prazer! Agora posso te chamar pelo nome!",
                                f"Legal, {nome}! Vou lembrar do seu nome! Prazer te conhecer!",
                                f"Que alegria, {nome}! Agora somos amigos de verdade!",
                                f"Olá {nome}! Adorei saber seu nome! Vamos ser grandes amigos!"
                            ]
                            
                            import random
                            response = random.choice(responses)
                            self.speak(response)
                            
                            # Salvar interação na memória
                            self._save_interaction("user_introduction", f"Usuario se apresentou como: {nome}")
                            
                            return True
                            
                except Exception as e:
                    print(f"[ERROR] Erro ao processar nome do usuário: {e}")
        
        return False
    
    def _get_user_name(self):
        """Retorna o nome do usuário ou None se não foi definido"""
        return self.memory.get_preference('user_name')
    
    def _get_personalized_greeting(self):
        """Retorna uma saudação personalizada com o nome do usuário se disponível"""
        user_name = self._get_user_name()
        if user_name:
            greetings = [
                f"Oi {user_name}!",
                f"Olá {user_name}!",
                f"E aí {user_name}!",
                f"Oi {user_name}, como você está?",
                f"Olá {user_name}, que bom te ver!"
            ]
            import random
            return random.choice(greetings)
        else:
            return "Olá!"
    
    def _handle_user_name_question(self, text):
        """Detecta quando usuário pergunta sobre seu próprio nome"""
        text_lower = text.lower()
        
        # Padrões para detectar pergunta sobre o nome do usuário
        user_name_questions = [
            'qual é o meu nome', 'qual o meu nome', 'qual meu nome',
            'como eu me chamo', 'como me chamo', 'meu nome é qual',
            'você sabe meu nome', 'sabe qual é meu nome', 'lembra do meu nome',
            'qual é meu nome', 'me diz meu nome', 'fala meu nome',
            'como você me chama', 'como me chama você'
        ]
        
        if any(pattern in text_lower for pattern in user_name_questions):
            user_name = self._get_user_name()
            
            if user_name:
                # Usuário já se apresentou, responder com o nome
                responses = [
                    f"Seu nome é {user_name}! Como eu poderia esquecer?",
                    f"Você se chama {user_name}! Lembro perfeitamente!",
                    f"Claro que lembro! Você é {user_name}!",
                    f"{user_name}! Esse é seu nome lindo!",
                    f"Você é {user_name}, não é mesmo?"
                ]
                
                import random
                response = random.choice(responses)
                self.speak(response)
                
                # Salvar interação na memória
                self._save_interaction("user_name_question", f"Usuario perguntou seu nome, respondi: {user_name}")
                return True
            else:
                # Usuário não se apresentou ainda
                responses = [
                    "Não sei! Qual é o seu nome? Adoraria te conhecer melhor!",
                    "Ainda não me disse! Como você se chama?",
                    "Não sei qual é seu nome... Pode me contar?",
                    "Você ainda não se apresentou! Qual é seu nome?",
                    "Hm... não sei! Me conta aí, como você se chama?",
                    "Ainda não me falou! Qual é o seu nome? Quero saber!"
                ]
                
                import random
                response = random.choice(responses)
                self.speak(response)
                
                # Salvar interação na memória
                self._save_interaction("user_name_unknown", "Usuario perguntou seu nome mas nao se apresentou")
                return True
        
        return False
    
    def _save_interaction(self, interaction_type, description):
        """Salva uma interação na memória para histórico"""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Usar o sistema de conversas do MemoryDatabase com assinatura correta
            user_input = f"[{interaction_type}]"
            blob_response = description
            
            self.memory.save_conversation(user_input, blob_response, "neutro", "alegre", 70)
            
            print(f"[DEBUG] Interação salva: {interaction_type} - {description}")
            
        except Exception as e:
            print(f"[ERROR] Erro ao salvar interação: {e}")
    
    def _get_recent_interactions(self, limit=5):
        """Recupera interações recentes para contexto"""
        try:
            recent_conversations = self.memory.get_recent_conversations(limit)
            interactions = []
            
            for conv in recent_conversations:
                # conv deve ter: (id, user_input, blob_response, timestamp, user_emotion, blob_emotion, mood_level)
                if len(conv) >= 3 and conv[1].startswith('['):
                    interaction_type = conv[1].strip('[]')
                    description = conv[2]
                    interactions.append({
                        'type': interaction_type,
                        'description': description,
                        'timestamp': conv[3] if len(conv) > 3 else None
                    })
            
            return interactions
            
        except Exception as e:
            print(f"[ERROR] Erro ao recuperar interações: {e}")
            return []
    
    def _handle_learned_patterns(self, text): return False
    def _is_asking_about_status(self, text): 
        """Verifica se está perguntando sobre status ou nome"""
        status_questions = [
            'como está', 'como vai', 'tudo bem', 'como se sente',
            'como se chama', 'qual seu nome', 'como você se chama',
            'qual é seu nome', 'como te chamo', 'seu nome é',
            'qual o seu nome', 'qual nome', 'como é seu nome',
            'me diz seu nome', 'fala seu nome'
        ]
        return any(phrase in text for phrase in status_questions)
    def _respond_about_status_ultra(self, user_emotion, text=""): 
        """Responde sobre status ou nome do BLOB"""
        # Lista mais específica para detectar perguntas sobre nome
        name_keywords = [
            'nome', 'chama', 'como te chamo', 'qual seu nome', 
            'qual é seu nome', 'qual o seu nome', 'como você se chama',
            'como se chama', 'seu nome é', 'me diz seu nome'
        ]
        
        # Se está perguntando sobre nome
        is_asking_name = any(phrase in text.lower() for phrase in name_keywords)
        
        if is_asking_name:
            if self.blob_name:
                responses = [
                    f"Eu sou a {self.blob_name}! Você gosta do nome?",
                    f"Me chamo {self.blob_name}! Que nome lindo, né?",
                    f"Meu nome é {self.blob_name}! Foi você que escolheu!",
                    f"Sou a {self.blob_name}! Gostou do nome?"
                ]
                response = random.choice(responses)
                print(f"🔍 Detectou pergunta sobre nome: '{text}' -> Resposta: '{response}'")
                self.speak(response)
            else:
                self.speak("Ainda não tenho nome... que tal me dar um nome legal?")
        else:
            # Resposta sobre status/humor
            mood = self.blob.mood_level
            if mood > 80:
                responses = ["Estou ótima! Super animada!", "Estou muito bem! E você?"]
            elif mood > 60:
                responses = ["Estou muito bem! Feliz da vida!", "Estou ótimo! Como você está?"]
            elif mood > 40:
                responses = ["Estou bem, obrigado! E você?", "Tudo tranquilo! Como vai você?"]
            else:
                responses = ["Estou um pouquinho para baixo...", "Poderia estar melhor..."]
            
            response = random.choice(responses)
            print(f"🔍 Detectou pergunta sobre status: '{text}' -> Resposta: '{response}'")
            self.speak(response)
    def _is_greeting(self, text): return any(g in text for g in ['oi', 'olá', 'hey'])
    def _respond_greeting_ultra(self, user_emotion): 
        greetings = [
            "Oi! Que bom te ver!",
            "Olá! Tudo bem?",
            "Oi querido! Como você está?",
            "Oi! Que alegria você aparecer!"
        ]
        self.speak(random.choice(greetings))
    def _is_farewell(self, text): return any(f in text for f in ['tchau', 'até', 'bye'])
    def _respond_farewell_ultra(self, user_emotion): self.speak("Tchau! Foi ótimo conversar!")

class AppUltraAvancada:
    """Interface ultra moderna e responsiva"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 BLOB ULTRA AVANÇADO v2.0 - IA Conversacional Suprema")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0D1117')  # Tema escuro moderno
        
        # Sistemas avançados
        self.memory_db = MemoryDatabase()
        self.emotional_ai = EmotionalAI(self.memory_db)
        
        # Canvas principal (maior e mais detalhado)
        self.canvas = tk.Canvas(
            self.root,
            width=1400,
            height=600,
            bg='#161B22',
            highlightthickness=0
        )
        self.canvas.pack(pady=15)
        
        # Grid futurístico
        self.draw_futuristic_grid()
        
        # BLOB ultra avançado
        self.blob = BLOBUltraAvancado(self.canvas, x=700, y=300)
        
        # Sistema de voz ultra avançado
        self.voice = VozUltraAvancada(self.blob, self, self.memory_db, self.emotional_ai)
        
        # Referência ao sistema de IA para confirmação de nomes
        if hasattr(self.voice, 'ultra_ai'):
            self.voice.ai_system = self.voice.ultra_ai
        
        # Interface moderna
        self.setup_modern_ui()
        self.setup_advanced_panels()
        
        # Iniciar sistemas
        self.update_all_displays()
        
        print("🚀 BLOB ULTRA AVANÇADO v2.0 INICIALIZADO!")
    
    def draw_futuristic_grid(self):
        """Grid futurístico com efeito neon"""
        # Linhas horizontais
        for i in range(0, 600, 40):
            self.canvas.create_line(
                0, i, 1400, i,
                fill='#21262D', width=1
            )
        
        # Linhas verticais
        for i in range(0, 1400, 40):
            self.canvas.create_line(
                i, 0, i, 600,
                fill='#21262D', width=1
            )
        
        # Pontos de intersecção brilhantes
        for x in range(0, 1400, 120):
            for y in range(0, 600, 120):
                self.canvas.create_oval(
                    x-2, y-2, x+2, y+2,
                    fill='#58A6FF', outline=''
                )
    
    def setup_modern_ui(self):
        """Interface ultra moderna"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#0D1117')
        main_frame.pack(fill='x', padx=20, pady=10)
        
        # Título futurístico
        title_frame = tk.Frame(main_frame, bg='#0D1117')
        title_frame.pack(pady=10)
        
        tk.Label(
            title_frame,
            text="🚀 BLOB ULTRA AVANÇADO v2.0",
            font=('Consolas', 20, 'bold'),
            bg='#0D1117', fg='#58A6FF'
        ).pack()
        
        tk.Label(
            title_frame,
            text="IA Conversacional • Memória Persistente • Aprendizado Emocional • 🔍 Busca Inteligente na Internet",
            font=('Consolas', 10),
            bg='#0D1117', fg='#7D8590'
        ).pack()
        
        # Botão de microfone futurístico
        self.mic_frame = tk.Frame(main_frame, bg='#0D1117')
        self.mic_frame.pack(pady=20)
        
        # Frame para botões do microfone e configurações
        buttons_frame = tk.Frame(self.mic_frame, bg='#0D1117')
        buttons_frame.pack()
        
        self.mic_button = tk.Button(
            buttons_frame,
            text="🎤",
            font=('Arial', 28),
            bg='#238636', fg='white',
            width=8, height=3,
            relief='flat', bd=0,
            command=self.toggle_microphone,
            cursor='hand2'
        )
        self.mic_button.pack(side='left', padx=10)
        
        # Botão de configurações
        self.config_button = tk.Button(
            buttons_frame,
            text="⚙️",
            font=('Arial', 20),
            bg='#6F42C1', fg='white',
            width=4, height=2,
            relief='flat', bd=0,
            command=self.open_settings,
            cursor='hand2'
        )
        self.config_button.pack(side='left', padx=10)
        
        tk.Label(
            self.mic_frame,
            text="Sistema de Escuta Inteligente - Clique e Fale",
            font=('Consolas', 12, 'bold'),
            bg='#0D1117', fg='#F0F6FC'
        ).pack(pady=5)
        
        self.voice_status_label = tk.Label(
            self.mic_frame,
            text="💤 Sistema aguardando...",
            font=('Consolas', 10),
            bg='#0D1117', fg='#7D8590'
        )
        self.voice_status_label.pack()
    
    def setup_advanced_panels(self):
        """Painéis avançados de informação"""
        # Frame para painéis
        panels_frame = tk.Frame(self.root, bg='#0D1117')
        panels_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Painel esquerdo - Status Emocional
        self.setup_emotion_panel(panels_frame)
        
        # Painel central - Conversação
        self.setup_conversation_panel(panels_frame)
        
        # Painel direito - Dados Avançados
        self.setup_data_panel(panels_frame)
    
    def setup_emotion_panel(self, parent):
        """Painel de status emocional avançado"""
        self.emotion_panel = tk.Frame(
            parent, bg='#161B22', relief='solid', bd=1
        )
        self.emotion_panel.pack(side='left', fill='y', padx=(0,10))
        
        tk.Label(
            self.emotion_panel,
            text="🧠 SISTEMA EMOCIONAL",
            font=('Consolas', 12, 'bold'),
            bg='#161B22', fg='#58A6FF'
        ).pack(pady=10)
        
        # Labels que serão atualizados
        self.emotion_label = tk.Label(
            self.emotion_panel, text="", font=('Consolas', 10),
            bg='#161B22', fg='#F0F6FC'
        )
        self.emotion_label.pack(pady=5)
        
        self.mood_progress = ttk.Progressbar(
            self.emotion_panel, length=200, mode='determinate'
        )
        self.mood_progress.pack(pady=5)
        
        self.relationship_label = tk.Label(
            self.emotion_panel, text="", font=('Consolas', 9),
            bg='#161B22', fg='#7D8590'
        )
        self.relationship_label.pack(pady=5)
    
    def setup_conversation_panel(self, parent):
        """Painel de conversação central"""
        self.conv_panel = tk.Frame(
            parent, bg='#161B22', relief='solid', bd=1
        )
        self.conv_panel.pack(side='left', fill='both', expand=True, padx=10)
        
        tk.Label(
            self.conv_panel,
            text="💬 HISTÓRICO DE CONVERSAS INTELIGENTES",
            font=('Consolas', 12, 'bold'),
            bg='#161B22', fg='#58A6FF'
        ).pack(pady=10)
        
        # Área de texto futurística
        self.conv_text = tk.Text(
            self.conv_panel,
            width=60, height=20,
            wrap=tk.WORD,
            bg='#0D1117',
            fg='#F0F6FC',
            font=('Consolas', 9),
            insertbackground='#58A6FF',
            relief='flat', bd=0
        )
        
        scrollbar = ttk.Scrollbar(
            self.conv_panel, orient="vertical",
            command=self.conv_text.yview
        )
        self.conv_text.configure(yscrollcommand=scrollbar.set)
        
        self.conv_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mensagem de boas-vindas avançada
        welcome_msg = """🚀 BLOB ULTRA AVANÇADO v2.0 INICIADO!

🧠 Funcionalidades Avançadas Ativas:
• Memória persistente entre sessões
• IA emocional que evolui com você  
• Sistema de aprendizado inteligente
• Análise profunda de sentimentos
• Funcionalidades práticas integradas
• 🔍 BUSCA INTELIGENTE NA INTERNET!

💡 Experimente comandos avançados:
• "Conte uma piada" • "Me ensina algo"
• "Calcule 25 + 37" • "Me lembre de algo"
• "Como está o tempo?" • "Meu sonho é..."

🔍 Faça perguntas que ele vai buscar na internet:
• "Por que o céu é azul?" • "O que é inteligência artificial?"
• "Como funciona o coração?" • "Onde fica o Japão?"
• "Quando foi descoberto o Brasil?" • "Quem foi Einstein?"

🎤 Clique no microfone e comece sua jornada!"""
        
        self.update_conversation(welcome_msg)
    
    def setup_data_panel(self, parent):
        """Painel de dados avançados"""
        self.data_panel = tk.Frame(
            parent, bg='#161B22', relief='solid', bd=1
        )
        self.data_panel.pack(side='right', fill='y', padx=(10,0))
        
        tk.Label(
            self.data_panel,
            text="📊 DADOS AVANÇADOS",
            font=('Consolas', 12, 'bold'),
            bg='#161B22', fg='#58A6FF'
        ).pack(pady=10)
        
        self.data_labels = {}
        
        # Criar labels para diferentes métricas
        data_types = [
            'Conversas Hoje', 'Nível Amizade', 'Humor Médio',
            'Tópico Favorito', 'Última Interação', 'Tempo Online'
        ]
        
        for data_type in data_types:
            label = tk.Label(
                self.data_panel,
                text=f"{data_type}: -",
                font=('Consolas', 9),
                bg='#161B22', fg='#7D8590'
            )
            label.pack(pady=2, anchor='w')
            self.data_labels[data_type] = label
    
    def toggle_microphone(self):
        """Toggle do microfone moderno - MELHORADO"""
        if not self.voice.enabled:
            self.update_voice_status("❌ Sistema de voz indisponível")
            return
        
        try:
            if self.voice.is_listening:
                # Parar escuta
                self.voice.is_listening = False
                self.update_mic_button_state(False)
                self.update_voice_status("⏹️ Escuta interrompida pelo usuário")
            else:
                # Iniciar escuta
                self.update_voice_status("🎤 Iniciando escuta...")
                success = self.voice.start_listening_session()
                if success:
                    self.update_mic_button_state(True)
                    self.update_voice_status("🎤 Ouvindo... fale naturalmente!")
                else:
                    self.update_voice_status("❌ Falha ao iniciar escuta")
                    self.update_mic_button_state(False)
        except Exception as e:
            print(f"❌ Erro no toggle do microfone: {e}")
            self.update_voice_status("❌ Erro no sistema de microfone")
            self.update_mic_button_state(False)
    
    def update_mic_button_state(self, is_active):
        """Atualiza estado do botão moderno"""
        if is_active:
            self.mic_button.config(
                bg='#DA3633', text="🔴", relief='sunken'
            )
        else:
            self.mic_button.config(
                bg='#238636', text="🎤", relief='flat'
            )
    
    def update_voice_status(self, status):
        """Atualiza status com cores modernas"""
        self.voice_status_label.config(text=status)
        
        if "Preparando" in status or "Calibrando" in status:
            self.mic_button.config(bg='#F85149', text="⚙️")
        elif "Fale" in status:
            self.update_mic_button_state(True)
        elif "Processando" in status:
            self.mic_button.config(bg='#1F6FEB', text="🧠")
        elif "Falando" in status:
            self.mic_button.config(bg='#FB8500', text="🗣️")
        else:
            self.update_mic_button_state(False)
    
    def open_settings(self):
        """Abre janela de configurações do BLOB"""
        try:
            # Importar o módulo de configurações
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))
            from settings_manager import SettingsManager
            
            # Criar e abrir configurações
            settings = SettingsManager()
            settings.open_settings_window(parent=self.root)
            
            print("⚙️ Janela de configurações aberta!")
            
        except Exception as e:
            print(f"❌ Erro ao abrir configurações: {e}")
            self.update_voice_status("❌ Erro ao abrir configurações")
    
    def update_conversation(self, message):
        """Atualiza conversa com timestamp"""
        timestamp = datetime.now().strftime("%H:%M")
        formatted_message = f"[{timestamp}] {message}\n\n"
        
        self.conv_text.insert(tk.END, formatted_message)
        self.conv_text.see(tk.END)
    
    def update_all_displays(self):
        """Atualiza todos os displays continuamente"""
        try:
            # Atualizar painel emocional
            mood_info = self.blob.get_current_mood_info()
            
            emotion_text = f"Emoção: {mood_info['emotion'].replace('_', ' ').title()}\nHumor: {mood_info['mood_level']:.1f}/100"
            self.emotion_label.config(text=emotion_text)
            
            self.mood_progress['value'] = mood_info['mood_level']
            
            relationship_text = f"Amizade: {self.voice.relationship_level:.1f}/100"
            self.relationship_label.config(text=relationship_text)
            
            # Atualizar dados avançados
            self.update_data_labels()
            
        except Exception as e:
            print(f"Erro na atualização: {e}")
        
        # Reagendar
        self.root.after(1000, self.update_all_displays)
    
    def update_data_labels(self):
        """Atualiza labels de dados"""
        try:
            # Dados simulados/reais
            data_values = {
                'Conversas Hoje': len(self.voice.conversation_context),
                'Nível Amizade': f"{self.voice.relationship_level:.1f}/100",
                'Humor Médio': f"{self.blob.mood_level:.1f}",
                'Tópico Favorito': "Conversas",
                'Última Interação': "Agora",
                'Tempo Online': "Contínuo"
            }
            
            for key, value in data_values.items():
                if key in self.data_labels:
                    self.data_labels[key].config(text=f"{key}: {value}")
        except:
            pass
    
    def show_name_confirmation(self, proposed_name, ai_response):
        """Mostra botões de confirmação para mudança de nome"""
        # Criar frame de confirmação
        self.confirmation_frame = tk.Frame(self.root, bg='#0D1117')
        self.confirmation_frame.pack(pady=20)
        
        # Título da confirmação
        tk.Label(
            self.confirmation_frame,
            text=ai_response,
            font=('Consolas', 14, 'bold'),
            bg='#0D1117', fg='#F85149'
        ).pack(pady=10)
        
        # Frame para botões
        buttons_frame = tk.Frame(self.confirmation_frame, bg='#0D1117')
        buttons_frame.pack()
        
        # Botão SIM
        yes_button = tk.Button(
            buttons_frame,
            text="✅ SIM",
            font=('Consolas', 12, 'bold'),
            bg='#238636', fg='white',
            width=10, height=2,
            relief='flat', bd=0,
            command=lambda: self.confirm_name_change(proposed_name, True),
            cursor='hand2'
        )
        yes_button.pack(side='left', padx=10)
        
        # Botão NÃO
        no_button = tk.Button(
            buttons_frame,
            text="❌ NÃO",
            font=('Consolas', 12, 'bold'),
            bg='#DA3633', fg='white',
            width=10, height=2,
            relief='flat', bd=0,
            command=lambda: self.confirm_name_change(proposed_name, False),
            cursor='hand2'
        )
        no_button.pack(side='left', padx=10)
        
        # Texto explicativo
        tk.Label(
            self.confirmation_frame,
            text=f"Seu BLOB vai se chamar {proposed_name}?",
            font=('Consolas', 10),
            bg='#0D1117', fg='#7D8590'
        ).pack(pady=5)
    
    def confirm_name_change(self, proposed_name, confirmed):
        """Confirma ou rejeita mudança de nome"""
        # Remover frame de confirmação
        if hasattr(self, 'confirmation_frame'):
            self.confirmation_frame.destroy()
            delattr(self, 'confirmation_frame')
        
        # Processar confirmação através da IA
        if hasattr(self.voice, 'ai_system'):
            result = self.voice.ai_system.confirm_name_change(proposed_name, confirmed)
            
            # Atualizar conversa com resultado
            self.update_conversation(f"🤖 BLOB: {result['response']}")
            
            # Falar se voz estiver ativa
            if self.voice.enabled:
                self.voice.speak_text(result['response'])
        else:
            # Fallback se não tiver IA
            if confirmed:
                response = f"Agora meu nome é {proposed_name}! Gostei do novo nome!"
            else:
                response = "Entendi! Continuo sendo um BLOB sem nome específico."
            
            self.update_conversation(f"🤖 BLOB: {response}")
            
            if self.voice.enabled:
                self.voice.speak_text(response)
    
    def handle_ai_response(self, ai_response):
        """Manipula resposta da IA verificando se é solicitação de nome"""
        if isinstance(ai_response, dict):
            if ai_response.get('type') == 'name_change_request':
                # Mostrar confirmação de nome
                self.show_name_confirmation(
                    ai_response['new_name'], 
                    ai_response['response']
                )
                return True
        return False
    
    def run(self):
        """Executa a aplicação ultra avançada"""
        print("🚀 BLOB ULTRA AVANÇADO v2.0 EM EXECUÇÃO!")
        print("🧠 IA Emocional • 💾 Memória Persistente • 🎯 Funcionalidades Práticas")
        print("⚡ Sistema de escuta inteligente ativo!")
        self.root.mainloop()

def main():
    """Função principal ultra avançada"""
    try:
        print("🚀 Iniciando BLOB ULTRA AVANÇADO v2.0...")
        print("📋 Sistemas Avançados:")
        print("   🧠 IA Emocional com evolução de personalidade")
        print("   💾 Banco de dados SQLite para memória persistente")
        print("   🎯 Módulos de funcionalidade (piadas, cálculos, lembretes)")
        print("   🎨 Interface moderna com tema futurístico")
        print("   📊 Análise emocional avançada do usuário")
        print("   🤝 Sistema de evolução de relacionamento")
        print("   🧩 Aprendizado de padrões conversacionais")
        print("   🔍 BUSCA INTELIGENTE NA INTERNET!")
        print()
        
        if not VOICE_AVAILABLE:
            print("⚠️ AVISO: Sistema de voz limitado!")
            print("📦 Para funcionalidade completa: pip install speechrecognition pyttsx3")
            print("🎮 Você ainda pode ver todas as animações e funcionalidades visuais!")
            print()
        
        if not WEB_SEARCH_AVAILABLE:
            print("⚠️ AVISO: Busca inteligente desabilitada!")
            print("📦 Para busca na internet: pip install requests beautifulsoup4")
            print("🔍 Instale para que o BLOB possa pesquisar qualquer coisa na internet!")
            print()
        
        app = AppUltraAvancada()
        app.run()
        
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()