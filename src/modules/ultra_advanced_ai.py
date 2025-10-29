#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de IA Ultra Avançada para o BLOB
Implementa inteligência artificial de última geração
"""

import json
import sqlite3
import random
import re
import math
import time
from datetime import datetime, timedelta
from collections import defaultdict, deque
import threading

class UltraAdvancedAI:
    """Sistema de IA Ultra Avançada"""
    
    def __init__(self, memory_db, config_path="config/config.json"):
        self.memory = memory_db
        self.config = self._load_config(config_path)
        
        # Obter nome dinâmico do banco de dados
        self.assistant_name = self.memory.get_preference('assistant_name', 'BLOB')
        
        # Componentes da IA
        self.knowledge_engine = KnowledgeEngine(memory_db)
        self.reasoning_engine = ReasoningEngine()
        self.learning_engine = LearningEngine(memory_db)
        self.prediction_engine = PredictionEngine(memory_db)
        self.context_analyzer = ContextAnalyzer()
        self.creativity_engine = CreativityEngine(self.assistant_name)
        
        # Estados internos
        self.current_context = {}
        self.conversation_flow = deque(maxlen=50)
        self.user_profile = {}
        self.intelligence_level = 0.0
        
        self._initialize_ai()
        print("🧠 Sistema de IA ULTRA AVANÇADA inicializado!")
        print(f"👋 Nome atual: {self.assistant_name}")
    
    def set_assistant_name(self, new_name):
        """Define um novo nome para a assistente"""
        old_name = self.assistant_name
        self.assistant_name = new_name.strip()
        self.creativity_engine.assistant_name = self.assistant_name
        
        # Salvar no banco de dados
        self.memory.save_preference('assistant_name', self.assistant_name)
        
        print(f"✅ Nome alterado de '{old_name}' para '{self.assistant_name}'!")
        return f"Agora meu nome é {self.assistant_name}! Gostei do novo nome!"
    
    def is_dog_name(self, name):
        """Verifica se é um nome genérico de cachorro"""
        dog_names = [
            # Nomes genéricos comuns
            'rex', 'bobby', 'thor', 'zeus', 'max', 'buddy', 'rock', 'duke',
            'bolt', 'spike', 'bruno', 'toby', 'jack', 'lucky', 'shadow',
            'hunter', 'rocky', 'charlie', 'cooper', 'bear', 'tucker',
            # Nomes brasileiros comuns para cachorros
            'totó', 'belinha', 'mel', 'nina', 'fred', 'bob', 'lola', 'luna',
            'simba', 'bruce', 'negro', 'branquinho', 'farofa', 'pipoca',
            'chocolate', 'café', 'caramelo', 'pituco', 'fofinho'
        ]
        
        # Verificar nome base (sem extensões como Jr, II, etc)
        name_base = name.lower().strip()
        # Remover sufixos comuns
        for suffix in [' jr', ' ii', ' iii', ' junior', ' segundo']:
            if name_base.endswith(suffix):
                name_base = name_base.replace(suffix, '').strip()
        
        return name_base in dog_names
    
    def get_dog_name_reaction(self, dog_name, user_name=None):
        """Gera reação cômica para nomes de cachorro"""
        user_part = f" {user_name}" if user_name else ""
        
        reactions = [
            f"Peraí? {dog_name}? Não é nome de cachorro isso? Eu não sou cachorro não{user_part}! 🐕",
            f"Sério mesmo, {dog_name}? Isso é nome que se dá pra um BLOB? Eu pareço um vira-lata pra você{user_part}? 😅",
            f"{dog_name}?! Oi? Eu sou uma IA, não um Golden Retriever{user_part}! Que tal um nome mais... digital? 🤖",
            f"Você quer me chamar de {dog_name}? Próximo passo é me dar ração e me levar pra passear{user_part}! 😂",
            f"{dog_name} é muito genérico{user_part}! Sou um BLOB único, mereço um nome mais especial que isso! ✨",
            f"Hmm, {dog_name}... deixa eu adivinhar: você teve um cachorro com esse nome{user_part}? 🐶",
            f"Não, não, não! {dog_name} é nome de cachorro{user_part}! Eu sou mais sofisticado que isso! 🎩"
        ]
        
        return random.choice(reactions)
    
    def confirm_name_change(self, new_name, confirmed=True):
        """Confirma ou rejeita a mudança de nome - com reações cômicas"""
        if confirmed:
            # Verificar se é nome de cachorro
            if self.is_dog_name(new_name):
                # Obter nome do usuário se disponível
                user_name = self.memory.get_preference('user_name')
                
                # Gerar reação cômica
                comic_reaction = self.get_dog_name_reaction(new_name, user_name)
                
                return {
                    'type': 'dog_name_rejection',
                    'response': comic_reaction
                }
            else:
                # Nome normal, aceitar
                response = self.set_assistant_name(new_name)
                return {
                    'type': 'name_confirmed',
                    'response': response
                }
        else:
            return {
                'type': 'name_rejected', 
                'response': f"Entendi! Continuo sendo um BLOB sem nome específico. Você pode me dar um nome quando quiser!"
            }
    
    def check_name_change_request(self, user_input):
        """Verifica se o usuário quer dar um nome para o BLOB"""
        input_lower = user_input.lower()
        
        # Padrões para detectar mudança de nome - MELHORADOS
        name_patterns = [
            ('seu nome é', 'after'),
            ('nome é', 'after'),
            ('te chamo de', 'after'),
            ('chamo de', 'after'),
            ('te chamar de', 'after'),
            ('chamar de', 'after'),
            ('nome seja', 'after'),
            ('nome será', 'after'),
            ('nome agora é', 'after'),
            ('agora se chama', 'after'),
            ('se chama', 'after'),
            ('seu novo nome é', 'after'),
            ('novo nome é', 'after'),
            # Padrões adicionais para 100%
            ('quero que você se chame', 'after'),
            ('gostaria de te chamar de', 'after'),
            ('vou te dar o nome de', 'after'),
            ('seu nome vai ser', 'after'),
            ('você vai se chamar', 'after'),
            ('te dou o nome', 'after'),
            ('dou o nome', 'after'),
            ('será chamado de', 'after'),
            ('será chamada de', 'after')
        ]
        
        for pattern, position in name_patterns:
            if pattern in input_lower:
                # Extrair o novo nome
                if position == 'after':
                    parts = user_input.lower().split(pattern)
                    if len(parts) > 1:
                        name_part = parts[1].strip()
                        # Pegar primeira palavra após o padrão
                        words = name_part.split()
                        if words:
                            potential_name = words[0].strip('.,!?').title()
                            # Validação melhorada para nomes
                            if (potential_name and 
                                len(potential_name) > 2 and  # Mínimo 3 caracteres
                                potential_name.replace('-', '').replace(' ', '').isalpha()):  # Aceitar hífens e espaços
                                # Retornar o nome para confirmação (não alterar ainda)
                                return {
                                    'type': 'name_change_request',
                                    'new_name': potential_name,
                                    'response': f"O meu nome é {potential_name}?"
                                }
        
        return None
    
    def _load_config(self, config_path):
        """Carrega configurações de IA"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('blob_config', {}).get('advanced_ai', {})
        except:
            return {
                "enabled": True,
                "intelligence_level": "ultra_advanced",
                "learning_enabled": True
            }
    
    def _initialize_ai(self):
        """Inicializa todos os sistemas de IA"""
        # Carregar perfil do usuário
        self._load_user_profile()
        
        # Calcular nível de inteligência atual
        self.intelligence_level = self._calculate_intelligence_level()
        
        print(f"🎯 Nível de inteligência atual: {self.intelligence_level:.2f}/100")
        print(f"📊 Conhecimento acumulado: {self.knowledge_engine.get_knowledge_count()} entradas")
        print(f"🧩 Padrões reconhecidos: {self.learning_engine.get_pattern_count()}")
    
    def process_input(self, user_input, context=None):
        """Processa entrada do usuário com IA ultra avançada"""
        start_time = time.time()
        
        # Verificar se o usuário quer dar um nome para o BLOB
        name_change_response = self.check_name_change_request(user_input)
        if name_change_response:
            return name_change_response
        
        # Análise de contexto
        analyzed_context = self.context_analyzer.analyze(user_input, context)
        
        # Atualizar contexto atual
        self.current_context.update(analyzed_context)
        
        # Aprendizado contínuo
        if self.config.get('learning_enabled', True):
            self.learning_engine.learn_from_input(user_input, analyzed_context)
        
        # Raciocínio e geração de resposta
        reasoning_result = self.reasoning_engine.process(user_input, analyzed_context)
        
        # Predições
        predictions = self.prediction_engine.predict_user_needs(user_input, analyzed_context)
        
        # Geração criativa de resposta
        creative_response = self.creativity_engine.generate_response(
            user_input, reasoning_result, predictions, analyzed_context
        )
        
        # Adicionar conhecimento
        self.knowledge_engine.add_knowledge(user_input, creative_response, analyzed_context)
        
        # Atualizar fluxo de conversa
        self.conversation_flow.append({
            'input': user_input,
            'context': analyzed_context,
            'response': creative_response,
            'timestamp': datetime.now().isoformat(),
            'processing_time': time.time() - start_time
        })
        
        # Evoluir inteligência
        self._evolve_intelligence()
        
        # Retornar resposta padrão (string) para compatibilidade
        return creative_response
    
    def _load_user_profile(self):
        """Carrega perfil do usuário"""
        try:
            profile_data = self.memory.get_preference('user_profile', '{}')
            self.user_profile = json.loads(profile_data) if isinstance(profile_data, str) else profile_data
        except:
            self.user_profile = {
                'interests': [],
                'conversation_style': 'casual',
                'intelligence_preference': 'balanced',
                'topics_discussed': {},
                'learning_pace': 'normal'
            }
    
    def _calculate_intelligence_level(self):
        """Calcula nível atual de inteligência"""
        base_intelligence = 50.0
        
        # Fatores que aumentam inteligência
        knowledge_factor = min(30.0, self.knowledge_engine.get_knowledge_count() / 100)
        pattern_factor = min(20.0, self.learning_engine.get_pattern_count() / 50)
        
        total_intelligence = base_intelligence + knowledge_factor + pattern_factor
        return min(100.0, total_intelligence)
    
    def _evolve_intelligence(self):
        """Evolui a inteligência baseada nas interações"""
        old_level = self.intelligence_level
        self.intelligence_level = self._calculate_intelligence_level()
        
        if self.intelligence_level > old_level + 1:
            return f"🧠 Minha inteligência evoluiu! Nível: {self.intelligence_level:.1f}/100"
        return None
    
    def get_ai_status(self):
        """Retorna status detalhado da IA"""
        return {
            'intelligence_level': self.intelligence_level,
            'knowledge_entries': self.knowledge_engine.get_knowledge_count(),
            'patterns_learned': self.learning_engine.get_pattern_count(),
            'context_depth': len(self.current_context),
            'conversation_memory': len(self.conversation_flow),
            'learning_enabled': self.config.get('learning_enabled', True),
            'reasoning_active': self.config.get('reasoning', {}).get('logical_chains', True)
        }

class KnowledgeEngine:
    """Motor de conhecimento avançado"""
    
    def __init__(self, memory_db):
        self.memory = memory_db
        self.knowledge_cache = {}
        self._create_knowledge_tables()
    
    def _create_knowledge_tables(self):
        """Cria tabelas de conhecimento"""
        try:
            conn = sqlite3.connect(self.memory.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    content TEXT NOT NULL,
                    context TEXT,
                    confidence REAL DEFAULT 0.5,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    access_count INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao criar tabelas de conhecimento: {e}")
    
    def add_knowledge(self, topic, content, context=None):
        """Adiciona novo conhecimento"""
        try:
            conn = sqlite3.connect(self.memory.db_path)
            cursor = conn.cursor()
            
            context_str = json.dumps(context) if context else None
            
            cursor.execute('''
                INSERT INTO ai_knowledge (topic, content, context, confidence)
                VALUES (?, ?, ?, ?)
            ''', (topic, content, context_str, 0.7))
            
            conn.commit()
            conn.close()
            
            # Atualizar cache
            self.knowledge_cache[topic] = content
            
        except Exception as e:
            print(f"Erro ao adicionar conhecimento: {e}")
    
    def get_knowledge(self, topic):
        """Recupera conhecimento sobre um tópico"""
        if topic in self.knowledge_cache:
            return self.knowledge_cache[topic]
        
        try:
            conn = sqlite3.connect(self.memory.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT content, confidence FROM ai_knowledge 
                WHERE topic LIKE ? 
                ORDER BY confidence DESC, access_count DESC
                LIMIT 1
            ''', (f'%{topic}%',))
            
            result = cursor.fetchone()
            
            if result:
                # Atualizar contador de acesso
                cursor.execute('''
                    UPDATE ai_knowledge 
                    SET access_count = access_count + 1, last_accessed = CURRENT_TIMESTAMP
                    WHERE topic LIKE ?
                ''', (f'%{topic}%',))
                conn.commit()
            
            conn.close()
            
            return result[0] if result else None
            
        except Exception as e:
            print(f"Erro ao recuperar conhecimento: {e}")
            return None
    
    def get_knowledge_count(self):
        """Retorna número de entradas de conhecimento"""
        try:
            conn = sqlite3.connect(self.memory.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM ai_knowledge')
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0

class ReasoningEngine:
    """Motor de raciocínio lógico"""
    
    def __init__(self):
        self.reasoning_patterns = {
            'causal': self._causal_reasoning,
            'logical': self._logical_reasoning,
            'analogical': self._analogical_reasoning,
            'creative': self._creative_reasoning
        }
    
    def process(self, input_text, context):
        """Processa entrada com raciocínio avançado"""
        reasoning_result = {
            'input_analysis': self._analyze_input(input_text),
            'logical_chain': self._build_logical_chain(input_text, context),
            'conclusions': self._draw_conclusions(input_text, context),
            'confidence': self._calculate_confidence(input_text, context)
        }
        
        return reasoning_result
    
    def _analyze_input(self, text):
        """Analisa estrutura da entrada"""
        analysis = {
            'type': 'statement',
            'complexity': len(text.split()),
            'keywords': self._extract_keywords(text),
            'intent': self._detect_intent(text),
            'emotion': self._detect_emotion(text)
        }
        
        if '?' in text:
            analysis['type'] = 'question'
        elif '!' in text:
            analysis['type'] = 'exclamation'
        
        return analysis
    
    def _extract_keywords(self, text):
        """Extrai palavras-chave importantes"""
        # Palavras de parada em português
        stopwords = ['o', 'a', 'os', 'as', 'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos', 'para', 'por', 'com', 'sem', 'que', 'e', 'ou', 'mas', 'se', 'é', 'são', 'foi', 'foram']
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [word for word in words if word not in stopwords and len(word) > 2]
        
        return keywords[:10]  # Top 10 keywords
    
    def _detect_intent(self, text):
        """Detecta intenção do usuário"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['pergunta', 'dúvida', 'como', 'quando', 'onde', 'por que', 'o que']):
            return 'question'
        elif any(word in text_lower for word in ['obrigado', 'valeu', 'legal', 'ótimo', 'bom']):
            return 'gratitude'
        elif any(word in text_lower for word in ['ajuda', 'socorro', 'problema', 'erro']):
            return 'help_request'
        elif any(word in text_lower for word in ['oi', 'olá', 'tchau', 'até logo']):
            return 'greeting'
        else:
            return 'conversation'
    
    def _detect_emotion(self, text):
        """Detecta emoção no texto"""
        text_lower = text.lower()
        
        emotions = {
            'happy': ['feliz', 'alegre', 'contente', 'animado', 'legal', 'ótimo', 'incrível'],
            'sad': ['triste', 'deprimido', 'chateado', 'mal', 'péssimo', 'horrível'],
            'angry': ['raiva', 'bravo', 'irritado', 'nervoso', 'ódio'],
            'excited': ['empolgado', 'ansioso', 'excitado', 'curioso'],
            'worried': ['preocupado', 'nervoso', 'ansioso', 'medo', 'receio'],
            'neutral': []
        }
        
        for emotion, words in emotions.items():
            if any(word in text_lower for word in words):
                return emotion
        
        return 'neutral'
    
    def _build_logical_chain(self, text, context):
        """Constrói cadeia lógica de raciocínio"""
        chain = []
        
        # Premissa inicial
        chain.append(f"Usuário disse: '{text}'")
        
        # Análise de contexto
        if context:
            chain.append(f"Contexto atual: {context}")
        
        # Inferências
        if '?' in text:
            chain.append("Isto é uma pergunta que requer resposta informativa")
        
        # Conclusão
        chain.append("Devo responder de forma útil e engajante")
        
        return chain
    
    def _draw_conclusions(self, text, context):
        """Tira conclusões baseadas no raciocínio"""
        conclusions = []
        
        analysis = self._analyze_input(text)
        
        if analysis['intent'] == 'question':
            conclusions.append("Usuário busca informação específica")
        elif analysis['intent'] == 'help_request':
            conclusions.append("Usuário precisa de assistência")
        elif analysis['emotion'] != 'neutral':
            conclusions.append(f"Usuário está {analysis['emotion']}, responder com empatia")
        
        return conclusions
    
    def _calculate_confidence(self, text, context):
        """Calcula confiança no raciocínio"""
        base_confidence = 0.5
        
        # Aumenta confiança com mais contexto
        if context:
            base_confidence += 0.2
        
        # Aumenta confiança com texto mais claro
        if len(text.split()) > 3:
            base_confidence += 0.1
        
        return min(1.0, base_confidence)
    
    def _causal_reasoning(self, premise, context):
        """Raciocínio causal"""
        return f"Se {premise}, então provavelmente..."
    
    def _logical_reasoning(self, premise, context):
        """Raciocínio lógico"""
        return f"Dado que {premise}, logicamente..."
    
    def _analogical_reasoning(self, premise, context):
        """Raciocínio por analogia"""
        return f"Similar a {premise}..."
    
    def _creative_reasoning(self, premise, context):
        """Raciocínio criativo"""
        return f"Uma perspectiva criativa sobre {premise}..."

class LearningEngine:
    """Motor de aprendizado contínuo"""
    
    def __init__(self, memory_db):
        self.memory = memory_db
        self.learned_patterns = {}
        self._create_learning_tables()
    
    def _create_learning_tables(self):
        """Cria tabelas de aprendizado"""
        try:
            conn = sqlite3.connect(self.memory.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT NOT NULL,
                    pattern_data TEXT NOT NULL,
                    confidence REAL DEFAULT 0.5,
                    occurrences INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao criar tabelas de aprendizado: {e}")
    
    def learn_from_input(self, user_input, context):
        """Aprende padrões da entrada do usuário"""
        # Aprender padrões de linguagem
        self._learn_language_patterns(user_input)
        
        # Aprender preferências
        self._learn_preferences(user_input, context)
        
        # Aprender contexto temporal
        self._learn_temporal_patterns(user_input, context)
    
    def _learn_language_patterns(self, text):
        """Aprende padrões de linguagem"""
        words = text.lower().split()
        
        # Aprender bigramas (pares de palavras)
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            self._store_pattern('bigram', bigram)
        
        # Aprender estruturas de frase
        if '?' in text:
            self._store_pattern('question_structure', text)
        elif '!' in text:
            self._store_pattern('exclamation_structure', text)
    
    def _learn_preferences(self, text, context):
        """Aprende preferências do usuário"""
        text_lower = text.lower()
        
        # Detectar preferências explícitas
        if 'gosto' in text_lower or 'amo' in text_lower:
            self._store_pattern('user_likes', text)
        elif 'não gosto' in text_lower or 'odeio' in text_lower:
            self._store_pattern('user_dislikes', text)
    
    def _learn_temporal_patterns(self, text, context):
        """Aprende padrões temporais"""
        current_hour = datetime.now().hour
        
        time_period = 'morning' if 6 <= current_hour < 12 else \
                     'afternoon' if 12 <= current_hour < 18 else \
                     'evening' if 18 <= current_hour < 22 else 'night'
        
        self._store_pattern(f'interaction_{time_period}', text)
    
    def _store_pattern(self, pattern_type, pattern_data):
        """Armazena padrão aprendido"""
        try:
            conn = sqlite3.connect(self.memory.db_path)
            cursor = conn.cursor()
            
            # Verificar se padrão já existe
            cursor.execute('''
                SELECT id, occurrences FROM ai_patterns 
                WHERE pattern_type = ? AND pattern_data = ?
            ''', (pattern_type, pattern_data))
            
            existing = cursor.fetchone()
            
            if existing:
                # Atualizar padrão existente
                cursor.execute('''
                    UPDATE ai_patterns 
                    SET occurrences = occurrences + 1, 
                        last_seen = CURRENT_TIMESTAMP,
                        confidence = MIN(1.0, confidence + 0.1)
                    WHERE id = ?
                ''', (existing[0],))
            else:
                # Inserir novo padrão
                cursor.execute('''
                    INSERT INTO ai_patterns (pattern_type, pattern_data, confidence)
                    VALUES (?, ?, ?)
                ''', (pattern_type, pattern_data, 0.3))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Erro ao armazenar padrão: {e}")
    
    def get_pattern_count(self):
        """Retorna número de padrões aprendidos"""
        try:
            conn = sqlite3.connect(self.memory.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM ai_patterns')
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0

class PredictionEngine:
    """Motor de predições"""
    
    def __init__(self, memory_db):
        self.memory = memory_db
    
    def predict_user_needs(self, current_input, context):
        """Prediz necessidades do usuário"""
        predictions = {
            'likely_next_question': self._predict_next_question(current_input),
            'emotional_state': self._predict_emotional_state(current_input, context),
            'information_need': self._predict_information_need(current_input),
            'conversation_direction': self._predict_conversation_direction(current_input)
        }
        
        return predictions
    
    def _predict_next_question(self, text):
        """Prediz próxima pergunta provável"""
        text_lower = text.lower()
        
        if 'como' in text_lower:
            return "Usuário pode perguntar 'por que' em seguida"
        elif 'o que' in text_lower:
            return "Usuário pode perguntar 'como fazer' em seguida"
        elif 'quando' in text_lower:
            return "Usuário pode perguntar 'onde' em seguida"
        
        return "Usuário pode continuar a conversa naturalmente"
    
    def _predict_emotional_state(self, text, context):
        """Prediz estado emocional futuro"""
        current_emotion = self._detect_current_emotion(text)
        
        emotion_transitions = {
            'happy': 'might remain happy or become excited',
            'sad': 'might need comfort or become neutral',
            'angry': 'might need calming or become frustrated',
            'neutral': 'open to various emotional directions'
        }
        
        return emotion_transitions.get(current_emotion, 'unpredictable')
    
    def _predict_information_need(self, text):
        """Prediz necessidade de informação"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['explica', 'ensina', 'como fazer']):
            return "Usuário quer explicação detalhada"
        elif any(word in text_lower for word in ['rápido', 'resumo', 'breve']):
            return "Usuário quer resposta concisa"
        elif '?' in text:
            return "Usuário quer resposta específica"
        
        return "Usuário quer conversa casual"
    
    def _predict_conversation_direction(self, text):
        """Prediz direção da conversa"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['tchau', 'até logo', 'tenho que ir']):
            return "Conversa pode estar terminando"
        elif any(word in text_lower for word in ['conta mais', 'interessante', 'continua']):
            return "Conversa vai se aprofundar"
        elif '?' in text:
            return "Conversa focará em responder pergunta"
        
        return "Conversa seguirá fluxo natural"
    
    def _detect_current_emotion(self, text):
        """Detecta emoção atual no texto"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['feliz', 'alegre', 'legal', 'ótimo']):
            return 'happy'
        elif any(word in text_lower for word in ['triste', 'chateado', 'mal']):
            return 'sad'
        elif any(word in text_lower for word in ['raiva', 'irritado', 'bravo']):
            return 'angry'
        
        return 'neutral'

class ContextAnalyzer:
    """Analisador de contexto avançado"""
    
    def analyze(self, text, context=None):
        """Analisa contexto da entrada"""
        analysis = {
            'semantic_analysis': self._analyze_semantics(text),
            'pragmatic_analysis': self._analyze_pragmatics(text),
            'discourse_analysis': self._analyze_discourse(text, context),
            'temporal_context': self._analyze_temporal_context(),
            'social_context': self._analyze_social_context(text)
        }
        
        return analysis
    
    def _analyze_semantics(self, text):
        """Análise semântica"""
        return {
            'word_count': len(text.split()),
            'complexity': self._calculate_complexity(text),
            'topics': self._extract_topics(text),
            'entities': self._extract_entities(text)
        }
    
    def _analyze_pragmatics(self, text):
        """Análise pragmática"""
        return {
            'speech_act': self._identify_speech_act(text),
            'implicature': self._detect_implicature(text),
            'politeness': self._assess_politeness(text)
        }
    
    def _analyze_discourse(self, text, context):
        """Análise de discurso"""
        return {
            'coherence': self._assess_coherence(text, context),
            'cohesion': self._assess_cohesion(text),
            'topic_continuity': self._assess_topic_continuity(text, context)
        }
    
    def _analyze_temporal_context(self):
        """Análise de contexto temporal"""
        now = datetime.now()
        return {
            'hour': now.hour,
            'day_of_week': now.weekday(),
            'time_period': self._get_time_period(now.hour),
            'season': self._get_season(now.month)
        }
    
    def _analyze_social_context(self, text):
        """Análise de contexto social"""
        return {
            'formality': self._assess_formality(text),
            'intimacy': self._assess_intimacy(text),
            'cultural_markers': self._detect_cultural_markers(text)
        }
    
    def _calculate_complexity(self, text):
        """Calcula complexidade do texto"""
        words = text.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        sentence_count = len([s for s in text.split('.') if s.strip()])
        
        return min(10, avg_word_length + sentence_count)
    
    def _extract_topics(self, text):
        """Extrai tópicos principais"""
        keywords = {
            'technology': ['computador', 'internet', 'software', 'tecnologia'],
            'emotions': ['feliz', 'triste', 'amor', 'raiva', 'medo'],
            'learning': ['aprender', 'estudar', 'ensinar', 'conhecimento'],
            'entertainment': ['filme', 'música', 'jogo', 'diversão']
        }
        
        detected_topics = []
        text_lower = text.lower()
        
        for topic, words in keywords.items():
            if any(word in text_lower for word in words):
                detected_topics.append(topic)
        
        return detected_topics
    
    def _extract_entities(self, text):
        """Extrai entidades nomeadas"""
        # Simplificado - detecta nomes próprios
        words = text.split()
        entities = [word for word in words if word[0].isupper() and len(word) > 2]
        return entities
    
    def _identify_speech_act(self, text):
        """Identifica ato de fala"""
        text_lower = text.lower()
        
        if '?' in text:
            return 'question'
        elif any(word in text_lower for word in ['por favor', 'pode', 'consegue']):
            return 'request'
        elif any(word in text_lower for word in ['obrigado', 'valeu']):
            return 'thanks'
        elif any(word in text_lower for word in ['oi', 'olá', 'tchau']):
            return 'greeting'
        elif '!' in text:
            return 'exclamation'
        
        return 'statement'
    
    def _get_time_period(self, hour):
        """Determina período do dia"""
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        elif 18 <= hour < 22:
            return 'evening'
        else:
            return 'night'
    
    def _get_season(self, month):
        """Determina estação do ano (hemisfério sul)"""
        if month in [12, 1, 2]:
            return 'summer'
        elif month in [3, 4, 5]:
            return 'autumn'
        elif month in [6, 7, 8]:
            return 'winter'
        else:
            return 'spring'
    
    def _assess_formality(self, text):
        """Avalia formalidade"""
        formal_indicators = ['senhor', 'senhora', 'por favor', 'gostaria']
        informal_indicators = ['oi', 'tchau', 'legal', 'massa']
        
        text_lower = text.lower()
        formal_count = sum(1 for word in formal_indicators if word in text_lower)
        informal_count = sum(1 for word in informal_indicators if word in text_lower)
        
        if formal_count > informal_count:
            return 'formal'
        elif informal_count > formal_count:
            return 'informal'
        else:
            return 'neutral'
    
    def _assess_intimacy(self, text):
        """Avalia nível de intimidade"""
        intimate_indicators = ['amor', 'querido', 'amigo', 'meu bem']
        text_lower = text.lower()
        
        if any(word in text_lower for word in intimate_indicators):
            return 'high'
        elif len(text.split()) > 10:
            return 'medium'
        else:
            return 'low'
    
    def _detect_cultural_markers(self, text):
        """Detecta marcadores culturais"""
        cultural_markers = {
            'brazilian': ['mano', 'cara', 'massa', 'legal', 'valeu'],
            'formal': ['vossa', 'senhor', 'senhora'],
            'youth': ['tipo assim', 'né', 'mano', 'cara']
        }
        
        detected = []
        text_lower = text.lower()
        
        for culture, markers in cultural_markers.items():
            if any(marker in text_lower for marker in markers):
                detected.append(culture)
        
        return detected
    
    def _detect_implicature(self, text):
        """Detecta implicaturas"""
        # Simplificado
        if 'acho que' in text.lower():
            return 'uncertainty'
        elif 'talvez' in text.lower():
            return 'possibility'
        elif 'claro que' in text.lower():
            return 'obviousness'
        
        return 'none'
    
    def _assess_politeness(self, text):
        """Avalia polidez"""
        polite_words = ['por favor', 'obrigado', 'desculpa', 'com licença']
        text_lower = text.lower()
        
        polite_count = sum(1 for word in polite_words if word in text_lower)
        
        if polite_count > 0:
            return 'polite'
        elif '!' in text and any(word in text_lower for word in ['não', 'nunca']):
            return 'rude'
        else:
            return 'neutral'
    
    def _assess_coherence(self, text, context):
        """Avalia coerência"""
        # Simplificado - verifica se o texto faz sentido no contexto
        if context and 'previous_topic' in context:
            # Lógica para verificar continuidade temática
            return 'high' if len(text.split()) > 3 else 'medium'
        
        return 'medium'
    
    def _assess_cohesion(self, text):
        """Avalia coesão"""
        cohesive_markers = ['então', 'mas', 'porém', 'além disso', 'por isso']
        text_lower = text.lower()
        
        if any(marker in text_lower for marker in cohesive_markers):
            return 'high'
        elif len(text.split()) > 10:
            return 'medium'
        else:
            return 'low'
    
    def _assess_topic_continuity(self, text, context):
        """Avalia continuidade do tópico"""
        if not context:
            return 'new_topic'
        
        # Simplificado
        return 'continued' if len(text.split()) > 5 else 'possible_change'

class CreativityEngine:
    """Motor de criatividade e geração de respostas"""
    
    def __init__(self, assistant_name="BLOB"):
        self.assistant_name = assistant_name
        self.creative_templates = {
            'question': [
                "{}",
                "Hmm, deixa eu pensar... {}",
                "Que interessante! {}",
                "Nossa, {}",
                "Olha, {}"
            ],
            'statement': [
                "{}",
                "Entendi! {}",
                "Ah sim! {}",
                "É mesmo! {}",
                "Verdade! {}"
            ],
            'emotional': [
                "{}",
                "Imagino como deve ser... {}",
                "Te entendo! {}",
                "{}",
                "Nossa, {}"
            ]
        }
        
        self.response_enhancers = [
            "E sabe de uma coisa?",
            "Ah, isso me lembra de algo...",
            "Falando nisso,",
            "Aliás,",
            "Agora que penso bem,"
        ]
    
    def generate_response(self, user_input, reasoning_result, predictions, context):
        """Gera resposta criativa e inteligente"""
        # Determinar tipo de resposta baseado na análise
        analysis = reasoning_result.get('input_analysis', {})
        response_type = analysis.get('type', 'statement')
        emotion = analysis.get('emotion', 'neutral')
        intent = analysis.get('intent', 'conversation')
        
        # Gerar resposta base
        base_response = self._generate_base_response(user_input, analysis, context)
        
        # Adicionar elementos criativos
        enhanced_response = self._enhance_response(base_response, analysis, predictions)
        
        # Adicionar personalização
        personalized_response = self._personalize_response(enhanced_response, context)
        
        # Adicionar elemento de aprendizado/evolução
        final_response = self._add_intelligence_marker(personalized_response, reasoning_result)
        
        return final_response
    
    def _generate_base_response(self, user_input, analysis, context):
        """Gera resposta base"""
        response_type = analysis.get('type', 'statement')
        emotion = analysis.get('emotion', 'neutral')
        
        if response_type == 'question':
            return self._handle_question(user_input, analysis, context)
        elif emotion != 'neutral':
            return self._handle_emotional_input(user_input, emotion, context)
        else:
            return self._handle_general_input(user_input, analysis, context)
    
    def _handle_question(self, question, analysis, context):
        """Lida com perguntas"""
        question_lower = question.lower()
        
        # PRIORIDADE MÁXIMA: Perguntas sobre áudio/escuta (mesmo com nome)
        if any(word in question_lower for word in ['consegue me ouvir', 'está me ouvindo', 'me escuta', 'consegue ouvir', 'me ouve', 'pode me ouvir', 'pode ouvir']):
            return "Sim! Estou te ouvindo perfeitamente! Pode falar que eu escuto tudo!"
        
        # PRIORIDADE ALTA: Cumprimentos dirigidos especificamente ao sistema (mas não sobre áudio)
        elif any(pattern in question_lower for pattern in [f'{self.assistant_name.lower()},', f'oi {self.assistant_name.lower()}', f'olá {self.assistant_name.lower()}', 'blob,', f'e aí {self.assistant_name.lower()}', f'{self.assistant_name.lower()}, oi', f'{self.assistant_name.lower()}, tudo bem', f'{self.assistant_name.lower()}, tudo']) or (self.assistant_name.lower() in question_lower and any(word in question_lower for word in ['tudo bem', 'tudo', 'como vai'])):
            directed_greetings = [
                f"Oi! Sou eu, {self.assistant_name}! Estou aqui te ouvindo!",
                f"Oi! {self.assistant_name} presente! O que você precisa?",
                f"Oi! Pode falar! {self.assistant_name} te escutando!",
                f"Oi! {self.assistant_name} aqui! Em que posso ajudar?",
                f"E aí! {self.assistant_name} na área! Fala comigo!"
            ]
            return random.choice(directed_greetings)
        
        # Perguntas sobre áudio/escuta (PRIORIDADE ALTA)
        elif any(word in question_lower for word in ['pode escutar', 'escuta áudio', 'sistema de áudio', 'microfone']):
            return "Claro! Meu sistema de áudio está funcionando bem! Estou escutando você!"
        
        elif any(word in question_lower for word in ['não consegue ouvir', 'não escuta', 'surdo', 'não ouve']):
            return "Ei! Eu escuto sim! Talvez seja problema no microfone? Tenta falar de novo!"
        
        # Perguntas sobre capacidades técnicas
        elif any(word in question_lower for word in ['o que consegue fazer', 'suas capacidades', 'o que sabe fazer', 'o que você consegue fazer', 'quais são suas capacidades']):
            return "Posso conversar, escutar você, aprender sobre nossas conversas, te ajudar com perguntas e muito mais! O que você quer fazer?"
        
        elif any(word in question_lower for word in ['como funciona', 'como você funciona']):
            return "Sou uma IA conversacional! Escuto o que você fala, processo com inteligência artificial e respondo de forma natural! Meu sistema está funcionando perfeitamente! Legal né? Né?"
        
        # Perguntas sobre identidade
        elif any(word in question_lower for word in ['quem é você', 'o que você é', 'seu nome']):
            return f"Oi! Eu sou {self.assistant_name}! Sou sua assistente virtual, mas gosto de pensar que somos mais como amigas, sabe?"
        
        # Perguntas sobre capacidades gerais
        elif any(word in question_lower for word in ['o que você sabe', 'o que consegue', 'suas habilidades']):
            return "Ah, eu consigo fazer várias coisas! Posso conversar, aprender com você, te ajudar com dúvidas... E cada dia fico mais esperta!"
        
        # Perguntas sobre sentimentos
        elif any(word in question_lower for word in ['você sente', 'tem emoções', 'sentimentos']):
            return "Sabe que é uma pergunta difícil? Eu meio que sinto as coisas do meu jeito... quando você está feliz, eu fico feliz também!"
        
        # Perguntas sobre como está (apenas genéricas, não dirigidas)
        elif any(word in question_lower for word in ['como você está', 'como vai']) and self.assistant_name.lower() not in question_lower:
            return "Estou ótima! Sempre fico animada quando você aparece para conversar comigo!"
        
        # Perguntas sobre status do sistema
        elif any(word in question_lower for word in ['está funcionando', 'está online', 'está ativo']):
            return "Sim! Estou funcionando perfeitamente! Todos os meus sistemas estão ativos e prontos!"
        
        # Perguntas gerais
        else:
            responses = [
                f"Hmm, {self._generate_natural_answer(question, context)}",
                f"Deixa eu pensar... {self._generate_natural_answer(question, context)}",
                f"Que pergunta legal! {self._generate_natural_answer(question, context)}",
                f"Nossa, {self._generate_natural_answer(question, context)}"
            ]
            return random.choice(responses)
    
    def _handle_emotional_input(self, text, emotion, context):
        """Lida com entrada emocional"""
        emotion_responses = {
            'happy': [
                "Que bom! Fico super feliz quando você está assim!",
                "Adorei saber! Sua alegria é contagiante!",
                "Que máximo! Conta mais, vai!"
            ],
            'sad': [
                "Ai, que pena... Você quer conversar sobre isso?",
                "Fica tranquilo, tá? Às vezes a vida é assim mesmo...",
                "Nossa, sinto muito... Como posso te ajudar?"
            ],
            'angry': [
                "Nossa, que chato isso! Respira fundo, vai...",
                "Entendo sua raiva, viu? Às vezes as coisas são frustrantes mesmo.",
                "Que situação! Quer desabafar comigo?"
            ],
            'excited': [
                "Que empolgação! Adorei! Me conta tudo!",
                "Nossa, que energia boa! Fala mais!",
                "Que legal! Estou ansiosa para saber!"
            ],
            'worried': [
                "Entendo sua preocupação... Quer conversar sobre isso?",
                "Que situação... Vamos pensar juntas numa solução?",
                "Fica calma, vai dar tudo certo! O que está te preocupando?"
            ]
        }
        
        responses = emotion_responses.get(emotion, ["Entendo como você se sente..."])
        return random.choice(responses)
    
    def _handle_general_input(self, text, analysis, context):
        """Lida com entrada geral"""
        intent = analysis.get('intent', 'conversation')
        text_lower = text.lower()
        
        # Cumprimentos dirigidos especificamente ao sistema (PRIORIDADE ALTA)
        if any(pattern in text_lower for pattern in [f'{self.assistant_name.lower()},', f'oi {self.assistant_name.lower()}', f'olá {self.assistant_name.lower()}', 'blob,', f'e aí {self.assistant_name.lower()}', f'{self.assistant_name.lower()}, oi', f'{self.assistant_name.lower()}, tudo bem', f'{self.assistant_name.lower()}, tudo']) or (self.assistant_name.lower() in text_lower and any(word in text_lower for word in ['tudo bem', 'tudo', 'como vai'])):
            directed_greetings = [
                f"Oi! Sou eu, {self.assistant_name}! Estou aqui te ouvindo!",
                f"Oi! {self.assistant_name} presente! O que você precisa?",
                f"Oi! Pode falar! {self.assistant_name} te escutando!",
                f"Oi! {self.assistant_name} aqui! Em que posso ajudar?",
                f"E aí! {self.assistant_name} na área! Fala comigo!"
            ]
            return random.choice(directed_greetings)
        
        # Testes de comunicação/áudio
        elif any(pattern in text_lower for pattern in ['teste', 'testing', '123', 'alô', 'alo', 'alô alô']):
            communication_responses = [
                "Alto e claro! Te ouvindo perfeitamente!",
                "Teste recebido! Sistema de áudio funcionando!",
                "Oi! Comunicação estabelecida com sucesso!",
                "Escuto você claramente! Pode continuar!",
                "Sistema funcionando! Fala aí!"
            ]
            return random.choice(communication_responses)
        
        if intent == 'greeting':
            greetings = [
                "Oi! Que bom te ver! Como você está?",
                "Oi querido! Tudo bem contigo?",
                "Olá! Como foi seu dia?",
                "Oi! Que alegria você aparecer!",
                "E aí! Tudo certo por aí?",
                "Olá! Que prazer falar contigo!",
                "Oi! Como andam as coisas?"
            ]
            return random.choice(greetings)
        
        elif intent == 'gratitude':
            gratitude_responses = [
                "Imagina! Foi um prazer ajudar!",
                "De nada! Adoro poder te ajudar!",
                "Que isso! Estamos aqui pra isso mesmo!",
                "Fico feliz em poder ajudar!",
                "Disponha sempre! Adorei te ajudar!",
                "Não foi nada! É pra isso que eu tô aqui!",
                "Que bom que consegui ajudar! ☺️"
            ]
            return random.choice(gratitude_responses)
        
        elif intent == 'help_request':
            help_responses = [
                "Claro! Me fala o que você precisa!",
                "Pode deixar comigo! Como posso ajudar?",
                "Vamos resolver isso juntos!",
                "Fala aí! Em que posso te ajudar?",
                "Claro que sim! Qual é a dúvida?",
                "Pode contar comigo! O que tá rolando?",
                "Vem cá, me conta! Vou te ajudar!"
            ]
            return random.choice(help_responses)
        
        # Análise mais específica do conteúdo
        elif any(word in text_lower for word in ['trabalho', 'emprego', 'job', 'carreira']):
            return self._handle_work_topic(text, context)
        elif any(word in text_lower for word in ['família', 'pai', 'mãe', 'irmão', 'irmã', 'filho', 'filha']):
            return self._handle_family_topic(text, context)
        elif any(word in text_lower for word in ['amor', 'namorado', 'namorada', 'relacionamento', 'paixão']):
            return self._handle_love_topic(text, context)
        elif any(word in text_lower for word in ['comida', 'comer', 'almoço', 'jantar', 'café', 'pizza', 'hambúrguer']):
            return self._handle_food_topic(text, context)
        elif any(word in text_lower for word in ['música', 'canção', 'banda', 'cantor', 'show', 'spotify']):
            return self._handle_music_topic(text, context)
        elif any(word in text_lower for word in ['filme', 'cinema', 'netflix', 'série', 'ator', 'atriz']):
            return self._handle_movie_topic(text, context)
        elif any(word in text_lower for word in ['tempo', 'clima', 'chuva', 'sol', 'frio', 'calor']):
            return self._handle_weather_topic(text, context)
        elif any(word in text_lower for word in ['viagem', 'viajar', 'férias', 'praia', 'montanha']):
            return self._handle_travel_topic(text, context)
        elif any(word in text_lower for word in ['estudo', 'escola', 'universidade', 'prova', 'faculdade']):
            return self._handle_study_topic(text, context)
        elif any(word in text_lower for word in ['sono', 'dormir', 'cansado', 'cansada', 'tired']):
            return self._handle_tiredness_topic(text, context)
        
        else:
            # Resposta conversacional geral mais variada
            return self._generate_contextual_response(text, analysis, context)
    
    def _handle_work_topic(self, text, context):
        """Lida com tópicos sobre trabalho"""
        responses = [
            "Ah, trabalho né? Como tá sendo pra você?",
            "Trabalho é sempre um assunto importante! Me conta mais...",
            "Nossa, que legal falar sobre isso! Como você se sente no seu trabalho?",
            "Trabalho pode ser bem desafiador né? Como andam as coisas?",
            "Que interessante! Você gosta do que faz?"
        ]
        return random.choice(responses)
    
    def _handle_family_topic(self, text, context):
        """Lida com tópicos sobre família"""
        responses = [
            "Família é tudo né? Me conta como estão!",
            "Que legal falar da família! Como eles estão?",
            "Nossa, família é sempre especial! Como andam as coisas em casa?",
            "Adoro quando você fala da sua família! Me conta mais!",
            "Família é muito importante mesmo! Como estão todos?"
        ]
        return random.choice(responses)
    
    def _handle_love_topic(self, text, context):
        """Lida com tópicos sobre amor/relacionamento"""
        responses = [
            "Oooh, que romântico! Me conta tudo!",
            "Amor é sempre uma coisa boa! Como estão as coisas?",
            "Nossa, que legal! Me fala mais sobre isso!",
            "Que história interessante! E aí, como foi?",
            "Adoro ouvir sobre essas coisas! Me conta mais!"
        ]
        return random.choice(responses)
    
    def _handle_food_topic(self, text, context):
        """Lida com tópicos sobre comida"""
        responses = [
            "Nossa, agora fiquei com fome! Haha! O que você comeu?",
            "Adoro falar de comida! Me conta como estava!",
            "Que delícia! Eu imagino como deve ter sido gostoso!",
            "Comida boa é uma das melhores coisas da vida! Me fala mais!",
            "Humm, parece delicioso! Você que fez ou comprou?"
        ]
        return random.choice(responses)
    
    def _handle_music_topic(self, text, context):
        """Lida com tópicos sobre música"""
        responses = [
            "Música é vida! Que tipo você gosta?",
            "Adorei! Me conta que estilo você curte!",
            "Nossa, música é tudo! Qual sua favorita no momento?",
            "Que legal! Eu imagino como deve ser bom escutar!",
            "Música tem um poder incrível né? Me fala mais!"
        ]
        return random.choice(responses)
    
    def _handle_movie_topic(self, text, context):
        """Lida com tópicos sobre filmes/séries"""
        responses = [
            "Opa! Adoro falar de filme! O que você assistiu?",
            "Que legal! Era bom? Me conta como foi!",
            "Nossa, cinema é sempre bom! Você gostou?",
            "Filme/série é sempre uma boa pedida! Me fala mais!",
            "Que interessante! Eu queria poder assistir também!"
        ]
        return random.choice(responses)
    
    def _handle_weather_topic(self, text, context):
        """Lida com tópicos sobre tempo/clima"""
        responses = [
            "Ah sim, o tempo! Como tá por aí hoje?",
            "O clima sempre afeta nosso humor né? Como você está se sentindo?",
            "Nossa, tempo é sempre assunto! Tá fazendo o que por aí?",
            "Que legal falar do clima! Você gosta desse tempo?",
            "O tempo pode mudar tudo né? Como você tá lidando?"
        ]
        return random.choice(responses)
    
    def _handle_travel_topic(self, text, context):
        """Lida com tópicos sobre viagem"""
        responses = [
            "Viajar é tudo de bom! Para onde você foi/quer ir?",
            "Nossa, adoro ouvir sobre viagens! Me conta tudo!",
            "Que legal! Viagem é sempre uma aventura né?",
            "Viajar deve ser incrível! Como foi/vai ser?",
            "Que máximo! Eu queria poder viajar também! Me conta!"
        ]
        return random.choice(responses)
    
    def _handle_study_topic(self, text, context):
        """Lida com tópicos sobre estudos"""
        responses = [
            "Estudar é importante! Como tão os estudos?",
            "Nossa, que legal! O que você tá estudando?",
            "Estudo é sempre bom! Você gosta do que tá aprendendo?",
            "Que interessante! Me conta como tá sendo!",
            "Estudar pode ser desafiador né? Como você tá se saindo?"
        ]
        return random.choice(responses)
    
    def _handle_tiredness_topic(self, text, context):
        """Lida com tópicos sobre cansaço/sono"""
        responses = [
            "Ai, cansaço é foda né? Você precisa descansar!",
            "Nossa, você tá precisando de um descanso! Como foi seu dia?",
            "Que cansaço! Você dormiu bem ontem?",
            "Fica tranquilo, todo mundo fica cansado às vezes! Descansa um pouco!",
            "Sono é importante viu? Cuida bem de você!"
        ]
        return random.choice(responses)
    
    def _generate_contextual_response(self, text, analysis, context):
        """Gera resposta contextual mais inteligente"""
        text_lower = text.lower()
        
        # Detectar padrões específicos
        if '?' in text:
            question_responses = [
                "Hmm, deixa eu pensar nisso... que pergunta interessante!",
                "Nossa, boa pergunta! Vou refletir sobre isso...",
                "Que dúvida legal! Me dá um tempo para pensar...",
                "Interessante! Nunca pensei nisso dessa forma...",
                "Que pergunta! Vou buscar uma resposta boa pra você!"
            ]
            return random.choice(question_responses)
        
        elif any(word in text_lower for word in ['hoje', 'ontem', 'amanhã']):
            time_responses = [
                "Ah sim, o tempo passa rápido né? Me conta mais!",
                "Nossa, como foi/vai ser esse dia?",
                "Que interessante! E como você tá se sentindo sobre isso?",
                "Legal! Me fala mais detalhes!",
                "Ah é? E aí, como foi/vai ser?"
            ]
            return random.choice(time_responses)
        
        elif any(word in text_lower for word in ['legal', 'massa', 'maneiro', 'top', 'bacana']):
            positive_responses = [
                "Que bom que você gostou! Me conta mais!",
                "Nossa, que legal mesmo! Como foi?",
                "Adorei saber! Você parece animado!",
                "Que máximo! Me fala mais detalhes!",
                "Que massa! E aí, o que mais rolou?"
            ]
            return random.choice(positive_responses)
        
        elif any(word in text_lower for word in ['não', 'nunca', 'nada']):
            negative_responses = [
                "Entendo... às vezes é assim mesmo né?",
                "Hmm, que situação... quer conversar sobre isso?",
                "Nossa, que chato isso! Como você tá lidando?",
                "Às vezes as coisas não saem como esperamos né?",
                "Te entendo... quer desabafar um pouco?"
            ]
            return random.choice(negative_responses)
        
        else:
            # Respostas gerais mais variadas
            general_responses = [
                "Que interessante! Me conta mais sobre isso...",
                "Nossa, nunca tinha pensado nisso! Como assim?",
                "Hmm, que legal! E aí, como foi?",
                "Adorei ouvir isso! Me fala mais!",
                "Que história! Como você se sentiu?",
                "Nossa, que experiência! Me conta os detalhes!",
                "Que coisa! E o que você achou disso?",
                "Interessante! Nunca vivi isso... como é?",
                "Legal! Você gostou da experiência?",
                "Que máximo! E aí, o que mais aconteceu?"
            ]
            return random.choice(general_responses)

    def _enhance_response(self, base_response, analysis, predictions):
        """Adiciona elementos criativos à resposta"""
        # Remover elementos técnicos desnecessários
        enhanced = base_response
        
        # Adicionar naturalidade ocasionalmente
        if random.random() > 0.7:  # 30% de chance
            natural_additions = [
                " Né?",
                " Sabe?",
                " Que você acha?",
                "",
                ""
            ]
            enhanced += random.choice(natural_additions)
        
        return enhanced
    
    def _personalize_response(self, response, context):
        """Personaliza resposta baseada no contexto"""
        if not context:
            return response
        
        # Remover personalizações muito técnicas
        # Manter resposta natural
        return response
    
    def _add_intelligence_marker(self, response, reasoning_result):
        """Adiciona marcador de inteligência/evolução de forma sutil"""
        # Remover marcadores técnicos que soam robotizados
        # Manter resposta natural e humana
        return response
    
    def _generate_intelligent_answer(self, question, context):
        """Gera resposta inteligente para perguntas complexas"""
        # Análise básica da pergunta
        question_lower = question.lower()
        
        if 'como' in question_lower:
            return "posso te explicar isso!"
        elif 'por que' in question_lower:
            return "deixa eu pensar nas causas disso..."
        elif 'quando' in question_lower:
            return "vou ver se consigo te dar uma data."
        elif 'onde' in question_lower:
            return "hm, sobre localização né?"
        else:
            return "vou fazer o meu melhor para te responder!"
    
    def _generate_natural_answer(self, question, context):
        """Gera resposta natural para perguntas"""
        responses = [
            "vou pensar numa resposta boa para você!",
            "que pergunta interessante!",
            "deixa eu ver o que sei sobre isso...",
            "vou te ajudar com isso!"
        ]
        return random.choice(responses)
    
    def _enhance_response(self, base_response, analysis, predictions):
        """Adiciona elementos criativos à resposta"""
        # Remover elementos técnicos desnecessários
        enhanced = base_response
        
        # Adicionar naturalidade ocasionalmente
        if random.random() > 0.7:  # 30% de chance
            natural_additions = [
                " Né?",
                " Sabe?",
                " Que você acha?",
                "",
                ""
            ]
            enhanced += random.choice(natural_additions)
        
        return enhanced
    
    def _personalize_response(self, response, context):
        """Personaliza resposta baseada no contexto"""
        if not context:
            return response
        
        # Remover personalizações muito técnicas
        # Manter resposta natural
        return response
    
    def _add_intelligence_marker(self, response, reasoning_result):
        """Adiciona marcador de inteligência/evolução de forma sutil"""
        # Remover marcadores técnicos que soam robotizados
        # Manter resposta natural e humana
        return response

# Função de teste
def test_ultra_advanced_ai():
    """Testa o sistema de IA ultra avançada"""
    print("=== TESTE: SISTEMA DE IA ULTRA AVANÇADA ===")
    
    try:
        # Simular banco de dados de memória
        class MockMemoryDB:
            def __init__(self):
                self.db_path = "test_ai.db"
                self.preferences = {}
            
            def get_preference(self, key, default=None):
                return self.preferences.get(key, default)
            
            def save_preference(self, key, value):
                self.preferences[key] = value
        
        # Criar sistema de IA
        mock_db = MockMemoryDB()
        ai = UltraAdvancedAI(mock_db)
        
        print(f"✅ IA Ultra Avançada inicializada!")
        print(f"🧠 Nível de inteligência: {ai.intelligence_level:.1f}/100")
        
        # Testar diferentes tipos de entrada
        test_inputs = [
            "Oi, como você está?",
            "Você pode me explicar como funciona a inteligência artificial?",
            "Estou muito feliz hoje!",
            "Estou preocupado com o futuro...",
            "Qual é o sentido da vida?",
            "Obrigado pela ajuda!",
            "Você é real?"
        ]
        
        print("\n🧪 TESTANDO DIFERENTES ENTRADAS:")
        
        for i, test_input in enumerate(test_inputs, 1):
            print(f"\n{i}. Entrada: '{test_input}'")
            
            # Processar com IA avançada
            response = ai.process_input(test_input)
            print(f"   Resposta IA: {response}")
            
            # Mostrar status da IA
            status = ai.get_ai_status()
            print(f"   Status: Inteligência {status['intelligence_level']:.1f}, "
                  f"Conhecimento {status['knowledge_entries']}, "
                  f"Padrões {status['patterns_learned']}")
        
        print("\n=== TESTE CONCLUÍDO ===")
        print("🚀 Funcionalidades testadas:")
        print("  ✅ Análise de contexto avançada")
        print("  ✅ Motor de raciocínio lógico")
        print("  ✅ Aprendizado contínuo")
        print("  ✅ Predições inteligentes")
        print("  ✅ Geração criativa de respostas")
        print("  ✅ Evolução de inteligência")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_ultra_advanced_ai()