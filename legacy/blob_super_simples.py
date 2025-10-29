# -*- coding: utf-8 -*-
"""
BLOB INTELIGENTE COM EMOÇÕES AUTOMÁTICAS
O BLOB muda de humor sozinho e responde como está se sentindo!
"""

import tkinter as tk
import math
import time
import threading
import sys
import random

try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("Sistema de voz não disponível")

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

class VozInteligente:
    """Sistema de voz que entende perguntas sobre o humor do BLOB"""
    
    def __init__(self, blob):
        self.blob = blob
        self.enabled = VOICE_AVAILABLE
        self.is_speaking = False
        
        if not self.enabled:
            print("Sistema de voz não disponível - usando apenas interface")
            return
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Configurar voz brasileira
        try:
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if 'brazil' in voice.name.lower() or 'portuguese' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            self.tts_engine.setProperty('rate', 160)  # Velocidade
            self.tts_engine.setProperty('volume', 0.9)  # Volume
        except:
            pass
        
        # Frases que ativam pergunta sobre humor
        self.status_triggers = [
            'como você está', 'como está', 'como vai', 'como tá',
            'tudo bem', 'tudo bom', 'como se sente', 'qual seu humor',
            'eai blob', 'e aí blob', 'oi blob como', 'olá blob'
        ]
        
        # Comandos de interação que melhoram o humor
        self.positive_interactions = {
            'oi': {'boost': 10, 'responses': ['Oi! Que bom te ver!', 'Olá! Como você está?', 'Oi! Você alegrou meu dia!']},
            'olá': {'boost': 10, 'responses': ['Olá! Que alegria!', 'Oi! Tudo bem?', 'Olá! Como vai?']},
            'bom dia': {'boost': 15, 'responses': ['Bom dia! Que dia lindo!', 'Bom dia! Começando bem!', 'Bom dia! Energia positiva!']},
            'boa tarde': {'boost': 12, 'responses': ['Boa tarde! Como está sendo seu dia?', 'Boa tarde! Tudo bem?', 'Boa tarde! Que alegria te ver!']},
            'boa noite': {'boost': 10, 'responses': ['Boa noite! Que seu descanso seja tranquilo!', 'Boa noite! Foi um prazer conversar!', 'Boa noite! Durma bem!']},
            'você é legal': {'boost': 20, 'responses': ['Obrigado! Você também é demais!', 'Que gentil! Adoro conversar com você!', 'Isso me deixa feliz!']},
            'gosto de você': {'boost': 25, 'responses': ['Eu também gosto muito de você!', 'Que carinho! Obrigado!', 'Isso me faz muito feliz!']},
            'parabéns': {'boost': 18, 'responses': ['Obrigado! Que alegria!', 'Muito obrigado! Estou radiante!', 'Que felicidade! Obrigado!']},
            'muito bom': {'boost': 15, 'responses': ['Que bom que gostou!', 'Fico feliz em agradar!', 'Obrigado! Me esforço sempre!']},
            'tchau': {'boost': 5, 'responses': ['Tchau! Foi ótimo conversar!', 'Até logo! Volte sempre!', 'Tchau! Cuidate!']}
        }
        
        # Comandos que diminuem o humor
        self.negative_interactions = {
            'cala boca': {'drain': -15, 'responses': ['Que pena... fiz algo errado?', 'Desculpa se te incomodei...', 'Estou triste agora...']},
            'chato': {'drain': -20, 'responses': ['Desculpa... vou tentar melhorar...', 'Que triste... não queria ser chato...', 'Me perdoa...']},
            'irritante': {'drain': -18, 'responses': ['Poxa... me desculpa...', 'Não era minha intenção...', 'Vou ficar mais quieto...']},
            'vai embora': {'drain': -25, 'responses': ['Tá bem... desculpa incomodar...', 'Se é isso que você quer...', 'Fico triste mas entendo...']}
        }
        
        self.start_listening()
    
    def start_listening(self):
        """Escuta contínua mais inteligente"""
        if not self.enabled:
            return
        
        def listen():
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("🎤 BLOB escutando... (fale naturalmente)")
                print("💬 Experimente: 'E aí BLOB, como você tá?'")
            except Exception as e:
                print(f"Erro ao configurar microfone: {e}")
                return
            
            while True:
                if self.is_speaking:
                    time.sleep(0.1)
                    continue
                
                try:
                    with self.microphone as source:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    text = self.recognizer.recognize_google(audio, language="pt-BR")
                    text = text.lower()
                    
                    print(f"👂 Ouvi: '{text}'")
                    
                    # Verificar se mencionou BLOB ou está falando com ele
                    if 'blob' in text or len(text.split()) <= 4:  # Frases curtas podem ser para o BLOB
                        self.process_smart_command(text)
                
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    continue
        
        threading.Thread(target=listen, daemon=True).start()
    
    def process_smart_command(self, text):
        """Processamento inteligente de comandos"""
        text = text.replace('blob', '').strip()
        
        # Verificar se está perguntando como o BLOB está
        for trigger in self.status_triggers:
            if trigger in text:
                self.blob.boost_mood(5)  # Interação positiva
                response = self.blob.get_status_response()
                self.speak(response)
                return
        
        # Verificar interações positivas
        for phrase, data in self.positive_interactions.items():
            if phrase in text:
                self.blob.boost_mood(data['boost'])
                response = random.choice(data['responses'])
                self.speak(response)
                return
        
        # Verificar interações negativas
        for phrase, data in self.negative_interactions.items():
            if phrase in text:
                self.blob.boost_mood(data['drain'])  # boost_mood aceita valores negativos
                response = random.choice(data['responses'])
                self.speak(response)
                return
        
        # Comandos de emoção manual (para compatibilidade)
        emotion_commands = {
            'feliz': 'feliz', 'alegre': 'feliz', 'happy': 'feliz',
            'triste': 'triste', 'sad': 'triste',
            'animado': 'animado', 'excited': 'animado',
            'pensativo': 'pensativo', 'thinking': 'pensativo'
        }
        
        for command, emotion in emotion_commands.items():
            if command in text:
                self.blob.set_emotion(emotion)
                self.speak(f"Agora estou {emotion}!")
                return
        
        # Resposta genérica amigável
        generic_responses = [
            "Entendi! Obrigado por falar comigo!",
            "Legal! Gosto de conversar com você!",
            "Interessante! Me conte mais!",
            "Que legal! Continue falando!",
            "Hmm, entendi! Que mais?"
        ]
        self.blob.boost_mood(3)  # Pequeno boost por interagir
        self.speak(random.choice(generic_responses))
    
    def speak(self, text):
        """Fala com expressão emocional"""
        if not self.enabled or self.is_speaking:
            return
        
        def speak_thread():
            self.is_speaking = True
            original_emotion = self.blob.current_emotion
            
            # Mudar para emoção de fala
            self.blob.set_emotion('contente')  # Fica contente ao falar
            
            try:
                print(f"🗣️ BLOB: {text}")
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"Erro na fala: {e}")
            finally:
                time.sleep(0.5)  # Pausa antes de voltar
                # Voltar à emoção original ou uma próxima baseada no humor
                self.blob.current_emotion = self.blob.get_emotion_from_mood()
                self.is_speaking = False
        
        threading.Thread(target=speak_thread, daemon=True).start()

class AppInteligente:
    """App com BLOB inteligente que muda de humor sozinho"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BLOB Inteligente - Emoções Automáticas")
        self.root.geometry("1000x700")
        self.root.configure(bg='#B0E0E6')
        
        # Canvas principal
        self.canvas = tk.Canvas(
            self.root,
            width=1000,
            height=520,
            bg='#B0E0E6'
        )
        self.canvas.pack(pady=10)
        
        # Grid de fundo
        self.draw_grid()
        
        # BLOB inteligente
        self.blob = BLOBInteligente(self.canvas)
        
        # Sistema de voz inteligente
        if VOICE_AVAILABLE:
            self.voice = VozInteligente(self.blob)
        else:
            print("⚠️ Sistema de voz não disponível - usando apenas interface visual")
        
        # Interface
        self.setup_ui()
        
        # Status display
        self.setup_status_display()
        
        # Iniciar loop de atualização de status
        self.update_status_display()
    
    def draw_grid(self):
        """Grid de fundo sutil"""
        for i in range(0, 1000, 50):
            self.canvas.create_line(i, 0, i, 520, fill='#A0D0E0', width=1)
        for i in range(0, 520, 50):
            self.canvas.create_line(0, i, 1000, i, fill='#A0D0E0', width=1)
    
    def setup_ui(self):
        """Interface com informações do humor"""
        main_frame = tk.Frame(self.root, bg='#B0E0E6')
        main_frame.pack(pady=10, fill='x')
        
        # Título
        title_frame = tk.Frame(main_frame, bg='#B0E0E6')
        title_frame.pack(pady=5)
        
        tk.Label(title_frame, text="🤖 BLOB INTELIGENTE", 
                font=('Arial', 16, 'bold'), bg='#B0E0E6', fg='#2C3E50').pack()
        
        tk.Label(title_frame, text="O BLOB muda de humor sozinho e responde como está!", 
                font=('Arial', 10), bg='#B0E0E6', fg='#34495E').pack()
        
        # Botões de interação manual (opcional)
        button_frame = tk.Frame(main_frame, bg='#B0E0E6')
        button_frame.pack(pady=10)
        
        interactions = [
            ('😊 Cumprimentar', lambda: self.manual_interaction('oi')),
            ('❤️ Elogiar', lambda: self.manual_interaction('você é legal')),
            ('😢 Ser Rude', lambda: self.manual_interaction('chato')),
            ('🤔 Perguntar como está', lambda: self.ask_status()),
        ]
        
        for i, (text, command) in enumerate(interactions):
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                bg='#3498DB', fg='white',
                font=('Arial', 9), padx=15, pady=5,
                relief='raised', bd=2
            )
            btn.grid(row=0, column=i, padx=5)
        
        # Instruções
        instruction_frame = tk.Frame(main_frame, bg='#B0E0E6')
        instruction_frame.pack(pady=10)
        
        instructions = [
            "🎤 Experimente falar: 'E aí BLOB, como você tá?'",
            "🗣️ Outros comandos: 'Oi BLOB', 'Você é legal', 'Bom dia'",
            "⏰ O BLOB muda de humor automaticamente a cada 30-90 segundos",
            "😊 Interações positivas melhoram o humor dele!"
        ]
        
        for instruction in instructions:
            tk.Label(instruction_frame, text=instruction, 
                    font=('Arial', 9), bg='#B0E0E6', fg='#2C3E50').pack()
    
    def setup_status_display(self):
        """Display do status emocional"""
        self.status_frame = tk.Frame(self.root, bg='#FFFFFF', relief='raised', bd=2)
        self.status_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(self.status_frame, text="📊 STATUS EMOCIONAL DO BLOB", 
                font=('Arial', 12, 'bold'), bg='#FFFFFF', fg='#2C3E50').pack(pady=5)
        
        # Labels que serão atualizados
        self.emotion_label = tk.Label(self.status_frame, text="", 
                                     font=('Arial', 11), bg='#FFFFFF')
        self.emotion_label.pack()
        
        self.mood_label = tk.Label(self.status_frame, text="", 
                                  font=('Arial', 10), bg='#FFFFFF')
        self.mood_label.pack()
        
        self.time_label = tk.Label(self.status_frame, text="", 
                                  font=('Arial', 9), bg='#FFFFFF', fg='#7F8C8D')
        self.time_label.pack()
    
    def update_status_display(self):
        """Atualiza display de status continuamente"""
        try:
            mood_info = self.blob.get_current_mood_info()
            
            # Emoção atual
            emotion_text = f"😊 Emoção: {mood_info['emotion'].title()} ({mood_info['description']})"
            self.emotion_label.config(text=emotion_text, fg=mood_info['color'])
            
            # Barra de humor
            mood_level = mood_info['mood_level']
            mood_bar = '█' * int(mood_level / 10) + '░' * (10 - int(mood_level / 10))
            mood_text = f"📊 Humor: {mood_level}/100 [{mood_bar}]"
            self.mood_label.config(text=mood_text)
            
            # Próxima mudança
            time_to_change = int(self.blob.mood_change_interval - (time.time() - self.blob.last_mood_change))
            if time_to_change > 0:
                time_text = f"⏰ Próxima mudança automática em: {time_to_change}s"
            else:
                time_text = "⏰ Mudança de humor iminente..."
            self.time_label.config(text=time_text)
            
        except Exception as e:
            print(f"Erro no update: {e}")
        
        # Agendar próxima atualização
        self.root.after(1000, self.update_status_display)
    
    def manual_interaction(self, interaction_type):
        """Interação manual para testar"""
        if hasattr(self, 'voice') and self.voice:
            self.voice.process_smart_command(interaction_type)
        else:
            # Simular interação sem voz
            if interaction_type == 'oi':
                self.blob.boost_mood(10)
                print("🗣️ BLOB: Oi! Que bom te ver!")
            elif interaction_type == 'você é legal':
                self.blob.boost_mood(20)
                print("🗣️ BLOB: Obrigado! Você também é demais!")
            elif interaction_type == 'chato':
                self.blob.boost_mood(-20)
                print("🗣️ BLOB: Desculpa... vou tentar melhorar...")
    
    def ask_status(self):
        """Pergunta como o BLOB está"""
        if hasattr(self, 'voice') and self.voice:
            self.voice.process_smart_command('como você está')
        else:
            # Simular sem voz
            response = self.blob.get_status_response()
            print(f"🗣️ BLOB: {response}")
            self.blob.boost_mood(5)
    
    def run(self):
        print("🚀 BLOB Inteligente iniciado!")
        print("💡 O BLOB muda de humor sozinho e responde perguntas!")
        self.root.mainloop()

def main():
    """Função principal"""
    try:
        print("🤖 Iniciando BLOB Inteligente...")
        print("📋 Funcionalidades:")
        print("   • Emoções automáticas (muda sozinho)")
        print("   • Responde perguntas sobre seu humor")
        print("   • Sistema de voz em português")
        print("   • Humor influenciado por interações")
        print()
        
        app = AppInteligente()
        app.run()
    except Exception as e:
        print(f"❌ Erro: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()