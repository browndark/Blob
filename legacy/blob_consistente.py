# -*- coding: utf-8 -*-
"""
BLOB 3D CONSISTENTE - Baseado no modelo visual fornecido
Versão simplificada e estável
"""

import tkinter as tk
from tkinter import ttk
import math
import time
import threading
import random
from dataclasses import dataclass
from typing import List, Tuple
import sys
import os

try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("Sistema de voz nao disponivel - instale: pip install speechrecognition pyttsx3 pyaudio")

@dataclass
class Vector3:
    """Classe para vetores 3D simplificados"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

class SimpleBLOB:
    """BLOB simples e consistente baseado no modelo visual"""
    
    def __init__(self, canvas, x=400, y=300, size=100):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.base_size = size
        self.current_size = size
        
        # Sistema de emoções com cores consistentes
        self.emotions = {
            'neutral': {'color': '#FFD700', 'pulse': 1.0},
            'happy': {'color': '#FFED4A', 'pulse': 1.1},
            'sad': {'color': '#E6C200', 'pulse': 0.9},
            'excited': {'color': '#FFF59D', 'pulse': 1.2},
            'angry': {'color': '#FFB300', 'pulse': 1.1},
            'thinking': {'color': '#FFCC02', 'pulse': 0.95},
            'speaking': {'color': '#FFF176', 'pulse': 1.15},
            'surprised': {'color': '#FFEB3B', 'pulse': 1.3}
        }
        
        self.current_emotion = 'neutral'
        self.is_speaking = False
        self.animation_time = 0
        
        # IDs dos elementos para limpeza
        self.all_elements = []
        
        self.start_animation()
    
    def set_emotion(self, emotion: str):
        """Define emoção do BLOB"""
        if emotion in self.emotions:
            self.current_emotion = emotion
    
    def clear_canvas(self):
        """Limpa todos os elementos do BLOB"""
        for element_id in self.all_elements:
            try:
                self.canvas.delete(element_id)
            except:
                pass
        self.all_elements.clear()
    
    def draw(self):
        """Desenha o BLOB de forma consistente baseado no modelo"""
        self.clear_canvas()
        
        # Obter cor e pulso da emoção atual
        emotion_data = self.emotions[self.current_emotion]
        color = emotion_data['color']
        pulse = emotion_data['pulse']
        
        # Tamanho com pulso suave
        size = self.base_size * (0.95 + 0.05 * pulse * math.sin(self.animation_time * 0.1))
        
        # CORPO PRINCIPAL - Formato oval como no modelo
        body_width = size * 1.2
        body_height = size * 1.0
        
        body_id = self.canvas.create_oval(
            self.x - body_width, self.y - body_height,
            self.x + body_width, self.y + body_height,
            fill=color,
            outline='#CC9900',
            width=3
        )
        self.all_elements.append(body_id)
        
        # BRAÇOS LATERAIS - Pequenos e redondos
        arm_size = size * 0.3
        arm_y = self.y - size * 0.2
        
        # Braço esquerdo
        left_arm_id = self.canvas.create_oval(
            self.x - body_width - arm_size, arm_y - arm_size * 0.8,
            self.x - body_width + arm_size, arm_y + arm_size * 0.8,
            fill=color,
            outline='#CC9900',
            width=2
        )
        self.all_elements.append(left_arm_id)
        
        # Braço direito
        right_arm_id = self.canvas.create_oval(
            self.x + body_width - arm_size, arm_y - arm_size * 0.8,
            self.x + body_width + arm_size, arm_y + arm_size * 0.8,
            fill=color,
            outline='#CC9900',
            width=2
        )
        self.all_elements.append(right_arm_id)
        
        # PERNAS INFERIORES - Pequenas e ovais
        leg_size = size * 0.25
        leg_y = self.y + body_height - leg_size
        
        # Perna esquerda
        left_leg_id = self.canvas.create_oval(
            self.x - body_width * 0.5 - leg_size, leg_y,
            self.x - body_width * 0.5 + leg_size, leg_y + leg_size * 1.5,
            fill=color,
            outline='#CC9900',
            width=2
        )
        self.all_elements.append(left_leg_id)
        
        # Perna direita
        right_leg_id = self.canvas.create_oval(
            self.x + body_width * 0.5 - leg_size, leg_y,
            self.x + body_width * 0.5 + leg_size, leg_y + leg_size * 1.5,
            fill=color,
            outline='#CC9900',
            width=2
        )
        self.all_elements.append(right_leg_id)
        
        # OLHOS - Grandes e expressivos
        eye_size = size * 0.15
        eye_y = self.y - size * 0.3
        
        # Olho esquerdo
        left_eye_bg_id = self.canvas.create_oval(
            self.x - size * 0.4 - eye_size, eye_y - eye_size,
            self.x - size * 0.4 + eye_size, eye_y + eye_size,
            fill='white',
            outline='#999999',
            width=2
        )
        self.all_elements.append(left_eye_bg_id)
        
        left_pupil_id = self.canvas.create_oval(
            self.x - size * 0.4 - eye_size * 0.4, eye_y - eye_size * 0.4,
            self.x - size * 0.4 + eye_size * 0.4, eye_y + eye_size * 0.4,
            fill='black'
        )
        self.all_elements.append(left_pupil_id)
        
        # Olho direito
        right_eye_bg_id = self.canvas.create_oval(
            self.x + size * 0.4 - eye_size, eye_y - eye_size,
            self.x + size * 0.4 + eye_size, eye_y + eye_size,
            fill='white',
            outline='#999999',
            width=2
        )
        self.all_elements.append(right_eye_bg_id)
        
        right_pupil_id = self.canvas.create_oval(
            self.x + size * 0.4 - eye_size * 0.4, eye_y - eye_size * 0.4,
            self.x + size * 0.4 + eye_size * 0.4, eye_y + eye_size * 0.4,
            fill='black'
        )
        self.all_elements.append(right_pupil_id)
        
        # BOCA - Baseada na emoção
        mouth_y = self.y + size * 0.1
        
        if self.current_emotion == 'happy':
            # Sorriso
            mouth_id = self.canvas.create_arc(
                self.x - size * 0.3, mouth_y - size * 0.1,
                self.x + size * 0.3, mouth_y + size * 0.2,
                start=200, extent=140,
                outline='black', width=3
            )
            self.all_elements.append(mouth_id)
        elif self.current_emotion == 'sad':
            # Boca triste
            mouth_id = self.canvas.create_arc(
                self.x - size * 0.3, mouth_y,
                self.x + size * 0.3, mouth_y + size * 0.3,
                start=20, extent=140,
                outline='black', width=3
            )
            self.all_elements.append(mouth_id)
        else:
            # Boca neutra - linha reta
            mouth_id = self.canvas.create_line(
                self.x - size * 0.15, mouth_y,
                self.x + size * 0.15, mouth_y,
                fill='black', width=3, capstyle=tk.ROUND
            )
            self.all_elements.append(mouth_id)
    
    def update_animation(self):
        """Atualiza animação suavemente"""
        self.animation_time += 1
        if self.animation_time % 2 == 0:  # Atualizar a cada 2 frames para suavidade
            self.draw()
    
    def start_animation(self):
        """Inicia loop de animação"""
        def animate():
            while True:
                self.update_animation()
                time.sleep(1/15)  # 15 FPS para suavidade
        
        threading.Thread(target=animate, daemon=True).start()

class VoiceSystemSimple:
    """Sistema de voz simplificado"""
    
    def __init__(self, blob: SimpleBLOB):
        self.blob = blob
        self.enabled = VOICE_AVAILABLE
        self.is_listening = False
        self.is_speaking = False
        
        if not self.enabled:
            return
        
        # Configurar reconhecimento
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Configurar TTS
        self.tts_engine = pyttsx3.init()
        self.setup_voice()
        
        # Respostas simples
        self.responses = {
            'feliz': "Que alegria! Estou feliz também!",
            'triste': "Não fique triste, estou aqui com você!",
            'animado': "Wow! Que energia boa!",
            'bravo': "Vamos respirar fundo juntos?",
            'pensando': "Deixe-me pensar...",
            'surpreso': "Nossa! Que surpresa!",
            'oi': "Oi! Como você está?",
            'olá': "Olá! É bom te ver!",
            'tchau': "Tchau! Até mais!",
            'default': "Interessante! Me conte mais!"
        }
        
        self.start_listening()
    
    def setup_voice(self):
        """Configura voz neutra"""
        try:
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Usar primeira voz disponível
                self.tts_engine.setProperty('voice', voices[0].id)
                self.tts_engine.setProperty('rate', 150)
                self.tts_engine.setProperty('volume', 0.8)
        except:
            pass
    
    def start_listening(self):
        """Inicia escuta automática"""
        if not self.enabled:
            return
            
        def listen_loop():
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Sistema de voz ativo - fale 'BLOB' + comando")
            except:
                return
            
            while True:
                if self.is_speaking:
                    time.sleep(0.1)
                    continue
                    
                try:
                    with self.microphone as source:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                    text = self.recognizer.recognize_google(audio, language="pt-BR")
                    text = text.lower()
                    
                    if 'blob' in text:
                        response = self.process_command(text)
                        if response:
                            self.speak(response)
                            
                except sr.WaitTimeoutError:
                    continue
                except:
                    continue
        
        threading.Thread(target=listen_loop, daemon=True).start()
    
    def process_command(self, text: str) -> str:
        """Processa comando de voz"""
        text = text.replace('blob', '').strip()
        
        # Verificar emoções
        for emotion in self.blob.emotions.keys():
            if emotion in text:
                self.blob.set_emotion(emotion)
                break
        
        # Encontrar resposta
        for key, response in self.responses.items():
            if key in text:
                return response
        
        return self.responses['default']
    
    def speak(self, text: str):
        """Fala texto"""
        if not self.enabled or self.is_speaking:
            return
        
        def speak_thread():
            self.is_speaking = True
            self.blob.set_emotion('speaking')
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                pass
            finally:
                self.is_speaking = False
                self.blob.set_emotion('neutral')
        
        threading.Thread(target=speak_thread, daemon=True).start()

class BLOBConsistente:
    """Aplicação principal do BLOB consistente"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BLOB Consistente - Assistente Virtual")
        self.root.geometry("900x700")
        self.root.configure(bg='#2C3E50')  # Fundo escuro como na imagem
        
        # Canvas principal
        self.canvas = tk.Canvas(
            self.root, 
            width=800, 
            height=600,
            bg='#34495E'  # Fundo do canvas
        )
        self.canvas.pack(pady=10)
        
        # Criar BLOB
        self.blob = SimpleBLOB(self.canvas)
        
        # Sistema de voz
        if VOICE_AVAILABLE:
            self.voice_system = VoiceSystemSimple(self.blob)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura interface simples"""
        # Frame de controles
        control_frame = tk.Frame(self.root, bg='#2C3E50')
        control_frame.pack(pady=10)
        
        # Botões de emoção
        emotions = ['neutral', 'happy', 'sad', 'excited', 'angry', 'thinking', 'surprised']
        for i, emotion in enumerate(emotions):
            btn = tk.Button(
                control_frame,
                text=emotion.title(),
                command=lambda e=emotion: self.blob.set_emotion(e),
                bg='#3498DB',
                fg='white',
                font=('Arial', 10),
                padx=10,
                relief=tk.FLAT
            )
            btn.grid(row=0, column=i, padx=5)
        
        # Status
        status_text = "Diga 'BLOB' + comando para interagir (ex: 'BLOB feliz')"
        status_label = tk.Label(
            self.root,
            text=status_text,
            bg='#2C3E50',
            fg='white',
            font=('Arial', 12),
            wraplength=800
        )
        status_label.pack(pady=10)
    
    def run(self):
        """Executa aplicação"""
        self.root.mainloop()

def main():
    """Função principal"""
    try:
        app = BLOBConsistente()
        app.run()
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()