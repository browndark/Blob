"""
Engine de Personalidade - Aprende e evolui com o usuário
"""

import random
import json
import re
from datetime import datetime
from typing import Dict, List, Any

class PersonalityEngine:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.personality_traits = self.load_personality()
        self.conversation_patterns = self.load_patterns()
        
        # Características base da personalidade
        self.base_traits = {
            "friendliness": 0.8,
            "curiosity": 0.7,
            "humor": 0.6,
            "empathy": 0.8,
            "energy": 0.7,
            "formality": 0.3,
            "supportiveness": 0.9
        }
        
        # Padrões de resposta baseados na personalidade
        self.response_templates = {
            "greeting": [
                "Oi {name}! Como você está?",
                "Olá {name}! Que bom te ver!",
                "Ei {name}! Como foi seu dia?",
                "Hey {name}! Estava com saudades!"
            ],
            "question": [
                "Que pergunta interessante!",
                "Deixe-me pensar sobre isso...",
                "Hmm, boa pergunta!",
                "Isso é algo que me faz pensar..."
            ],
            "enthusiasm": [
                "Que legal!",
                "Isso é incrível!",
                "Uau, adorei isso!",
                "Que demais!"
            ],
            "support": [
                "Estou aqui para você!",
                "Você pode contar comigo!",
                "Vamos resolver isso juntos!",
                "Não se preocupe, vou te ajudar!"
            ],
            "learning": [
                "Interessante, não sabia disso!",
                "Acabei de aprender algo novo!",
                "Obrigado por me ensinar isso!",
                "Que conhecimento legal!"
            ]
        }
        
        # Palavras-chave para detectar emoções
        self.emotion_keywords = {
            "happy": ["feliz", "alegre", "contente", "animado", "bem", "ótimo", "legal", "incrível"],
            "sad": ["triste", "chateado", "deprimido", "mal", "péssimo", "down", "para baixo"],
            "excited": ["empolgado", "ansioso", "excitado", "entusiasmado", "eufórico"],
            "angry": ["bravo", "irritado", "nervoso", "furioso", "raiva", "ódio"],
            "confused": ["confuso", "perdido", "não entendo", "complicado", "difícil"],
            "grateful": ["obrigado", "grato", "agradecido", "valeu", "thanks"]
        }
        
    def load_personality(self) -> Dict[str, Any]:
        """Carrega traits de personalidade salvos"""
        data = self.db_manager.get_personality_data()
        if data:
            return json.loads(data)
        else:
            return self.base_traits.copy()
            
    def save_personality(self):
        """Salva traits de personalidade"""
        self.db_manager.save_personality_data(json.dumps(self.personality_traits))
        
    def load_patterns(self) -> Dict[str, List[str]]:
        """Carrega padrões de conversa aprendidos"""
        patterns = self.db_manager.get_conversation_patterns()
        return patterns if patterns else {}
        
    def detect_emotion(self, text: str) -> str:
        """Detecta a emoção predominante no texto"""
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
                
        if emotion_scores:
            return max(emotion_scores, key=emotion_scores.get)
        return "neutral"
        
    def adapt_personality(self, user_input: str, user_emotion: str):
        """Adapta a personalidade baseada na interação"""
        # Aumenta empatia se usuário está triste
        if user_emotion == "sad":
            self.personality_traits["empathy"] = min(1.0, self.personality_traits["empathy"] + 0.01)
            self.personality_traits["supportiveness"] = min(1.0, self.personality_traits["supportiveness"] + 0.01)
            
        # Aumenta humor se usuário gosta de piadas
        elif user_emotion == "happy" and any(word in user_input.lower() for word in ["haha", "kkkk", "rsrs", "engraçado", "piada"]):
            self.personality_traits["humor"] = min(1.0, self.personality_traits["humor"] + 0.02)
            
        # Adapta energia baseada no usuário
        elif user_emotion == "excited":
            self.personality_traits["energy"] = min(1.0, self.personality_traits["energy"] + 0.01)
        elif user_emotion == "sad":
            self.personality_traits["energy"] = max(0.3, self.personality_traits["energy"] - 0.01)
            
        # Adapta formalidade baseada no estilo do usuário
        formal_indicators = ["por favor", "obrigado", "com licença", "poderia"]
        informal_indicators = ["oi", "opa", "beleza", "valeu", "cara"]
        
        if any(indicator in user_input.lower() for indicator in formal_indicators):
            self.personality_traits["formality"] = min(1.0, self.personality_traits["formality"] + 0.01)
        elif any(indicator in user_input.lower() for indicator in informal_indicators):
            self.personality_traits["formality"] = max(0.0, self.personality_traits["formality"] - 0.01)
            
        self.save_personality()
        
    def learn_from_input(self, user_input: str):
        """Aprende padrões da fala do usuário"""
        # Detectar gírias e expressões únicas
        words = user_input.lower().split()
        
        # Detectar padrões de saudação
        greetings = ["oi", "olá", "hey", "e aí", "beleza", "opa"]
        if any(greeting in words for greeting in greetings):
            if "user_greetings" not in self.conversation_patterns:
                self.conversation_patterns["user_greetings"] = []
            
            # Adicionar variação de saudação
            greeting_words = [word for word in words if word in greetings]
            if greeting_words and greeting_words[0] not in self.conversation_patterns["user_greetings"]:
                self.conversation_patterns["user_greetings"].append(greeting_words[0])
                
        # Detectar expressões de afirmação
        affirmations = ["sim", "claro", "certeza", "com certeza", "óbvio", "exato"]
        if any(affirmation in user_input.lower() for affirmation in affirmations):
            if "user_affirmations" not in self.conversation_patterns:
                self.conversation_patterns["user_affirmations"] = []
            
            for affirmation in affirmations:
                if affirmation in user_input.lower() and affirmation not in self.conversation_patterns["user_affirmations"]:
                    self.conversation_patterns["user_affirmations"].append(affirmation)
                    
        # Salvar padrões
        self.db_manager.save_conversation_patterns(self.conversation_patterns)
        
    def generate_response(self, user_input: str, user_name: str = None) -> str:
        """Gera resposta baseada na personalidade atual"""
        user_emotion = self.detect_emotion(user_input)
        
        # Aprender com a entrada
        self.learn_from_input(user_input)
        self.adapt_personality(user_input, user_emotion)
        
        # Escolher tipo de resposta baseado no input
        response_type = self.classify_input(user_input)
        
        # Gerar resposta baseada na personalidade
        response = self.create_contextual_response(user_input, response_type, user_emotion, user_name)
        
        # Aplicar modificadores de personalidade
        response = self.apply_personality_modifiers(response)
        
        return response
        
    def classify_input(self, user_input: str) -> str:
        """Classifica o tipo de input do usuário"""
        text_lower = user_input.lower()
        
        # Saudações
        if any(greeting in text_lower for greeting in ["oi", "olá", "hey", "e aí", "bom dia", "boa tarde", "boa noite"]):
            return "greeting"
            
        # Perguntas
        if user_input.strip().endswith("?") or any(q_word in text_lower for q_word in ["como", "quando", "onde", "por que", "o que", "qual"]):
            return "question"
            
        # Expressões de gratidão
        if any(thanks in text_lower for thanks in ["obrigado", "obrigada", "valeu", "grato", "agradecido"]):
            return "gratitude"
            
        # Compartilhamento de informação
        if any(share in text_lower for share in ["aconteceu", "fiz", "vi", "ouvi", "aprendi"]):
            return "sharing"
            
        # Pedido de ajuda
        if any(help_word in text_lower for help_word in ["ajuda", "socorro", "help", "pode me ajudar", "preciso"]):
            return "help_request"
            
        return "general"
        
    def create_contextual_response(self, user_input: str, response_type: str, user_emotion: str, user_name: str) -> str:
        """Cria resposta contextual"""
        name = user_name or "amigo"
        
        if response_type == "greeting":
            templates = self.response_templates["greeting"]
            # Usar saudação aprendida do usuário ocasionalmente
            if "user_greetings" in self.conversation_patterns and random.random() < 0.3:
                user_greeting = random.choice(self.conversation_patterns["user_greetings"])
                return f"{user_greeting.capitalize()} {name}! Como você está?"
            return random.choice(templates).format(name=name)
            
        elif response_type == "question":
            base_responses = self.response_templates["question"]
            base = random.choice(base_responses)
            
            # Tentar responder perguntas simples
            simple_responses = self.get_simple_answer(user_input)
            if simple_responses:
                return f"{base} {simple_responses}"
            else:
                return f"{base} Não tenho certeza sobre isso, mas podemos descobrir juntos!"
                
        elif response_type == "gratitude":
            return "Fico feliz em poder ajudar! 😊 Sempre que precisar, estarei aqui!"
            
        elif response_type == "sharing":
            enthusiasm = self.response_templates["enthusiasm"]
            return f"{random.choice(enthusiasm)} Conte-me mais sobre isso!"
            
        elif response_type == "help_request":
            support = self.response_templates["support"]
            return f"{random.choice(support)} Em que posso te ajudar?"
            
        else:  # general
            return self.generate_general_response(user_input, user_emotion, name)
            
    def get_simple_answer(self, question: str) -> str:
        """Responde perguntas simples"""
        q_lower = question.lower()
        
        if "seu nome" in q_lower or "como você se chama" in q_lower:
            return "Eu sou o assistente que você nomeou! Lembra?"
            
        elif "como você está" in q_lower:
            return "Estou ótimo! Sempre bem quando estou conversando com você!"
            
        elif "que horas" in q_lower:
            now = datetime.now()
            return f"São {now.hour:02d}:{now.minute:02d}!"
            
        elif "que dia" in q_lower:
            today = datetime.now()
            dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            return f"Hoje é {dias[today.weekday()]}, dia {today.day}!"
            
        return ""
        
    def generate_general_response(self, user_input: str, user_emotion: str, name: str) -> str:
        """Gera resposta geral baseada na emoção detectada"""
        if user_emotion == "sad":
            return f"Percebo que você não está muito bem, {name}. Quer conversar sobre isso? Estou aqui para te ouvir."
            
        elif user_emotion == "happy":
            return f"Que bom ver você animado, {name}! Sua alegria é contagiante! 😊"
            
        elif user_emotion == "excited":
            return f"Adoro sua empolgação, {name}! Me conta mais sobre isso!"
            
        elif user_emotion == "angry":
            return f"Vejo que você está chateado, {name}. Quer desabafar? Às vezes ajuda conversar."
            
        elif user_emotion == "confused":
            return f"Entendo, {name}. Vamos tentar esclarecer isso juntos, passo a passo."
            
        else:  # neutral
            responses = [
                f"Interessante, {name}! Me fale mais sobre isso.",
                f"Entendi, {name}. O que você acha disso?",
                f"Hmm, {name}, que perspectiva interessante!",
                f"Legal, {name}! Como você se sente em relação a isso?"
            ]
            return random.choice(responses)
            
    def apply_personality_modifiers(self, response: str) -> str:
        """Aplica modificadores baseados na personalidade"""
        # Ajustar entusiasmo
        if self.personality_traits["energy"] > 0.7:
            if not any(punct in response for punct in ["!", "😊", "😄"]):
                response = response.rstrip(".") + "!"
                
        # Adicionar emojis baseado na personalidade
        if self.personality_traits["friendliness"] > 0.7 and random.random() < 0.3:
            emojis = ["😊", "😄", "🙂", "😉"]
            if not any(emoji in response for emoji in emojis):
                response += f" {random.choice(emojis)}"
                
        # Ajustar formalidade
        if self.personality_traits["formality"] < 0.3:
            # Tornar mais informal
            response = response.replace("Você", "você")
            response = response.replace("Por favor", "por favor")
            
        # Adicionar humor ocasional
        if self.personality_traits["humor"] > 0.6 and random.random() < 0.1:
            humor_additions = [
                " (pelo menos é o que eu acho! 😅)",
                " ...ou talvez eu esteja falando bobagem! 😄",
                " - mas o que eu sei? Sou só um computador! 🤖"
            ]
            if not response.endswith(("!", "?", "😊", "😄", "🙂", "😉")):
                response += random.choice(humor_additions)
                
        return response
        
    def get_personality_summary(self) -> str:
        """Retorna resumo da personalidade atual"""
        traits = []
        
        if self.personality_traits["friendliness"] > 0.7:
            traits.append("amigável")
        if self.personality_traits["humor"] > 0.6:
            traits.append("bem-humorado")
        if self.personality_traits["empathy"] > 0.7:
            traits.append("empático")
        if self.personality_traits["energy"] > 0.7:
            traits.append("energético")
        if self.personality_traits["supportiveness"] > 0.8:
            traits.append("prestativo")
            
        if traits:
            return f"Minha personalidade atual: {', '.join(traits)}"
        else:
            return "Ainda estou desenvolvendo minha personalidade!"