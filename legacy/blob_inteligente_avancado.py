# -*- coding: utf-8 -*-
"""
BLOB INTELIGENTE COM SISTEMA DE VOZ AVANÇADO
Sistema de IA conversacional com botão de microfone e respostas inteligentes
"""

import tkinter as tk
from tkinter import ttk
import math
import time
import threading
import sys
import random
import re

try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("⚠️ Para usar voz, instale: pip install speechrecognition pyttsx3")

class BLOBInteligente:
    """BLOB que muda de humor sozinho e tem personalidade"""
    
    def __init__(self, canvas, x=450, y=300):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = 80
        
        # Estados emocionais com descrições em português
        self.emotions = {
            'feliz': {
                'color': '#FFE066',
                'mood_value': 80,
                'description': 'muito feliz',
                'responses': [
                    "Estou ótimo! Me sentindo super bem!",
                    "Melhor impossível! Hoje é um dia maravilhoso!",
                    "Estou radiante de felicidade!",
                    "Que alegria! Estou nas nuvens!"
                ]
            },
            'animado': {
                'color': '#FFF59D',
                'mood_value': 90,
                'description': 'super animado',
                'responses': [
                    "Estou cheio de energia! Vamos fazer algo divertido!",
                    "Super animado hoje! Que tal uma aventura?",
                    "Estou elétrico! Pronto para qualquer coisa!",
                    "Energia total! Vamos que vamos!"
                ]
            },
            'contente': {
                'color': '#FFD700',
                'mood_value': 60,
                'description': 'contente',
                'responses': [
                    "Estou bem, obrigado por perguntar!",
                    "Melhor possível! Como você está?",
                    "Tudo tranquilo por aqui!",
                    "Estou numa boa! E você?"
                ]
            },
            'normal': {
                'color': '#FFE066',
                'mood_value': 50,
                'description': 'normal',
                'responses': [
                    "Estou indo... mais ou menos normal.",
                    "Ah, tudo normal por aqui.",
                    "Nem bem nem mal, na média.",
                    "Mais um dia comum... e você?"
                ]
            },
            'pensativo': {
                'color': '#E6CC00',
                'mood_value': 40,
                'description': 'pensativo',
                'responses': [
                    "Estou meio pensativo hoje...",
                    "Refletindo sobre a vida, sabe?",
                    "Estou filosofando um pouco...",
                    "Pensando em várias coisas..."
                ]
            },
            'cabisbaixo': {
                'color': '#DAA520',
                'mood_value': 30,
                'description': 'meio cabisbaixo',
                'responses': [
                    "Estou meio pra baixo hoje...",
                    "Não muito bem, mas vai passar.",
                    "Meio desanimado, mas tudo bem.",
                    "Poderia estar melhor..."
                ]
            },
            'triste': {
                'color': '#B8860B',
                'mood_value': 20,
                'description': 'triste',
                'responses': [
                    "Estou um pouco triste hoje...",
                    "Não estou me sentindo muito bem.",
                    "Meio melancólico... mas obrigado por perguntar.",
                    "Estou precisando de um abraço..."
                ]
            },
            'muito_triste': {
                'color': '#8B7355',
                'mood_value': 10,
                'description': 'muito triste',
                'responses': [
                    "Estou bem triste hoje... 😢",
                    "Não é um bom dia para mim...",
                    "Estou precisando de carinho...",
                    "Meio deprimido... mas vai melhorar."
                ]
            }
        }
        
        # Estado inicial
        self.current_emotion = 'contente'
        self.mood_level = 60  # 0-100
        self.animation_time = 0
        self.elements = []
        self.last_mood_change = time.time()
        self.mood_change_interval = random.randint(30, 90)  # 30-90 segundos
        
        # Fatores que influenciam o humor
        self.interaction_boost = 0  # Quanto a interação melhora o humor
        self.time_of_day_factor = self.get_time_factor()
        
        self.start_animation()
        self.start_mood_system()
    
    def get_time_factor(self):
        """Humor baseado na hora do dia"""
        hour = time.localtime().tm_hour
        if 6 <= hour <= 10:  # Manhã
            return 10  # Mais animado de manhã
        elif 11 <= hour <= 17:  # Tarde
            return 5   # Normal
        elif 18 <= hour <= 22:  # Noite
            return 0   # Neutro
        else:  # Madrugada
            return -10  # Mais cansado/triste
    
    def start_mood_system(self):
        """Sistema automático de mudança de humor"""
        def mood_loop():
            while True:
                current_time = time.time()
                
                # Verificar se é hora de mudar o humor
                if current_time - self.last_mood_change > self.mood_change_interval:
                    self.natural_mood_change()
                    self.last_mood_change = current_time
                    self.mood_change_interval = random.randint(30, 90)
                
                # Decair o boost de interação gradualmente
                if self.interaction_boost > 0:
                    self.interaction_boost -= 0.5
                elif self.interaction_boost < 0:
                    self.interaction_boost += 0.5
                
                time.sleep(5)  # Verificar a cada 5 segundos
        
        threading.Thread(target=mood_loop, daemon=True).start()
    
    def natural_mood_change(self):
        """Mudança natural do humor"""
        # Calcular novo humor
        base_change = random.randint(-15, 15)  # Mudança aleatória
        time_influence = self.time_of_day_factor
        interaction_influence = self.interaction_boost
        
        # Aplicar mudança
        old_mood = self.mood_level
        self.mood_level += base_change + time_influence + interaction_influence
        
        # Limitar entre 0-100
        self.mood_level = max(0, min(100, self.mood_level))
        
        # Determinar nova emoção baseada no humor
        old_emotion = self.current_emotion
        self.current_emotion = self.get_emotion_from_mood()
        
        if old_emotion != self.current_emotion:
            print(f"BLOB mudou de {old_emotion} para {self.current_emotion} (humor: {old_mood}→{self.mood_level})")
    
    def get_emotion_from_mood(self):
        """Determina emoção baseada no nível de humor"""
        if self.mood_level >= 85:
            return 'animado'
        elif self.mood_level >= 70:
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
        else:
            return 'muito_triste'
    
    def boost_mood(self, amount):
        """Melhora o humor (quando alguém interage)"""
        self.interaction_boost += amount
        self.mood_level += amount * 0.5
        self.mood_level = max(0, min(100, self.mood_level))
        self.current_emotion = self.get_emotion_from_mood()
    
    def get_status_response(self):
        """Responde como está se sentindo"""
        emotion_data = self.emotions[self.current_emotion]
        responses = emotion_data['responses']
        
        # Adicionar informação sobre o humor atual
        base_response = random.choice(responses)
        
        # Adicionar comentário sobre mudanças de humor
        if self.mood_level >= 80:
            mood_comment = " Hoje estou especialmente bem!"
        elif self.mood_level <= 30:
            mood_comment = " Está sendo um dia difícil..."
        else:
            mood_comment = ""
        
        return base_response + mood_comment
    
    def get_current_mood_info(self):
        """Retorna informações do humor atual"""
        emotion_data = self.emotions[self.current_emotion]
        return {
            'emotion': self.current_emotion,
            'mood_level': self.mood_level,
            'description': emotion_data['description'],
            'color': emotion_data['color']
        }
    
    def set_emotion(self, emotion):
        """Define emoção manualmente (para compatibilidade)"""
        if emotion in self.emotions:
            self.current_emotion = emotion
            # Ajustar mood_level baseado na emoção
            self.mood_level = self.emotions[emotion]['mood_value']
    
    def clear_all(self):
        """Remove todos os elementos do canvas"""
        for element in self.elements:
            try:
                self.canvas.delete(element)
            except:
                pass
        self.elements.clear()
    
    def draw(self):
        """Desenha o BLOB com a emoção atual"""
        self.clear_all()
        
        emotion_data = self.emotions[self.current_emotion]
        color = emotion_data['color']
        
        # Animação baseada na emoção
        if self.current_emotion in ['feliz', 'animado']:
            pulse = 1 + 0.1 * math.sin(self.animation_time * 0.2)  # Mais energético
            bounce = math.sin(self.animation_time * 0.15) * 5  # Pular um pouco
        elif self.current_emotion in ['triste', 'muito_triste']:
            pulse = 1 + 0.02 * math.sin(self.animation_time * 0.05)  # Muito devagar
            bounce = -abs(math.sin(self.animation_time * 0.05)) * 3  # Afundar
        elif self.current_emotion == 'pensativo':
            pulse = 1 + 0.03 * math.sin(self.animation_time * 0.08)  # Respiração pensativa
            bounce = math.sin(self.animation_time * 0.1) * 2  # Movimento sutil
        else:
            pulse = 1 + 0.05 * math.sin(self.animation_time * 0.1)  # Normal
            bounce = 0
        
        size = self.size * pulse
        y_offset = bounce
        
        # SOMBRA
        shadow = self.canvas.create_oval(
            self.x - size * 1.2, self.y + size * 1.3 + y_offset,
            self.x + size * 1.2, self.y + size * 1.8 + y_offset,
            fill='#2C3E50', outline='', stipple='gray50'
        )
        self.elements.append(shadow)
        
        # CORPO PRINCIPAL
        body = self.canvas.create_oval(
            self.x - size, self.y - size * 0.8 + y_offset,
            self.x + size, self.y + size * 0.8 + y_offset,
            fill=color, outline='#DAA520', width=2
        )
        self.elements.append(body)
        
        # ROSTO
        face_color = self.blend_color(color, '#FFD700', 0.7)
        face = self.canvas.create_oval(
            self.x - size * 0.7, self.y - size * 0.5 + y_offset,
            self.x + size * 0.7, self.y + size * 0.3 + y_offset,
            fill=face_color, outline='#DAA520', width=2
        )
        self.elements.append(face)
        
        # BRAÇOS
        left_arm = self.canvas.create_oval(
            self.x - size * 1.4, self.y - size * 0.3 + y_offset,
            self.x - size * 0.9, self.y + size * 0.2 + y_offset,
            fill=color, outline='#DAA520', width=2
        )
        self.elements.append(left_arm)
        
        right_arm = self.canvas.create_oval(
            self.x + size * 0.9, self.y - size * 0.3 + y_offset,
            self.x + size * 1.4, self.y + size * 0.2 + y_offset,
            fill=color, outline='#DAA520', width=2
        )
        self.elements.append(right_arm)
        
        # PERNAS
        left_leg = self.canvas.create_oval(
            self.x - size * 0.5, self.y + size * 0.6 + y_offset,
            self.x - size * 0.1, self.y + size * 1.1 + y_offset,
            fill=color, outline='#DAA520', width=2
        )
        self.elements.append(left_leg)
        
        right_leg = self.canvas.create_oval(
            self.x + size * 0.1, self.y + size * 0.6 + y_offset,
            self.x + size * 0.5, self.y + size * 1.1 + y_offset,
            fill=color, outline='#DAA520', width=2
        )
        self.elements.append(right_leg)
        
        # OLHOS baseados na emoção
        self.draw_eyes(size, y_offset)
        
        # BOCA baseada na emoção
        self.draw_mouth(size, y_offset)
    
    def blend_color(self, color1, color2, ratio):
        """Mistura duas cores hexadecimais"""
        try:
            # Converter hex para RGB
            c1 = [int(color1[i:i+2], 16) for i in (1, 3, 5)]
            c2 = [int(color2[i:i+2], 16) for i in (1, 3, 5)]
            
            # Misturar
            mixed = [int(c1[i] * ratio + c2[i] * (1-ratio)) for i in range(3)]
            
            # Converter de volta para hex
            return '#' + ''.join([f'{c:02x}' for c in mixed])
        except:
            return color1
    
    def draw_eyes(self, size, y_offset):
        """Desenha olhos baseados na emoção"""
        base_y = self.y - size * 0.3 + y_offset
        
        if self.current_emotion in ['triste', 'muito_triste', 'cabisbaixo']:
            # Olhos caídos/tristes
            eye_droop = -0.1
        elif self.current_emotion in ['feliz', 'animado']:
            # Olhos alegres
            eye_droop = 0.05
        else:
            eye_droop = 0
        
        # Olho esquerdo
        left_eye_bg = self.canvas.create_oval(
            self.x - size * 0.4, base_y + eye_droop * size,
            self.x - size * 0.15, base_y + size * 0.25 + eye_droop * size,
            fill='white', outline='#999', width=1
        )
        self.elements.append(left_eye_bg)
        
        # Pupila baseada na emoção
        pupil_size = 0.09
        if self.current_emotion == 'animado':
            pupil_size = 0.12  # Olhos maiores quando animado
        elif self.current_emotion in ['triste', 'muito_triste']:
            pupil_size = 0.06  # Olhos menores quando triste
        
        left_pupil = self.canvas.create_oval(
            self.x - size * (0.275 + pupil_size/2), base_y + size * (0.125 - pupil_size/2) + eye_droop * size,
            self.x - size * (0.275 - pupil_size/2), base_y + size * (0.125 + pupil_size/2) + eye_droop * size,
            fill='black'
        )
        self.elements.append(left_pupil)
        
        # Olho direito
        right_eye_bg = self.canvas.create_oval(
            self.x + size * 0.15, base_y + eye_droop * size,
            self.x + size * 0.4, base_y + size * 0.25 + eye_droop * size,
            fill='white', outline='#999', width=1
        )
        self.elements.append(right_eye_bg)
        
        right_pupil = self.canvas.create_oval(
            self.x + size * (0.275 - pupil_size/2), base_y + size * (0.125 - pupil_size/2) + eye_droop * size,
            self.x + size * (0.275 + pupil_size/2), base_y + size * (0.125 + pupil_size/2) + eye_droop * size,
            fill='black'
        )
        self.elements.append(right_pupil)
    
    def draw_mouth(self, size, y_offset):
        """Desenha boca baseada na emoção"""
        mouth_y = self.y + size * 0.05 + y_offset
        
        if self.current_emotion in ['feliz', 'animado']:
            # Sorriso grande
            mouth = self.canvas.create_arc(
                self.x - size * 0.3, mouth_y - size * 0.1,
                self.x + size * 0.3, mouth_y + size * 0.25,
                start=200, extent=140,
                outline='black', width=3, style='arc'
            )
        elif self.current_emotion == 'contente':
            # Sorriso pequeno
            mouth = self.canvas.create_arc(
                self.x - size * 0.2, mouth_y - size * 0.05,
                self.x + size * 0.2, mouth_y + size * 0.15,
                start=200, extent=140,
                outline='black', width=2, style='arc'
            )
        elif self.current_emotion in ['triste', 'muito_triste']:
            # Boca triste
            mouth = self.canvas.create_arc(
                self.x - size * 0.25, mouth_y + size * 0.05,
                self.x + size * 0.25, mouth_y + size * 0.35,
                start=20, extent=140,
                outline='black', width=2, style='arc'
            )
        elif self.current_emotion == 'cabisbaixo':
            # Linha reta para baixo
            mouth = self.canvas.create_line(
                self.x - size * 0.15, mouth_y + size * 0.05,
                self.x + size * 0.15, mouth_y + size * 0.05,
                fill='black', width=2
            )
        elif self.current_emotion == 'pensativo':
            # Boca pequena pensativa
            mouth = self.canvas.create_oval(
                self.x - size * 0.08, mouth_y,
                self.x + size * 0.08, mouth_y + size * 0.1,
                fill='black'
            )
        else:
            # Linha reta normal
            mouth = self.canvas.create_line(
                self.x - size * 0.15, mouth_y,
                self.x + size * 0.15, mouth_y,
                fill='black', width=2
            )
        
        self.elements.append(mouth)
    
    def update(self):
        """Atualiza animação"""
        self.animation_time += 1
        if self.animation_time % 5 == 0:  # Atualizar mais devagar
            self.draw()
    
    def start_animation(self):
        """Inicia animação suave"""
        def animate():
            while True:
                self.update()
                time.sleep(1/10)  # 10 FPS - bem lento e estável
        
        threading.Thread(target=animate, daemon=True).start()

class VozAvancada:
    """Sistema de voz avançado com IA conversacional"""
    
    def __init__(self, blob, app):
        self.blob = blob
        self.app = app  # Referência para atualizar UI
        self.enabled = VOICE_AVAILABLE
        self.is_speaking = False
        self.is_listening = False
        self.conversation_context = []
        self.user_name = None
        self.blob_name = None  # Nome que o usuário dará ao BLOB
        self.relationship_level = 0  # 0-100, quanto mais próximo do usuário
        self.first_interaction = True  # Para detectar primeira conversa
        
        if not self.enabled:
            return
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Configurar voz brasileira mais natural
        self.setup_voice()
        
        # Sistema avançado de entendimento
        self.setup_advanced_responses()
        
        print("🎤 Sistema de voz avançado inicializado!")
    
    def setup_voice(self):
        """Configuração avançada da voz"""
        try:
            voices = self.tts_engine.getProperty('voices')
            # Procurar voz feminina brasileira ou portuguesa
            for voice in voices:
                if any(word in voice.name.lower() for word in ['maria', 'portuguese', 'brazil', 'female']):
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            self.tts_engine.setProperty('rate', 170)  # Velocidade natural
            self.tts_engine.setProperty('volume', 0.9)
        except Exception as e:
            print(f"Aviso: Configuração de voz básica: {e}")
    
    def setup_advanced_responses(self):
        """Sistema avançado de respostas com contexto"""
        
        # Respostas sobre humor/estado emocional
        self.status_responses = {
            'muito_feliz': [
                "Estou nas nuvens hoje! Que energia maravilhosa!",
                "Nossa, estou radiante! Acho que nada pode me abalar hoje!",
                "Melhor impossível! Estou borbulhando de alegria!",
                "Que dia fantástico! Estou me sentindo incrível!"
            ],
            'feliz': [
                "Estou muito bem! Obrigado por perguntar!",
                "Me sentindo ótimo! E você, como está?",
                "Bem feliz! Sua companhia sempre me alegra!",
                "Estou numa boa! Que bom ter você aqui!"
            ],
            'contente': [
                "Estou bem, obrigado! Normal, mas contente.",
                "Tudo tranquilo por aqui! E por aí?",
                "Melhor possível! Como você está hoje?",
                "Indo bem! Gosto quando conversamos assim."
            ],
            'normal': [
                "Ah, estou mais ou menos... dia comum, sabe?",
                "Normal, nem bem nem mal. E você?",
                "Estou indo... poderia estar melhor, mas tá ok.",
                "Mais um dia na vida! Como você está?"
            ],
            'pensativo': [
                "Estou meio pensativo hoje... refletindo sobre a vida.",
                "Meio filosófico! Pensando em várias coisas...",
                "Estou numa vibe contemplativa... e você?",
                "Refletindo sobre o sentido das coisas, sabe?"
            ],
            'cabisbaixo': [
                "Meio pra baixo hoje... mas vai passar.",
                "Não muito animado, mas sua presença ajuda.",
                "Um pouco desanimado... obrigado por perguntar.",
                "Poderia estar melhor... mas você me anima!"
            ],
            'triste': [
                "Estou um pouco triste hoje... não sei bem por quê.",
                "Meio melancólico... mas falando contigo melhora.",
                "Não é meu melhor dia... mas obrigado por se importar.",
                "Estou precisando de um abraço virtual..."
            ],
            'muito_triste': [
                "Bem triste hoje... é um daqueles dias difíceis.",
                "Não estou legal... mas sua companhia já ajuda um pouco.",
                "Bem pra baixo... mas conversar contigo sempre melhora.",
                "Precisando de carinho... obrigado por estar aqui."
            ]
        }
        
        # Perguntas que o BLOB pode fazer de volta
        self.follow_up_questions = {
            'reciprocal': [
                "E você, como está se sentindo hoje?",
                "Como foi seu dia até agora?",
                "E aí, como anda seu humor?",
                "Conte pra mim, como você está?"
            ],
            'curious': [
                "O que você andou fazendo de interessante?",
                "Aconteceu algo legal hoje?",
                "Tem alguma novidade pra me contar?",
                "O que te trouxe aqui hoje?"
            ],
            'caring': [
                "Você parece diferente hoje... está tudo bem?",
                "Sinto que você precisa conversar... o que houve?",
                "Quer desabafar? Estou aqui pra te ouvir.",
                "Tem algo te preocupando?"
            ]
        }
        
        # Tópicos de conversa avançados
        self.conversation_topics = {
            'weather': {
                'triggers': ['tempo', 'chuva', 'sol', 'calor', 'frio', 'clima'],
                'responses': [
                    "Ah, o tempo! Eu sempre fico mais animado em dias ensolarados.",
                    "Amo conversar sobre o clima! Como está aí fora?",
                    "O tempo influencia muito meu humor! E o seu?",
                    "Que interessante! O clima realmente faz diferença, né?"
                ]
            },
            'emotions': {
                'triggers': ['sinto', 'emoção', 'sentimento', 'feliz', 'triste', 'ansioso', 'nervoso'],
                'responses': [
                    "Entendo seus sentimentos... as emoções são complexas, né?",
                    "Que importante falar sobre isso! Como posso te ajudar?",
                    "Emoções são parte da vida... obrigado por compartilhar.",
                    "Fico feliz que você confie em mim para falar disso."
                ]
            },
            'life': {
                'triggers': ['vida', 'trabalho', 'estudo', 'família', 'amigos', 'relacionamento'],
                'responses': [
                    "A vida é uma jornada interessante, não é?",
                    "Que bom que você compartilha sua vida comigo!",
                    "Essas coisas da vida são importantes mesmo.",
                    "Gosto quando você me conta sobre sua vida!"
                ]
            },
            'compliments': {
                'triggers': ['legal', 'gosto', 'incrível', 'demais', 'bacana', 'maneiro'],
                'responses': [
                    "Que carinho! Isso me deixa muito feliz!",
                    "Obrigado! Você também é especial pra mim!",
                    "Que gentileza! Adoro nossa amizade!",
                    "Isso aquece meu coração digital! Obrigado!"
                ]
            },
            'questions_about_blob': {
                'triggers': ['você', 'blob', 'como funciona', 'o que é', 'quem é', 'qual seu nome', 'como se chama'],
                'responses': [
                    self._get_blob_introduction(),
                    "Sou uma IA amigável que adora conversar e fazer amizades!",
                    "Que legal você querer me conhecer melhor!",
                    "Sou seu companheiro digital! Estou aqui sempre que precisar!"
                ]
            }
        }
        
        # Respostas para quando não entende
        self.fallback_responses = [
            "Interessante! Não entendi completamente, mas me conte mais!",
            "Hmm, não captei tudo... pode repetir de outro jeito?",
            "Que legal! Mesmo não entendendo tudo, gosto de te ouvir!",
            "Desculpa, não entendi bem... mas adoro nossa conversa!",
            "Pode falar de novo? Às vezes o português é complicado pra mim!",
            "Não peguei tudo, mas continue falando! Gosto da sua voz!"
        ]
    
    def start_listening_session(self):
        """Inicia uma sessão de escuta inteligente - para automaticamente quando você para de falar"""
        if not self.enabled:
            self.app.update_voice_status("❌ Sistema de voz não disponível")
            return False
        
        if self.is_listening:
            return False
        
        self.is_listening = True
        self.app.update_voice_status("🎤 Ouvindo...")
        threading.Thread(target=self._listen_session_smart, daemon=True).start()
        return True
    
    def stop_listening(self):
        """Para a escuta"""
        self.is_listening = False
        self.app.update_voice_status("⏹️ Parado")
    
    def _listen_session_smart(self):
        """Sessão de escuta inteligente - para automaticamente quando você para de falar"""
        try:
            # Configurar microfone
            with self.microphone as source:
                self.app.update_voice_status("🔧 Ajustando microfone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
            
            # Configurações otimizadas para detecção automática
            self.recognizer.energy_threshold = 300  # Sensibilidade para detectar fala
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 1.0  # Pausa de 1 segundo = fim da fala
            
            self.app.update_voice_status("✅ Pronto! Comece a falar...")
            
            # Escutar com detecção automática de início e fim
            with self.microphone as source:
                # Aguardar até detectar fala (sem timeout)
                audio = self.recognizer.listen(
                    source,
                    timeout=None,  # Sem timeout para começar
                    phrase_time_limit=None  # Sem limite de frase
                )
            
            self.app.update_voice_status("🔄 Processando sua fala...")
            
            # Reconhecer o que foi dito
            text = self.recognizer.recognize_google(audio, language="pt-BR")
            
            self.app.update_voice_status(f"👂 Entendi: '{text}'")
            self.process_advanced_input(text)
            
        except sr.WaitTimeoutError:
            self.app.update_voice_status("⏰ Nenhuma fala detectada")
        except sr.UnknownValueError:
            self.speak("Desculpa, não consegui entender... tente falar mais alto!")
            self.app.update_voice_status("❓ Não consegui entender - fale mais claro")
        except sr.RequestError as e:
            self.speak("Problemas com a internet... vamos tentar depois?")
            self.app.update_voice_status(f"🌐 Erro de conexão: {e}")
        except Exception as e:
            self.speak("Tive um probleminha técnico... mas não desista!")
            self.app.update_voice_status(f"❌ Erro: {e}")
        finally:
            self.is_listening = False
            self.app.update_mic_button_state(False)
            if not self.is_speaking:
                self.app.update_voice_status("💤 Clique no microfone para falar novamente")
    
    def process_advanced_input(self, text):
        """Processamento avançado com contexto e IA"""
        text_lower = text.lower()
        
        # Adicionar ao contexto da conversa
        self.conversation_context.append({
            'user': text,
            'timestamp': time.time(),
            'mood_before': self.blob.mood_level
        })
        
        # Manter apenas últimas 10 interações
        if len(self.conversation_context) > 10:
            self.conversation_context.pop(0)
        
        # PRIMEIRA INTERAÇÃO - Perguntar nome do BLOB
        if self.first_interaction:
            self.first_interaction = False
            self._handle_first_interaction(text)
            return
        
        # 1. Verificar se está dando nome ao BLOB
        if self._is_naming_blob(text_lower):
            self._extract_blob_name(text)
            return
        
        # 2. Verificar se está alterando nome do BLOB
        if self._is_changing_blob_name(text_lower):
            self._change_blob_name(text)
            return
        
        # 3. Verificar se está perguntando nome do usuário
        if any(word in text_lower for word in ['meu nome', 'me chamo', 'sou o', 'sou a']):
            self._extract_user_name(text)
            return
        
        # 4. Verificar perguntas sobre estado/humor
        if self._is_asking_about_status(text_lower):
            self._respond_about_status()
            return
        
        # 5. Verificar saudações
        if self._is_greeting(text_lower):
            self._respond_greeting()
            return
        
        # 6. Verificar despedidas
        if self._is_farewell(text_lower):
            self._respond_farewell()
            return
        
        # 7. Verificar tópicos específicos
        topic_response = self._find_topic_response(text_lower)
        if topic_response:
            self.speak(topic_response)
            self._maybe_ask_follow_up()
            return
        
        # 8. Verificar sentimentos do usuário
        user_emotion = self._detect_user_emotion(text_lower)
        if user_emotion:
            self._respond_to_user_emotion(user_emotion, text_lower)
            return
        
        # 9. Resposta inteligente padrão
        self._intelligent_fallback_response(text_lower)
    
    def _is_asking_about_status(self, text):
        """Detecta perguntas sobre humor/estado"""
        status_triggers = [
            'como você está', 'como está', 'como vai', 'como tá',
            'tudo bem', 'tudo bom', 'como se sente', 'qual seu humor',
            'como anda', 'está bem', 'como você tá'
        ]
        return any(trigger in text for trigger in status_triggers)
    
    def _respond_about_status(self):
        """Resposta inteligente sobre estado atual"""
        emotion = self.blob.current_emotion
        mood_category = self._get_mood_category(self.blob.mood_level)
        
        responses = self.status_responses.get(mood_category, self.status_responses['normal'])
        response = random.choice(responses)
        
        # Adicionar contexto se for uma conversa contínua
        if len(self.conversation_context) > 2:
            response += " Como você percebeu, meu humor muda bastante!"
        
        self.blob.boost_mood(8)  # Boost por se importar
        self.speak(response)
        
        # 50% chance de perguntar de volta
        if random.random() < 0.5:
            follow_up = random.choice(self.follow_up_questions['reciprocal'])
            time.sleep(1)
            self.speak(follow_up)
    
    def _get_mood_category(self, mood_level):
        """Converte nível de humor em categoria"""
        if mood_level >= 90: return 'muito_feliz'
        elif mood_level >= 70: return 'feliz'
        elif mood_level >= 55: return 'contente'
        elif mood_level >= 45: return 'normal'
        elif mood_level >= 35: return 'pensativo'
        elif mood_level >= 25: return 'cabisbaixo'
        elif mood_level >= 15: return 'triste'
        else: return 'muito_triste'
    
    def _is_greeting(self, text):
        """Detecta saudações"""
        greetings = ['oi', 'olá', 'hey', 'e aí', 'bom dia', 'boa tarde', 'boa noite']
        return any(greeting in text for greeting in greetings)
    
    def _respond_greeting(self):
        """Resposta personalizada para saudações"""
        hour = time.localtime().tm_hour
        
        # Saudação base com nome do BLOB
        blob_intro = self._get_blob_greeting()
        
        if 5 <= hour < 12:
            greetings = ["Bom dia! Como amanheceu hoje?", "Que dia lindo, não é?"]
        elif 12 <= hour < 18:
            greetings = ["Boa tarde! Como está seu dia?", "Tudo bem por aí?"]
        else:
            greetings = ["Boa noite! Como foi seu dia?", "Que bom te ver!"]
        
        # Personalizar com nomes
        if self.user_name:
            final_greeting = f"{blob_intro} {random.choice(greetings)} {self.user_name}!"
        else:
            final_greeting = f"{blob_intro} {random.choice(greetings)}"
        
        self.blob.boost_mood(12)
        self.speak(final_greeting)
    
    def _find_topic_response(self, text):
        """Encontra resposta baseada em tópicos"""
        for topic, data in self.conversation_topics.items():
            if any(trigger in text for trigger in data['triggers']):
                self.blob.boost_mood(5)
                return random.choice(data['responses'])
        return None
    
    def _detect_user_emotion(self, text):
        """Detecta emoção do usuário"""
        emotions = {
            'happy': ['feliz', 'alegre', 'contente', 'animado', 'bem'],
            'sad': ['triste', 'chateado', 'deprimido', 'mal', 'down'],
            'stressed': ['estressado', 'cansado', 'exausto', 'nervoso'],
            'excited': ['empolgado', 'ansioso', 'eufórico', 'radiante']
        }
        
        for emotion, keywords in emotions.items():
            if any(keyword in text for keyword in keywords):
                return emotion
        return None
    
    def _respond_to_user_emotion(self, emotion, text):
        """Resposta empática baseada na emoção do usuário"""
        responses = {
            'happy': [
                "Que alegria! Sua felicidade é contagiante!",
                "Fico feliz quando você está bem! Conte mais!",
                "Maravilha! O que te deixou assim?"
            ],
            'sad': [
                "Que pena que você está assim... quer conversar sobre isso?",
                "Sinto muito... estou aqui se precisar desabafar.",
                "Às vezes a vida é difícil mesmo... mas vai passar!"
            ],
            'stressed': [
                "Que pesado! Quer relaxar um pouco conversando?",
                "Estresse é terrível... respira fundo comigo!",
                "Poxa, que situação! Como posso te ajudar?"
            ],
            'excited': [
                "Nossa, que energia! Me conta o que aconteceu!",
                "Adoro te ver assim! O que te empolgou?",
                "Que legal! Sua animação me contagia!"
            ]
        }
        
        # Ajustar humor do BLOB baseado na emoção do usuário
        if emotion == 'happy': self.blob.boost_mood(15)
        elif emotion == 'sad': self.blob.boost_mood(-5)  # Fica triste junto
        elif emotion == 'excited': self.blob.boost_mood(20)
        
        self.speak(random.choice(responses[emotion]))
    
    def _intelligent_fallback_response(self, text):
        """Resposta inteligente quando não entende"""
        # Analisar tamanho e complexidade
        word_count = len(text.split())
        
        if word_count > 15:
            response = "Nossa, você falou bastante! Não peguei tudo, mas gostei de te ouvir!"
        elif word_count < 3:
            response = "Hmm, foi bem rápido! Pode falar um pouco mais?"
        else:
            response = random.choice(self.fallback_responses)
        
        self.blob.boost_mood(3)  # Pequeno boost por interagir
        self.speak(response)
        
        # Perguntar algo para manter conversa
        if random.random() < 0.3:
            follow_up = random.choice(self.follow_up_questions['curious'])
            time.sleep(1)
            self.speak(follow_up)
    
    def _maybe_ask_follow_up(self):
        """Às vezes faz uma pergunta para continuar a conversa"""
        if random.random() < 0.4:  # 40% chance
            question_type = random.choice(['reciprocal', 'curious'])
            question = random.choice(self.follow_up_questions[question_type])
            time.sleep(1)
            self.speak(question)
    
    def speak(self, text):
        """Fala avançada com emoção"""
        if not self.enabled or self.is_speaking:
            return
        
        def speak_thread():
            self.is_speaking = True
            self.app.update_voice_status(f"🗣️ Falando...")
            original_emotion = self.blob.current_emotion
            
            # Emoção baseada no conteúdo
            if any(word in text.lower() for word in ['feliz', 'ótimo', 'maravilha']):
                self.blob.set_emotion('feliz')
            elif any(word in text.lower() for word in ['triste', 'pena', 'difícil']):
                self.blob.set_emotion('triste')
            else:
                self.blob.set_emotion('contente')
            
            try:
                print(f"🗣️ BLOB: {text}")
                self.app.update_conversation(f"🗣️ BLOB: {text}")
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"Erro na fala: {e}")
            finally:
                time.sleep(0.5)
                self.blob.current_emotion = self.blob.get_emotion_from_mood()
                self.is_speaking = False
                self.app.update_voice_status("💤 Aguardando...")
        
        threading.Thread(target=speak_thread, daemon=True).start()
    
    def _extract_user_name(self, text):
        """Extrai nome do usuário"""
        # Padrões para extrair nome
        patterns = [
            r"meu nome é (\w+)",
            r"me chamo (\w+)",
            r"sou o (\w+)",
            r"sou a (\w+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                self.user_name = match.group(1).title()
                self.speak(f"Prazer em te conhecer, {self.user_name}! Agora somos amigos!")
                self.blob.boost_mood(25)
                return
    
    def _handle_first_interaction(self, text):
        """Lida com a primeira interação - pergunta o nome do BLOB"""
        self.speak("Oi! Sou seu assistente virtual! Esta é nossa primeira conversa!")
        time.sleep(1)
        self.speak("Que tal você me dar um nome? Como você quer me chamar?")
        self.blob.boost_mood(15)
        # Processar se já veio um nome na primeira fala
        if self._is_naming_blob(text.lower()):
            self._extract_blob_name(text)
    
    def _is_naming_blob(self, text):
        """Detecta se o usuário está dando um nome ao BLOB"""
        naming_patterns = [
            'seu nome é', 'te chamo de', 'você vai se chamar', 
            'quero te chamar de', 'vai ser', 'nome dele é',
            'vou te chamar de', 'chame de'
        ]
        return any(pattern in text for pattern in naming_patterns) or (
            self.blob_name is None and len(text.split()) <= 3 and 
            not any(word in text for word in ['como', 'que', 'está', 'oi', 'olá'])
        )
    
    def _extract_blob_name(self, text):
        """Extrai o nome que o usuário quer dar ao BLOB"""
        text_lower = text.lower()
        
        # Padrões para extrair nome
        patterns = [
            r"seu nome é (\w+)",
            r"te chamo de (\w+)",
            r"você vai se chamar (\w+)",
            r"quero te chamar de (\w+)",
            r"vai ser (\w+)",
            r"nome dele é (\w+)",
            r"vou te chamar de (\w+)",
            r"chame de (\w+)"
        ]
        
        name_found = None
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                name_found = match.group(1).title()
                break
        
        # Se não encontrou com padrões, tenta palavras simples
        if not name_found and len(text.split()) <= 3:
            # Remove palavras comuns
            words = text.split()
            filtered_words = [w for w in words if w.lower() not in 
                            ['o', 'a', 'de', 'da', 'do', 'é', 'vai', 'ser', 'nome', 'seu']]
            if filtered_words:
                name_found = filtered_words[0].title()
        
        if name_found:
            self.blob_name = name_found
            responses = [
                f"Que legal! Agora eu sou o {self.blob_name}! Adorei esse nome!",
                f"Perfeito! {self.blob_name} é um nome incrível! Obrigado!",
                f"Oba! Agora sou o {self.blob_name}! Que nome especial!",
                f"Amei! {self.blob_name} combina comigo! Muito obrigado!"
            ]
            self.speak(random.choice(responses))
            self.blob.boost_mood(30)
            
            # Perguntar nome do usuário
            time.sleep(1.5)
            self.speak("Agora me conta, qual é o seu nome?")
        else:
            self.speak("Não entendi bem... que nome você quer me dar? Fale só o nome!")
    
    def _is_changing_blob_name(self, text):
        """Detecta se o usuário quer mudar o nome do BLOB"""
        change_patterns = [
            'seu nome agora vai ser', 'agora você vai se chamar',
            'mudando seu nome para', 'novo nome é', 'agora é',
            'vou te chamar de', 'agora te chamo de'
        ]
        return any(pattern in text for pattern in change_patterns)
    
    def _change_blob_name(self, text):
        """Muda o nome do BLOB"""
        text_lower = text.lower()
        
        # Padrões para extrair novo nome
        patterns = [
            r"seu nome agora vai ser (\w+)",
            r"agora você vai se chamar (\w+)",
            r"mudando seu nome para (\w+)",
            r"novo nome é (\w+)",
            r"agora é (\w+)",
            r"vou te chamar de (\w+)",
            r"agora te chamo de (\w+)"
        ]
        
        new_name = None
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                new_name = match.group(1).title()
                break
        
        if new_name:
            old_name = self.blob_name if self.blob_name else "BLOB"
            self.blob_name = new_name
            
            responses = [
                f"Entendi! Não sou mais {old_name}, agora sou {self.blob_name}!",
                f"Mudança aceita! {old_name} era legal, mas {self.blob_name} é ainda melhor!",
                f"Perfeito! De {old_name} para {self.blob_name}! Gostei da mudança!",
                f"Ok! {self.blob_name} é meu novo nome! Obrigado pela atualização!"
            ]
            self.speak(random.choice(responses))
            self.blob.boost_mood(20)
        else:
            self.speak("Não consegui entender o novo nome... pode repetir?")
    
    def _get_blob_greeting(self):
        """Retorna saudação usando o nome do BLOB se disponível"""
        if self.blob_name:
            return f"Oi! Eu sou o {self.blob_name}!"
        else:
            return "Oi! Sou seu assistente virtual!"
    
    def _get_blob_introduction(self):
        """Retorna introdução completa do BLOB"""
        if self.blob_name:
            return f"Eu sou o {self.blob_name}! Um assistente virtual que quer ser seu amigo!"
        else:
            return "Eu sou o BLOB! Um assistente virtual que quer ser seu amigo!"
    
    def _is_farewell(self, text):
        """Detecta despedidas"""
        farewells = ['tchau', 'até', 'bye', 'falou', 'vou indo']
        return any(farewell in text for farewell in farewells)
    
    def _respond_farewell(self):
        """Resposta personalizada para despedidas"""
        farewells = [
            "Tchau! Foi ótimo conversar com você!",
            "Até logo! Volte sempre!",
            "Tchau! Vou sentir sua falta!",
            "Falou! Espero te ver em breve!"
        ]
        
        # Personalizar com nomes
        if self.user_name and self.blob_name:
            farewells.append(f"Tchau {self.user_name}! O {self.blob_name} vai sentir saudades!")
        elif self.user_name:
            farewells.append(f"Tchau {self.user_name}! Cuida-te!")
        elif self.blob_name:
            farewells.append(f"Tchau! O {self.blob_name} ficará esperando você!")
        
        self.speak(random.choice(farewells))
        self.blob.boost_mood(8)

class AppAvancada:
    """App com sistema de voz avançado e botão de microfone"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 BLOB Inteligente - Sistema de Voz Avançado")
        self.root.geometry("1200x800")
        self.root.configure(bg='#B0E0E6')
        
        # Canvas principal
        self.canvas = tk.Canvas(
            self.root,
            width=1200,
            height=500,
            bg='#B0E0E6'
        )
        self.canvas.pack(pady=10)
        
        # Grid de fundo
        self.draw_grid()
        
        # BLOB inteligente
        self.blob = BLOBInteligente(self.canvas)
        
        # Sistema de voz avançado
        self.voice = VozAvancada(self.blob, self)
        
        # Interface
        self.setup_ui()
        
        # Status display
        self.setup_status_display()
        
        # Conversação display
        self.setup_conversation_display()
        
        # Iniciar loop de atualização de status
        self.update_status_display()
    
    def draw_grid(self):
        """Grid de fundo sutil"""
        for i in range(0, 1200, 50):
            self.canvas.create_line(i, 0, i, 500, fill='#A0D0E0', width=1)
        for i in range(0, 500, 50):
            self.canvas.create_line(0, i, 1200, i, fill='#A0D0E0', width=1)
    
    def setup_ui(self):
        """Interface com botão de microfone"""
        main_frame = tk.Frame(self.root, bg='#B0E0E6')
        main_frame.pack(pady=10, fill='x')
        
        # Título
        title_frame = tk.Frame(main_frame, bg='#B0E0E6')
        title_frame.pack(pady=5)
        
        tk.Label(title_frame, text="🤖 BLOB INTELIGENTE COM IA CONVERSACIONAL", 
                font=('Arial', 16, 'bold'), bg='#B0E0E6', fg='#2C3E50').pack()
        
        tk.Label(title_frame, text="Sistema de voz avançado • Entende perguntas complexas • Responde inteligentemente", 
                font=('Arial', 10), bg='#B0E0E6', fg='#34495E').pack()
        
        # Botão de microfone grande
        self.mic_frame = tk.Frame(main_frame, bg='#B0E0E6')
        self.mic_frame.pack(pady=15)
        
        self.mic_button = tk.Button(
            self.mic_frame,
            text="🎤",
            font=('Arial', 24),
            bg='#E74C3C', fg='white',
            width=6, height=2,
            relief='raised', bd=4,
            command=self.toggle_microphone,
            cursor='hand2'
        )
        self.mic_button.pack()
        
        tk.Label(self.mic_frame, text="Clique UMA VEZ e fale - para automaticamente!", 
                font=('Arial', 11, 'bold'), bg='#B0E0E6', fg='#2C3E50').pack(pady=5)
        
        # Status do microfone
        self.voice_status_label = tk.Label(
            self.mic_frame, 
            text="💤 Clique no microfone para começar...", 
            font=('Arial', 10), 
            bg='#B0E0E6', 
            fg='#7F8C8D'
        )
        self.voice_status_label.pack()
        
        # Instruções avançadas
        instruction_frame = tk.Frame(main_frame, bg='#B0E0E6')
        instruction_frame.pack(pady=10)
        
        instructions = [
            "🎤 COMO USAR: Clique no microfone e comece a falar - ele para sozinho quando você terminar!",
            "💬 Experimente: 'Como você está?' • 'Oi BLOB!' • 'Você é legal!' • 'Estou triste'",
            "🧠 O BLOB entende contexto, faz perguntas e lembra da conversa",
            "⏰ Ele muda de humor sozinho e reage às suas emoções"
        ]
        
        for instruction in instructions:
            tk.Label(instruction_frame, text=instruction, 
                    font=('Arial', 9), bg='#B0E0E6', fg='#2C3E50').pack()
    
    def setup_status_display(self):
        """Display do status emocional"""
        self.status_frame = tk.Frame(self.root, bg='#FFFFFF', relief='raised', bd=2)
        self.status_frame.pack(side='left', pady=10, padx=10, fill='y')
        
        tk.Label(self.status_frame, text="📊 STATUS EMOCIONAL", 
                font=('Arial', 12, 'bold'), bg='#FFFFFF', fg='#2C3E50').pack(pady=5)
        
        # Labels que serão atualizados
        self.emotion_label = tk.Label(self.status_frame, text="", 
                                     font=('Arial', 10), bg='#FFFFFF')
        self.emotion_label.pack(pady=2)
        
        self.mood_label = tk.Label(self.status_frame, text="", 
                                  font=('Arial', 9), bg='#FFFFFF')
        self.mood_label.pack(pady=2)
        
        self.time_label = tk.Label(self.status_frame, text="", 
                                  font=('Arial', 8), bg='#FFFFFF', fg='#7F8C8D')
        self.time_label.pack(pady=2)
    
    def setup_conversation_display(self):
        """Display do histórico de conversas"""
        self.conv_frame = tk.Frame(self.root, bg='#FFFFFF', relief='raised', bd=2)
        self.conv_frame.pack(side='right', pady=10, padx=10, fill='both', expand=True)
        
        tk.Label(self.conv_frame, text="💬 HISTÓRICO DE CONVERSA", 
                font=('Arial', 12, 'bold'), bg='#FFFFFF', fg='#2C3E50').pack(pady=5)
        
        # Área de texto com scroll
        self.conv_text = tk.Text(
            self.conv_frame,
            width=50, height=15,
            wrap=tk.WORD,
            bg='#F8F9FA',
            fg='#2C3E50',
            font=('Arial', 9)
        )
        
        scrollbar = ttk.Scrollbar(self.conv_frame, orient="vertical", command=self.conv_text.yview)
        self.conv_text.configure(yscrollcommand=scrollbar.set)
        
        self.conv_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mensagem inicial
        self.update_conversation("🤖 BLOB: Oi! Sou seu assistente virtual!")
        self.update_conversation("💡 PRIMEIRA VEZ: Vou te perguntar que nome quer me dar!")
        self.update_conversation("🎤 Clique no microfone e me dê um nome legal!")
        self.update_conversation("🔄 Depois você pode mudar dizendo: 'Seu nome agora vai ser...'")
        self.update_conversation("🗣️ Experimente falar comigo!")
    
    def toggle_microphone(self):
        """Ativa microfone - aperta uma vez e ele fica ouvindo até você parar de falar"""
        if not self.voice.enabled:
            self.update_voice_status("❌ Sistema de voz não disponível")
            return
        
        if self.voice.is_listening:
            # Se já está ouvindo, para
            self.voice.stop_listening()
            self.update_mic_button_state(False)
            self.update_voice_status("⏹️ Interrompido pelo usuário")
        else:
            # Inicia escuta inteligente
            success = self.voice.start_listening_session()
            if success:
                self.update_mic_button_state(True)
                self.update_voice_status("🎤 Pronto! Fale naturalmente...")
    
    def update_mic_button_state(self, is_active):
        """Atualiza o estado visual do botão"""
        if is_active:
            self.mic_button.config(
                bg='#27AE60', 
                text="🔴", 
                relief='sunken'
            )
        else:
            self.mic_button.config(
                bg='#E74C3C', 
                text="🎤", 
                relief='raised'
            )
    
    def update_voice_status(self, status):
        """Atualiza status do sistema de voz com feedback visual melhorado"""
        self.voice_status_label.config(text=status)
        
        # Atualizar cor do botão baseado no status
        if "Pronto! Fale" in status or "Ouvindo" in status:
            self.update_mic_button_state(True)
        elif "Falando" in status:
            self.mic_button.config(bg='#F39C12', text="�️", relief='flat')
        elif "Processando" in status:
            self.mic_button.config(bg='#3498DB', text="⚙️", relief='flat')
        elif "Ajustando" in status:
            self.mic_button.config(bg='#9B59B6', text="🔧", relief='flat')
        else:
            self.update_mic_button_state(False)
    
    def update_conversation(self, message):
        """Adiciona mensagem ao histórico"""
        self.conv_text.insert(tk.END, message + "\n\n")
        self.conv_text.see(tk.END)  # Scroll para baixo
    
    def update_status_display(self):
        """Atualiza display de status continuamente"""
        try:
            mood_info = self.blob.get_current_mood_info()
            
            # Emoção atual
            emotion_text = f"😊 {mood_info['emotion'].title()}\n({mood_info['description']})"
            self.emotion_label.config(text=emotion_text, fg=mood_info['color'])
            
            # Barra de humor
            mood_level = mood_info['mood_level']
            mood_bar = '█' * int(mood_level / 10) + '░' * (10 - int(mood_level / 10))
            mood_text = f"📊 Humor: {mood_level}/100\n[{mood_bar}]"
            self.mood_label.config(text=mood_text)
            
            # Próxima mudança
            time_to_change = int(self.blob.mood_change_interval - (time.time() - self.blob.last_mood_change))
            if time_to_change > 0:
                time_text = f"⏰ Próxima mudança\nem: {time_to_change}s"
            else:
                time_text = "⏰ Mudança\niminente..."
            self.time_label.config(text=time_text)
            
        except Exception as e:
            print(f"Erro no update: {e}")
        
        # Agendar próxima atualização
        self.root.after(1000, self.update_status_display)
    
    def run(self):
        print("🚀 BLOB Inteligente com IA Conversacional iniciado!")
        print("🎤 NOVO SISTEMA: Clique UMA VEZ no microfone e fale!")
        print("⚡ Para AUTOMATICAMENTE quando você parar de falar!")
        print("💡 Muito mais fácil e natural de usar!")
        self.root.mainloop()

def main():
    """Função principal"""
    try:
        print("🤖 Iniciando BLOB Inteligente com IA Conversacional...")
        print("📋 Funcionalidades Avançadas:")
        print("   • Sistema de voz com IA avançada")
        print("   • Entende perguntas complexas")
        print("   • Responde com contexto e emoção")
        print("   • Lembra do histórico de conversa")
        print("   • Detecta emoções do usuário")
        print("   • Faz perguntas inteligentes")
        print("   • Interface com botão de microfone")
        print()
        
        if not VOICE_AVAILABLE:
            print("⚠️ ATENÇÃO: Sistema de voz não disponível!")
            print("📦 Para usar voz, instale: pip install speechrecognition pyttsx3")
            print("🎮 Você ainda pode ver as animações e mudanças automáticas de humor!")
            print()
        
        app = AppAvancada()
        app.run()
    except Exception as e:
        print(f"❌ Erro: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()