# -*- coding: utf-8 -*-
"""
BLOB SUPER SIMPLES E CONSISTENTE
Baseado na imagem mostrada - design limpo e estável
"""

import tkinter as tk
import math
import time
import threading
import sys

try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("Sistema de voz nao disponivel")

class BLOBSimples:
    """BLOB super simples e consistente"""
    
    def __init__(self, canvas, x=450, y=300):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = 80
        
        # Cores por emoção - simples e consistentes
        self.colors = {
            'neutral': '#FFE066',
            'happy': '#FFE066', 
            'sad': '#E6CC00',
            'excited': '#FFF59D',
            'angry': '#FFB300',
            'thinking': '#FFD700',
            'speaking': '#FFF176',
            'surprised': '#FFEB3B'
        }
        
        self.current_emotion = 'neutral'
        self.animation_time = 0
        self.elements = []  # Lista para controlar elementos
        
        self.start_animation()
    
    def set_emotion(self, emotion):
        if emotion in self.colors:
            self.current_emotion = emotion
    
    def clear_all(self):
        """Remove todos os elementos do canvas"""
        for element in self.elements:
            try:
                self.canvas.delete(element)
            except:
                pass
        self.elements.clear()
    
    def draw(self):
        """Desenha o BLOB de forma super simples"""
        self.clear_all()
        
        color = self.colors[self.current_emotion]
        
        # Pulso suave
        pulse = 1 + 0.05 * math.sin(self.animation_time * 0.1)
        size = self.size * pulse
        
        # SOMBRA - simples e fixa
        shadow = self.canvas.create_oval(
            self.x - size * 1.2, self.y + size * 1.3,
            self.x + size * 1.2, self.y + size * 1.8,
            fill='#2C3E50', outline='', stipple='gray50'
        )
        self.elements.append(shadow)
        
        # CORPO PRINCIPAL - oval simples
        body = self.canvas.create_oval(
            self.x - size, self.y - size * 0.8,
            self.x + size, self.y + size * 0.8,
            fill=color, outline='#DAA520', width=2
        )
        self.elements.append(body)
        
        # ROSTO - círculo amarelo mais escuro
        face = self.canvas.create_oval(
            self.x - size * 0.7, self.y - size * 0.5,
            self.x + size * 0.7, self.y + size * 0.3,
            fill='#FFD700', outline='#DAA520', width=2
        )
        self.elements.append(face)
        
        # BRAÇOS - círculos pequenos nas laterais
        # Braço esquerdo
        left_arm = self.canvas.create_oval(
            self.x - size * 1.4, self.y - size * 0.3,
            self.x - size * 0.9, self.y + size * 0.2,
            fill=color, outline='#DAA520', width=2
        )
        self.elements.append(left_arm)
        
        # Braço direito
        right_arm = self.canvas.create_oval(
            self.x + size * 0.9, self.y - size * 0.3,
            self.x + size * 1.4, self.y + size * 0.2,
            fill=color, outline='#DAA520', width=2
        )
        self.elements.append(right_arm)
        
        # PERNAS - círculos pequenos embaixo
        # Perna esquerda
        left_leg = self.canvas.create_oval(
            self.x - size * 0.5, self.y + size * 0.6,
            self.x - size * 0.1, self.y + size * 1.1,
            fill=color, outline='#DAA520', width=2
        )
        self.elements.append(left_leg)
        
        # Perna direita
        right_leg = self.canvas.create_oval(
            self.x + size * 0.1, self.y + size * 0.6,
            self.x + size * 0.5, self.y + size * 1.1,
            fill=color, outline='#DAA520', width=2
        )
        self.elements.append(right_leg)
        
        # OLHOS - simples e consistentes
        # Olho esquerdo
        left_eye_bg = self.canvas.create_oval(
            self.x - size * 0.4, self.y - size * 0.3,
            self.x - size * 0.15, self.y - size * 0.05,
            fill='white', outline='#999', width=1
        )
        self.elements.append(left_eye_bg)
        
        left_pupil = self.canvas.create_oval(
            self.x - size * 0.32, self.y - size * 0.22,
            self.x - size * 0.23, self.y - size * 0.13,
            fill='black'
        )
        self.elements.append(left_pupil)
        
        # Olho direito
        right_eye_bg = self.canvas.create_oval(
            self.x + size * 0.15, self.y - size * 0.3,
            self.x + size * 0.4, self.y - size * 0.05,
            fill='white', outline='#999', width=1
        )
        self.elements.append(right_eye_bg)
        
        right_pupil = self.canvas.create_oval(
            self.x + size * 0.23, self.y - size * 0.22,
            self.x + size * 0.32, self.y - size * 0.13,
            fill='black'
        )
        self.elements.append(right_pupil)
        
        # BOCA - linha simples
        mouth_y = self.y + size * 0.05
        
        if self.current_emotion == 'happy':
            # Sorriso simples
            mouth = self.canvas.create_arc(
                self.x - size * 0.25, mouth_y - size * 0.1,
                self.x + size * 0.25, mouth_y + size * 0.2,
                start=200, extent=140,
                outline='black', width=2, style='arc'
            )
        elif self.current_emotion == 'sad':
            # Boca triste
            mouth = self.canvas.create_arc(
                self.x - size * 0.2, mouth_y,
                self.x + size * 0.2, mouth_y + size * 0.3,
                start=20, extent=140,
                outline='black', width=2, style='arc'
            )
        else:
            # Linha reta
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

class VozSimples:
    """Sistema de voz super simples"""
    
    def __init__(self, blob):
        self.blob = blob
        self.enabled = VOICE_AVAILABLE
        self.is_speaking = False
        
        if not self.enabled:
            return
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Configurar voz
        try:
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
                self.tts_engine.setProperty('rate', 150)
        except:
            pass
        
        # Respostas simples
        self.responses = {
            'feliz': "Estou feliz!",
            'triste': "Que pena...",
            'animado': "Que legal!",
            'bravo': "Hmm...",
            'oi': "Oi!",
            'tchau': "Tchau!",
            'default': "Entendi!"
        }
        
        self.start_listening()
    
    def start_listening(self):
        """Escuta simples"""
        if not self.enabled:
            return
        
        def listen():
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("BLOB ativo - diga 'BLOB' + comando")
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
                        self.process_command(text)
                
                except:
                    continue
        
        threading.Thread(target=listen, daemon=True).start()
    
    def process_command(self, text):
        """Processa comando simples"""
        text = text.replace('blob', '').strip()
        
        # Verificar emoções
        if 'feliz' in text or 'happy' in text:
            self.blob.set_emotion('happy')
            self.speak("Estou feliz!")
        elif 'triste' in text or 'sad' in text:
            self.blob.set_emotion('sad')
            self.speak("Que pena...")
        elif 'animado' in text or 'excited' in text:
            self.blob.set_emotion('excited')
            self.speak("Que legal!")
        elif 'bravo' in text or 'angry' in text:
            self.blob.set_emotion('angry')
            self.speak("Hmm...")
        elif 'oi' in text or 'olá' in text:
            self.speak("Oi!")
        elif 'tchau' in text:
            self.speak("Tchau!")
        else:
            self.speak("Entendi!")
    
    def speak(self, text):
        """Fala simples"""
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

class AppSimples:
    """App super simples"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BLOB Simples e Consistente")
        self.root.geometry("900x600")
        self.root.configure(bg='#B0E0E6')  # Azul claro como na imagem
        
        # Canvas simples
        self.canvas = tk.Canvas(
            self.root,
            width=900,
            height=500,
            bg='#B0E0E6'
        )
        self.canvas.pack(pady=20)
        
        # Grid simples
        self.draw_grid()
        
        # BLOB
        self.blob = BLOBSimples(self.canvas)
        
        # Voz
        if VOICE_AVAILABLE:
            self.voice = VozSimples(self.blob)
        
        # Interface
        self.setup_ui()
    
    def draw_grid(self):
        """Grid simples"""
        for i in range(0, 900, 50):
            self.canvas.create_line(i, 0, i, 500, fill='#A0D0E0', width=1)
        for i in range(0, 500, 50):
            self.canvas.create_line(0, i, 900, i, fill='#A0D0E0', width=1)
    
    def setup_ui(self):
        """Interface simples"""
        frame = tk.Frame(self.root, bg='#B0E0E6')
        frame.pack(pady=10)
        
        tk.Label(frame, text="BLOB CONSISTENTE", 
                font=('Arial', 14, 'bold'), bg='#B0E0E6').pack(pady=5)
        
        button_frame = tk.Frame(frame, bg='#B0E0E6')
        button_frame.pack()
        
        emotions = ['neutral', 'happy', 'sad', 'excited', 'angry', 'thinking']
        for i, emotion in enumerate(emotions):
            btn = tk.Button(
                button_frame,
                text=emotion.title(),
                command=lambda e=emotion: self.blob.set_emotion(e),
                bg='#4A90E2', fg='white',
                font=('Arial', 10), padx=10, pady=2
            )
            btn.grid(row=0, column=i, padx=5)
        
        tk.Label(frame, text="Diga 'BLOB' + comando para interagir",
                font=('Arial', 10), bg='#B0E0E6').pack(pady=5)
    
    def run(self):
        self.root.mainloop()

def main():
    try:
        app = AppSimples()
        app.run()
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()