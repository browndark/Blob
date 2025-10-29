# -*- coding: utf-8 -*-
"""
BLOB 3D SIMPLIFICADO - ASSISTENTE VIRTUAL AMIGÁVEL
Versão melhorada com detecção automática de voz e respostas naturais
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
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

class AmoebaBlob3D:
    """Classe principal do BLOB 3D com emoções e personalidade"""
    
    def __init__(self, canvas, x=400, y=300, size=80):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.base_size = size
        self.current_size = size
        
        # Sistema de emoções expandido
        self.emotions = {
            'neutral': {'color': '#FFD700', 'pulse': 1.0, 'speed': 0.02},
            'happy': {'color': '#FFD700', 'pulse': 1.2, 'speed': 0.05},
            'sad': {'color': '#FFB000', 'pulse': 0.8, 'speed': 0.01},
            'excited': {'color': '#FFF200', 'pulse': 1.4, 'speed': 0.08},
            'angry': {'color': '#FF8000', 'pulse': 1.1, 'speed': 0.06},
            'thinking': {'color': '#FFE55C', 'pulse': 0.9, 'speed': 0.015},
            'speaking': {'color': '#FFFF00', 'pulse': 1.3, 'speed': 0.04},
            'sleepy': {'color': '#FFCC66', 'pulse': 0.7, 'speed': 0.008},
            'surprised': {'color': '#FFFF99', 'pulse': 1.5, 'speed': 0.1},
            'loving': {'color': '#FFE4E1', 'pulse': 1.1, 'speed': 0.03}
        }
        
        self.current_emotion = 'neutral'
        self.is_speaking = False
        
        # Animação orgânica
        self.animation_time = 0
        self.deformation_points = self._generate_deformation_points()
        self.particle_system = []
        
        # Olhos
        self.left_eye_offset = Vector3(-20, -15, 0)
        self.right_eye_offset = Vector3(20, -15, 0)
        self.eye_blink_timer = 0
        self.is_blinking = False
        
        # Braços e pernas
        self.limbs = {
            'left_arm': {'angle': math.pi/4, 'length': 40},
            'right_arm': {'angle': -math.pi/4, 'length': 40},
            'left_leg': {'angle': math.pi/2 + 0.2, 'length': 35},
            'right_leg': {'angle': math.pi/2 - 0.2, 'length': 35}
        }
        
        # IDs dos elementos gráficos
        self.body_id = None
        self.left_eye_id = None
        self.right_eye_id = None
        self.limb_ids = {}
        
        self.start_animation()
    
    def _generate_deformation_points(self):
        """Gera pontos para deformação orgânica"""
        points = []
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            points.append({
                'angle': angle,
                'base_radius': 1.0,
                'deformation': random.uniform(0.8, 1.2),
                'speed': random.uniform(0.01, 0.03)
            })
        return points
    
    def set_emotion(self, emotion: str):
        """Define uma emoção para o BLOB"""
        if emotion in self.emotions:
            self.current_emotion = emotion
            # Adicionar partículas especiais para certas emoções
            if emotion == 'excited':
                self._add_excitement_particles()
            elif emotion == 'happy':
                self._add_happiness_particles()
    
    def _add_excitement_particles(self):
        """Adiciona partículas de excitação"""
        for _ in range(5):
            particle = {
                'x': self.x + random.uniform(-30, 30),
                'y': self.y + random.uniform(-30, 30),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-3, -1),
                'life': 30,
                'color': '#FFFF00'
            }
            self.particle_system.append(particle)
    
    def _add_happiness_particles(self):
        """Adiciona partículas de felicidade"""
        for _ in range(3):
            particle = {
                'x': self.x + random.uniform(-20, 20),
                'y': self.y - 20,
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-2, -0.5),
                'life': 25,
                'color': '#FFD700'
            }
            self.particle_system.append(particle)
    
    def update_animation(self):
        """Atualiza a animação do BLOB"""
        self.animation_time += self.emotions[self.current_emotion]['speed']
        
        # Atualizar deformações orgânicas
        for point in self.deformation_points:
            point['deformation'] = 1.0 + 0.2 * math.sin(
                self.animation_time * point['speed'] * 10 + point['angle']
            )
        
        # Pulso baseado na emoção
        pulse = self.emotions[self.current_emotion]['pulse']
        self.current_size = self.base_size * (1.0 + 0.1 * pulse * math.sin(self.animation_time))
        
        # Piscar aleatório
        self.eye_blink_timer += 1
        if self.eye_blink_timer > 120 and random.random() < 0.02:
            self.is_blinking = True
            self.eye_blink_timer = 0
        elif self.eye_blink_timer > 10:
            self.is_blinking = False
        
        # Atualizar partículas
        self._update_particles()
        
        # Movimento sutil dos braços
        self.limbs['left_arm']['angle'] = math.pi/4 + 0.2 * math.sin(self.animation_time * 0.5)
        self.limbs['right_arm']['angle'] = -math.pi/4 - 0.2 * math.sin(self.animation_time * 0.5)
        
        self.draw()
    
    def _update_particles(self):
        """Atualiza sistema de partículas"""
        for particle in self.particle_system[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particle_system.remove(particle)
    
    def draw(self):
        """Desenha o BLOB 3D na tela"""
        # Limpar elementos anteriores
        if self.body_id:
            self.canvas.delete(self.body_id)
        if self.left_eye_id:
            self.canvas.delete(self.left_eye_id)
        if self.right_eye_id:
            self.canvas.delete(self.right_eye_id)
        for limb_id in self.limb_ids.values():
            if limb_id:
                self.canvas.delete(limb_id)
        
        # Desenhar partículas
        for particle in self.particle_system:
            self.canvas.create_oval(
                particle['x']-2, particle['y']-2,
                particle['x']+2, particle['y']+2,
                fill=particle['color'], outline=""
            )
        
        # Corpo principal com deformação orgânica
        body_points = []
        for point in self.deformation_points:
            radius = self.current_size * point['deformation']
            x = self.x + radius * math.cos(point['angle'])
            y = self.y + radius * math.sin(point['angle'])
            body_points.extend([x, y])
        
        if len(body_points) >= 6:
            self.body_id = self.canvas.create_polygon(
                body_points,
                fill=self.emotions[self.current_emotion]['color'],
                outline='#DAA520',
                width=3,
                smooth=True
            )
        
        # Braços
        self._draw_limb('left_arm', self.x - 30, self.y)
        self._draw_limb('right_arm', self.x + 30, self.y)
        
        # Pernas
        self._draw_limb('left_leg', self.x - 15, self.y + 40)
        self._draw_limb('right_leg', self.x + 15, self.y + 40)
        
        # Olhos
        if not self.is_blinking:
            # Olho esquerdo
            left_eye_x = self.x + self.left_eye_offset.x
            left_eye_y = self.y + self.left_eye_offset.y
            self.left_eye_id = self.canvas.create_oval(
                left_eye_x-8, left_eye_y-8,
                left_eye_x+8, left_eye_y+8,
                fill='white', outline='black', width=2
            )
            self.canvas.create_oval(
                left_eye_x-3, left_eye_y-3,
                left_eye_x+3, left_eye_y+3,
                fill='black'
            )
            
            # Olho direito
            right_eye_x = self.x + self.right_eye_offset.x
            right_eye_y = self.y + self.right_eye_offset.y
            self.right_eye_id = self.canvas.create_oval(
                right_eye_x-8, right_eye_y-8,
                right_eye_x+8, right_eye_y+8,
                fill='white', outline='black', width=2
            )
            self.canvas.create_oval(
                right_eye_x-3, right_eye_y-3,
                right_eye_x+3, right_eye_y+3,
                fill='black'
            )
        else:
            # Olhos fechados (linhas)
            left_eye_x = self.x + self.left_eye_offset.x
            left_eye_y = self.y + self.left_eye_offset.y
            self.left_eye_id = self.canvas.create_line(
                left_eye_x-8, left_eye_y, left_eye_x+8, left_eye_y,
                fill='black', width=3
            )
            
            right_eye_x = self.x + self.right_eye_offset.x
            right_eye_y = self.y + self.right_eye_offset.y
            self.right_eye_id = self.canvas.create_line(
                right_eye_x-8, right_eye_y, right_eye_x+8, right_eye_y,
                fill='black', width=3
            )
    
    def _draw_limb(self, limb_name, start_x, start_y):
        """Desenha um braço ou perna"""
        limb = self.limbs[limb_name]
        end_x = start_x + limb['length'] * math.cos(limb['angle'])
        end_y = start_y + limb['length'] * math.sin(limb['angle'])
        
        self.limb_ids[limb_name] = self.canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill='#DAA520', width=8, capstyle=tk.ROUND
        )
        
        # Mão/pé
        self.canvas.create_oval(
            end_x-6, end_y-6, end_x+6, end_y+6,
            fill='#FFD700', outline='#DAA520', width=2
        )
    
    def start_animation(self):
        """Inicia o loop de animação"""
        def animate():
            while True:
                self.update_animation()
                time.sleep(1/30)  # 30 FPS
        
        threading.Thread(target=animate, daemon=True).start()

class VoiceSystem3D:
    """Sistema de voz 3D com reconhecimento automático"""
    
    def __init__(self, blob: AmoebaBlob3D):
        self.blob = blob
        self.enabled = VOICE_AVAILABLE
        self.is_listening = False
        self.is_speaking = False
        
        if not self.enabled:
            return
        
        # Configurar reconhecimento de voz
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Configurar Text-to-Speech
        self.tts_engine = pyttsx3.init()
        self.setup_neutral_voice()
        
        # Respostas em português natural
        self.responses = {
            'feliz': "Que bom te ver feliz! Isso me deixa animado também!",
            'triste': "Ah, você parece triste... Quer conversar sobre isso?",
            'animado': "Nossa, que energia boa! Estou super animado também!",
            'bravo': "Vejo que você está irritado. Vamos respirar fundo juntos?",
            'pensando': "Hmm, deixe-me pensar junto com você...",
            'surpreso': "Uau! Que surpresa incrível!",
            'dormindo': "Está com sono? Que tal uma soneca gostosa?",
            'amoroso': "Que carinho! Você é muito especial para mim!",
            
            # Cumprimentos
            'oi': "Oi! Como você está hoje?",
            'olá': "Olá! É muito bom te ver!",
            'tchau': "Tchau! Foi ótimo conversar com você!",
            'bom dia': "Bom dia! Espero que tenha um dia maravilhoso!",
            'boa tarde': "Boa tarde! Como está sendo seu dia?",
            'boa noite': "Boa noite! Descanse bem!",
            
            # Perguntas
            'como está': "Estou muito bem, obrigado! E você, como está?",
            'tudo bem': "Tudo ótimo comigo! E com você, está tudo bem?",
            'como vai': "Vai tudo muito bem! Como você está se sentindo?",
            
            # Padrão
            'default': "Interessante! Me conte mais sobre isso!"
        }
        
        # Iniciar escuta automática
        self.start_continuous_listening()
    
    def setup_neutral_voice(self):
        """Configura uma voz neutra e amigável"""
        try:
            voices = self.tts_engine.getProperty('voices')
            if voices:
                print("Vozes disponíveis no sistema:")
                for i, voice in enumerate(voices):
                    print(f"  {i}: {voice.name}")
                
                # Procurar por uma voz neutra
                neutral_voice = None
                for voice in voices:
                    voice_name = voice.name.lower()
                    # Buscar vozes que soem neutras
                    if any(keyword in voice_name for keyword in ['zira', 'david', 'mark', 'neutral']):
                        neutral_voice = voice
                        print(f"Voz neutra selecionada: {voice.name}")
                        break
                
                if not neutral_voice:
                    # Buscar voz masculina como segunda opção
                    for voice in voices:
                        if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                            neutral_voice = voice
                            print(f"Voz masculina neutra selecionada: {voice.name}")
                            break
                
                if neutral_voice:
                    self.tts_engine.setProperty('voice', neutral_voice.id)
                else:
                    print(f"Usando voz padrão: {voices[0].name}")
                    self.tts_engine.setProperty('voice', voices[0].id)
            else:
                print("Nenhuma voz encontrada no sistema")
                
        except Exception as e:
            print(f"Erro na configuração da voz: {e}")
    
    def start_continuous_listening(self):
        """Inicia escuta contínua e automática"""
        if not self.enabled:
            return
            
        print("Escuta automática ativada - fale naturalmente!")
        
        def continuous_listen():
            # Calibrar microfone
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Microfone calibrado!")
            except Exception as e:
                print(f"Erro na calibração: {e}")
                return
            
            self._continuous_listen_loop()
        
        threading.Thread(target=continuous_listen, daemon=True).start()
    
    def _continuous_listen_loop(self):
        """Loop contínuo de escuta"""
        while True:
            if not self.enabled or self.is_speaking:
                time.sleep(0.1)
                continue
                
            try:
                with self.microphone as source:
                    # Escutar com timeout menor para ser mais responsivo
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Processar em thread separada para não bloquear
                threading.Thread(
                    target=self._process_audio,
                    args=(audio,),
                    daemon=True
                ).start()
                    
            except sr.WaitTimeoutError:
                # Timeout é normal na escuta contínua
                continue
            except Exception as e:
                print(f"Erro na escuta: {e}")
                time.sleep(1)
    
    def _process_audio(self, audio):
        """Processa áudio capturado"""
        try:
            # Reconhecer texto
            text = self.recognizer.recognize_google(audio, language="pt-BR")
            text = text.lower().strip()
            
            print(f"Você disse: '{text}'")
            
            # Processar comando
            response = self.process_command(text)
            if response:
                self.speak(response)
                
        except sr.UnknownValueError:
            # Não conseguiu entender - normal, não fazer nada
            pass
        except sr.RequestError as e:
            print(f"Erro no serviço de reconhecimento: {e}")
        except Exception as e:
            print(f"Erro no processamento: {e}")
    
    def process_command(self, text: str) -> str:
        """Processa comando de voz e retorna resposta"""
        text = text.lower().strip()
        
        # Verificar se mencionou "blob" para ativação
        if 'blob' not in text:
            return None  # Ignorar se não mencionar "blob"
        
        # Remover "blob" do texto para processar o comando
        text = text.replace('blob', '').strip()
        
        # Procurar por emoções
        for emotion in self.blob.emotions.keys():
            if emotion in text:
                self.blob.set_emotion(emotion)
                if emotion in self.responses:
                    return self.responses[emotion]
        
        # Procurar por cumprimentos e comandos
        for key, response in self.responses.items():
            if key in text:
                return response
        
        # Resposta padrão
        return self.responses['default']
    
    def speak(self, text: str):
        """Fala texto de forma natural"""
        if not self.enabled or self.is_speaking:
            return
        
        # Processar texto para soar mais natural
        processed_text = self.process_text_for_natural_voice(text)
        
        self.is_speaking = True
        self.blob.is_speaking = True
        self.blob.set_emotion('speaking')
        
        def speak_thread():
            try:
                # Configurar parâmetros para voz mais natural
                original_rate = self.tts_engine.getProperty('rate')
                original_volume = self.tts_engine.getProperty('volume')
                
                # Ajustar para soar mais natural e amigável
                self.tts_engine.setProperty('rate', 140)     # Um pouco mais rápido
                self.tts_engine.setProperty('volume', 0.8)   # Volume normal
                
                # Falar de forma contínua, mais natural
                self.tts_engine.say(processed_text)
                self.tts_engine.runAndWait()
                
                # Restaurar configurações
                self.tts_engine.setProperty('rate', original_rate)
                self.tts_engine.setProperty('volume', original_volume)
                
            except Exception as e:
                print(f"Erro TTS: {e}")
            finally:
                self.is_speaking = False
                self.blob.is_speaking = False
                self.blob.set_emotion('neutral')
        
        threading.Thread(target=speak_thread, daemon=True).start()
    
    def process_text_for_natural_voice(self, text: str) -> str:
        """Processa texto para soar mais natural"""
        # Manter pontuação natural
        processed = text
        
        # Adicionar sons de amoeba ocasionalmente de forma mais natural
        import random
        if random.random() < 0.2:  # 20% de chance, menos frequente
            blob_sounds = ["*blob*", "*glub*"]
            processed = processed + " " + random.choice(blob_sounds)
        
        return processed

class BLOB3DSimplified:
    """Aplicação principal do BLOB 3D simplificado"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BLOB 3D - Assistente Virtual")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a2e')
        
        # Canvas principal
        self.canvas = tk.Canvas(
            self.root, 
            width=800, 
            height=600,
            bg='#16213e'
        )
        self.canvas.pack(pady=10)
        
        # Criar BLOB
        self.blob = AmoebaBlob3D(self.canvas)
        
        # Sistema de voz
        if VOICE_AVAILABLE:
            self.voice_system = VoiceSystem3D(self.blob)
            print("Pressione 'Iniciar Voz' para começar a conversar!")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame de controles
        control_frame = tk.Frame(self.root, bg='#1a1a2e')
        control_frame.pack(pady=10)
        
        # Botões de emoção
        emotions = ['neutral', 'happy', 'sad', 'excited', 'angry', 'thinking', 'surprised']
        for i, emotion in enumerate(emotions):
            btn = tk.Button(
                control_frame,
                text=emotion.title(),
                command=lambda e=emotion: self.blob.set_emotion(e),
                bg='#0f3460',
                fg='white',
                font=('Arial', 10),
                padx=10
            )
            btn.grid(row=0, column=i, padx=5)
        
        # Frame de voz
        voice_frame = tk.Frame(self.root, bg='#1a1a2e')
        voice_frame.pack(pady=10)
        
        # Botão de voz
        self.voice_button = tk.Button(
            voice_frame,
            text="Iniciar Voz",
            command=self.toggle_voice,
            bg='#e94560',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=5
        )
        self.voice_button.pack(side=tk.LEFT, padx=10)
        
        # Status da voz
        self.voice_status = tk.Label(
            voice_frame,
            text="Voz desligada" if not VOICE_AVAILABLE else "Pressione para ativar",
            bg='#1a1a2e',
            fg='white',
            font=('Arial', 10)
        )
        self.voice_status.pack(side=tk.LEFT, padx=10)
        
        # Instruções
        info_text = ("Comandos de voz: 'feliz', 'triste', 'animado', 'bravo', 'pensando', "
                    "'surpreso', 'oi', 'tchau', 'como está' + mencione 'BLOB'")
        info_label = tk.Label(
            self.root,
            text=info_text,
            bg='#1a1a2e',
            fg='#cccccc',
            font=('Arial', 9),
            wraplength=800,
            justify=tk.CENTER
        )
        info_label.pack(pady=5)
    
    def toggle_voice(self):
        """Alterna sistema de voz"""
        if not VOICE_AVAILABLE:
            return
        
        if hasattr(self.voice_system, 'is_listening') and self.voice_system.is_listening:
            # Parar escuta
            self.voice_system.is_listening = False
            self.voice_button.config(text="Iniciar Voz")
            self.voice_status.config(text="Voz desligada")
        else:
            # Iniciar escuta
            self.voice_system.is_listening = True
            self.voice_status.config(text="Escutando... Fale comigo!")
            self.voice_button.config(text="Parar Voz")
    
    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()

def main():
    """Função principal"""
    try:
        app = BLOB3DSimplified()
        app.run()
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()