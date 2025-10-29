#!/usr/bin/env python3
"""
🌟 BLOB 3D Advanced - Amoeba Amarela Interativa
Versão robusta com 3D real, animações fluidas e interações avançadas
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import time
import threading
import random
from dataclasses import dataclass
from typing import List, Tuple
import json

# Imports do sistema de voz
try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("⚠️ Sistema de voz não disponível. Instale: pip install SpeechRecognition pyttsx3")

@dataclass
class Vector3:
    """Classe para vetores 3D"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def normalize(self):
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if length > 0:
            return Vector3(self.x/length, self.y/length, self.z/length)
        return Vector3()

class BlobBodyPart:
    """Parte do corpo da amoeba (braço, perna, etc.)"""
    def __init__(self, name: str, position: Vector3, size: float = 1.0):
        self.name = name
        self.position = position
        self.size = size
        self.rotation = Vector3()
        self.animation_offset = random.uniform(0, 2 * math.pi)
        self.color = [1.0, 1.0, 0.3, 1.0]  # Amarelo
        
    def update_animation(self, time_delta: float, emotion: str):
        """Atualiza animação da parte do corpo"""
        base_time = time.time() + self.animation_offset
        
        if emotion == "excited":
            # Movimento mais enérgico
            self.rotation.y = math.sin(base_time * 3) * 15
            self.position.y += math.sin(base_time * 4) * 0.1
        elif emotion == "sad":
            # Movimento mais lento e para baixo
            self.rotation.y = math.sin(base_time * 0.5) * 5
            self.position.y -= 0.2
        elif emotion == "thinking":
            # Movimento sutil e contemplativo
            self.rotation.x = math.sin(base_time * 1.5) * 8
        else:
            # Movimento neutro (respiração)
            self.rotation.y = math.sin(base_time * 1.2) * 10
            self.position.y += math.sin(base_time * 0.8) * 0.05

class AmoebaBlob:
    """Amoeba BLOB 3D com braços e pernas"""
    
    def __init__(self):
        self.position = Vector3(0, 0, 0)
        self.scale = 1.0
        self.emotion = "neutral"
        self.is_speaking = False
        self.energy_level = 0.5
        
        # Cores dinâmicas
        self.base_color = [1.0, 1.0, 0.2, 1.0]  # Amarelo brilhante
        self.current_color = self.base_color.copy()
        
        # Criar partes do corpo
        self.body_parts = {
            'head': BlobBodyPart('head', Vector3(0, 1.5, 0), 1.2),
            'body': BlobBodyPart('body', Vector3(0, 0, 0), 1.5),
            'left_arm': BlobBodyPart('left_arm', Vector3(-1.2, 0.5, 0), 0.6),
            'right_arm': BlobBodyPart('right_arm', Vector3(1.2, 0.5, 0), 0.6),
            'left_leg': BlobBodyPart('left_leg', Vector3(-0.5, -1.5, 0), 0.7),
            'right_leg': BlobBodyPart('right_leg', Vector3(0.5, -1.5, 0), 0.7),
        }
        
        # Parâmetros de deformação (amoeba)
        self.deformation_strength = 0.3
        self.deformation_speed = 2.0
        
        # Sistema de partículas para efeitos
        self.particles = []
        
    def set_emotion(self, emotion: str):
        """Define emoção da amoeba"""
        self.emotion = emotion
        
        # Cores baseadas na emoção
        color_map = {
            "happy": [1.0, 1.0, 0.0, 1.0],      # Amarelo puro
            "excited": [1.0, 0.8, 0.0, 1.0],    # Laranja-amarelo
            "sad": [0.8, 0.8, 0.4, 1.0],        # Amarelo opaco
            "angry": [1.0, 0.5, 0.0, 1.0],      # Laranja
            "thinking": [0.9, 1.0, 0.6, 1.0],   # Amarelo-verde
            "speaking": [1.0, 1.0, 0.4, 1.0],   # Amarelo claro
            "neutral": [1.0, 1.0, 0.2, 1.0]     # Amarelo padrão
        }
        
        target_color = color_map.get(emotion, self.base_color)
        self.current_color = target_color
        
        # Efeitos especiais por emoção
        if emotion == "excited":
            self.create_sparkle_particles()
        elif emotion == "happy":
            self.create_glow_effect()
    
    def create_sparkle_particles(self):
        """Cria partículas de brilho"""
        for _ in range(20):
            particle = {
                'position': Vector3(
                    random.uniform(-2, 2),
                    random.uniform(-1, 3),
                    random.uniform(-2, 2)
                ),
                'velocity': Vector3(
                    random.uniform(-0.1, 0.1),
                    random.uniform(0.05, 0.15),
                    random.uniform(-0.1, 0.1)
                ),
                'life': 2.0,
                'color': [1.0, 1.0, 0.8, 1.0]
            }
            self.particles.append(particle)
    
    def create_glow_effect(self):
        """Cria efeito de brilho"""
        # Implementação do efeito de brilho será adicionada
        pass
    
    def update(self, time_delta: float):
        """Atualiza animação da amoeba"""
        current_time = time.time()
        
        # Atualizar partes do corpo
        for part in self.body_parts.values():
            part.update_animation(time_delta, self.emotion)
        
        # Deformação orgânica da amoeba
        if self.emotion == "speaking":
            self.deformation_strength = 0.5
            self.deformation_speed = 4.0
        else:
            self.deformation_strength = 0.3
            self.deformation_speed = 2.0
        
        # Atualizar partículas
        self.update_particles(time_delta)
        
        # Movimento de respiração geral
        breath_factor = math.sin(current_time * 0.8) * 0.05
        self.scale = 1.0 + breath_factor
    
    def update_particles(self, time_delta: float):
        """Atualiza sistema de partículas"""
        for particle in self.particles[:]:
            particle['position'] = particle['position'] + (particle['velocity'] * time_delta)
            particle['life'] -= time_delta
            particle['color'][3] = max(0, particle['life'] / 2.0)  # Fade out
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_sphere_deformed(self, radius: float, deformation: float = 0.3):
        """Desenha esfera deformada (efeito amoeba)"""
        glBegin(GL_TRIANGLES)
        
        for lat in range(20):
            for lon in range(40):
                # Calcular coordenadas da esfera com deformação
                lat1 = math.pi * (-0.5 + lat / 20.0)
                lat2 = math.pi * (-0.5 + (lat + 1) / 20.0)
                lon1 = 2 * math.pi * (lon / 40.0)
                lon2 = 2 * math.pi * ((lon + 1) / 40.0)
                
                # Vértices com deformação orgânica
                vertices = []
                for lt, ln in [(lat1, lon1), (lat1, lon2), (lat2, lon2), (lat2, lon1)]:
                    x = math.cos(lt) * math.cos(ln)
                    y = math.sin(lt)
                    z = math.cos(lt) * math.sin(ln)
                    
                    # Aplicar deformação senoidal para efeito amoeba
                    deform = 1.0 + deformation * math.sin(time.time() * self.deformation_speed + x * 3 + y * 2 + z * 4)
                    
                    vertices.append([x * radius * deform, y * radius * deform, z * radius * deform])
                
                # Desenhar triângulos
                for i in range(2):
                    base = i * 2
                    for j in range(3):
                        idx = [base, base + 1, base + 2] if j < 2 else [base, base + 2, (base + 3) % 4]
                        v = vertices[idx[j]]
                        
                        # Normal para iluminação
                        normal = np.array(v) / np.linalg.norm(v)
                        glNormal3fv(normal)
                        glVertex3fv(v)
        
        glEnd()
    
    def draw_limb(self, start_pos: Vector3, end_pos: Vector3, thickness: float = 0.3):
        """Desenha membro (braço ou perna) como cilindro orgânico"""
        direction = Vector3(
            end_pos.x - start_pos.x,
            end_pos.y - start_pos.y,
            end_pos.z - start_pos.z
        ).normalize()
        
        # Desenhar cilindro orgânico
        segments = 12
        length_segments = 8
        
        glBegin(GL_TRIANGLES)
        
        for i in range(length_segments):
            t1 = i / length_segments
            t2 = (i + 1) / length_segments
            
            # Posições ao longo do membro
            pos1 = Vector3(
                start_pos.x + direction.x * t1,
                start_pos.y + direction.y * t1,
                start_pos.z + direction.z * t1
            )
            pos2 = Vector3(
                start_pos.x + direction.x * t2,
                start_pos.y + direction.y * t2,
                start_pos.z + direction.z * t2
            )
            
            # Variar espessura para efeito orgânico
            thick1 = thickness * (0.8 + 0.2 * math.sin(t1 * math.pi))
            thick2 = thickness * (0.8 + 0.2 * math.sin(t2 * math.pi))
            
            for j in range(segments):
                angle1 = 2 * math.pi * j / segments
                angle2 = 2 * math.pi * (j + 1) / segments
                
                # Vértices do cilindro
                x1, z1 = thick1 * math.cos(angle1), thick1 * math.sin(angle1)
                x2, z2 = thick1 * math.cos(angle2), thick1 * math.sin(angle2)
                x3, z3 = thick2 * math.cos(angle1), thick2 * math.sin(angle1)
                x4, z4 = thick2 * math.cos(angle2), thick2 * math.sin(angle2)
                
                # Triângulos do segmento
                vertices = [
                    [pos1.x + x1, pos1.y, pos1.z + z1],
                    [pos1.x + x2, pos1.y, pos1.z + z2],
                    [pos2.x + x3, pos2.y, pos2.z + z3],
                    [pos2.x + x4, pos2.y, pos2.z + z4]
                ]
                
                # Primeiro triângulo
                for idx in [0, 1, 2]:
                    glVertex3fv(vertices[idx])
                
                # Segundo triângulo
                for idx in [1, 3, 2]:
                    glVertex3fv(vertices[idx])
        
        glEnd()
    
    def render(self):
        """Renderiza a amoeba BLOB 3D"""
        glPushMatrix()
        
        # Aplicar transformações globais
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glScalef(self.scale, self.scale, self.scale)
        
        # Configurar material
        glColor4fv(self.current_color)
        
        # Corpo principal (amoeba)
        glPushMatrix()
        body_part = self.body_parts['body']
        glTranslatef(body_part.position.x, body_part.position.y, body_part.position.z)
        glRotatef(body_part.rotation.x, 1, 0, 0)
        glRotatef(body_part.rotation.y, 0, 1, 0)
        glRotatef(body_part.rotation.z, 0, 0, 1)
        self.draw_sphere_deformed(body_part.size, self.deformation_strength)
        glPopMatrix()
        
        # Cabeça
        glPushMatrix()
        head_part = self.body_parts['head']
        glTranslatef(head_part.position.x, head_part.position.y, head_part.position.z)
        glRotatef(head_part.rotation.x, 1, 0, 0)
        glRotatef(head_part.rotation.y, 0, 1, 0)
        
        # Cabeça um pouco menor e mais deformada quando falando
        head_deform = self.deformation_strength * 1.5 if self.is_speaking else self.deformation_strength
        self.draw_sphere_deformed(head_part.size, head_deform)
        
        # Olhos simples
        glColor3f(0, 0, 0)  # Preto
        glPushMatrix()
        glTranslatef(-0.3, 0.3, 0.8)
        gluSphere(gluNewQuadric(), 0.15, 10, 10)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.3, 0.3, 0.8)
        gluSphere(gluNewQuadric(), 0.15, 10, 10)
        glPopMatrix()
        
        # Boca (varia com emoção)
        glColor3f(0.2, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(0, -0.2, 0.9)
        if self.emotion == "happy":
            # Sorriso
            glRotatef(180, 1, 0, 0)
            gluPartialDisk(gluNewQuadric(), 0, 0.3, 10, 5, 0, 180)
        elif self.emotion == "sad":
            # Carranca
            gluPartialDisk(gluNewQuadric(), 0, 0.3, 10, 5, 0, 180)
        elif self.is_speaking:
            # Boca aberta
            gluSphere(gluNewQuadric(), 0.2, 8, 8)
        else:
            # Neutro
            gluDisk(gluNewQuadric(), 0, 0.15, 8, 1)
        glPopMatrix()
        
        glPopMatrix()
        
        # Restaurar cor do corpo
        glColor4fv(self.current_color)
        
        # Braços
        for arm_name in ['left_arm', 'right_arm']:
            arm = self.body_parts[arm_name]
            glPushMatrix()
            glTranslatef(arm.position.x, arm.position.y, arm.position.z)
            glRotatef(arm.rotation.x, 1, 0, 0)
            glRotatef(arm.rotation.y, 0, 1, 0)
            glRotatef(arm.rotation.z, 0, 0, 1)
            self.draw_sphere_deformed(arm.size * 0.8, self.deformation_strength * 0.5)
            
            # Desenhar "mão" como uma esfera menor
            glPushMatrix()
            hand_offset = 0.8 if 'left' in arm_name else -0.8
            glTranslatef(hand_offset, -0.5, 0)
            self.draw_sphere_deformed(arm.size * 0.4, self.deformation_strength * 0.3)
            glPopMatrix()
            
            glPopMatrix()
        
        # Pernas
        for leg_name in ['left_leg', 'right_leg']:
            leg = self.body_parts[leg_name]
            glPushMatrix()
            glTranslatef(leg.position.x, leg.position.y, leg.position.z)
            glRotatef(leg.rotation.x, 1, 0, 0)
            glRotatef(leg.rotation.y, 0, 1, 0)
            glRotatef(leg.rotation.z, 0, 0, 1)
            self.draw_sphere_deformed(leg.size, self.deformation_strength * 0.7)
            
            # Desenhar "pé" como uma esfera menor
            glPushMatrix()
            glTranslatef(0, -0.8, 0.3)
            self.draw_sphere_deformed(leg.size * 0.5, self.deformation_strength * 0.3)
            glPopMatrix()
            
            glPopMatrix()
        
        # Renderizar partículas
        self.render_particles()
        
        glPopMatrix()
    
    def render_particles(self):
        """Renderiza sistema de partículas"""
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        for particle in self.particles:
            glPushMatrix()
            glTranslatef(particle['position'].x, particle['position'].y, particle['position'].z)
            glColor4fv(particle['color'])
            gluSphere(gluNewQuadric(), 0.05, 6, 6)
            glPopMatrix()
        
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)

class AdvancedVoiceSystem:
    """Sistema de voz avançado com IA"""
    
    def __init__(self, blob_ref):
        self.blob = blob_ref
        self.enabled = VOICE_AVAILABLE
        self.is_listening = False
        self.is_speaking = False
        
        if self.enabled:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.tts_engine = pyttsx3.init()
            
            # Configurar TTS
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Tentar encontrar voz feminina para a amoeba
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            self.tts_engine.setProperty('rate', 160)
            self.tts_engine.setProperty('volume', 0.9)
            
            # Comandos especiais
            self.commands = {
                'feliz': 'happy',
                'triste': 'sad',
                'animado': 'excited',
                'pensando': 'thinking',
                'neutro': 'neutral',
                'dança': 'dance',
                'acena': 'wave',
                'pula': 'jump'
            }
            
            print("✅ Sistema de voz avançado inicializado!")
    
    def start_listening(self):
        """Inicia escuta de voz em thread separada"""
        if not self.enabled or self.is_listening:
            return
        
        self.is_listening = True
        threading.Thread(target=self._listen_loop, daemon=True).start()
    
    def stop_listening(self):
        """Para escuta de voz"""
        self.is_listening = False
    
    def _listen_loop(self):
        """Loop de escuta de voz"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Timeout mais curto para responsividade
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Reconhecer em thread separada para não bloquear
                threading.Thread(
                    target=self._process_audio, 
                    args=(audio,), 
                    daemon=True
                ).start()
                
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print(f"Erro na escuta: {e}")
                time.sleep(0.5)
    
    def _process_audio(self, audio):
        """Processa áudio reconhecido"""
        try:
            text = self.recognizer.recognize_google(audio, language='pt-BR')
            print(f"🎤 Reconhecido: {text}")
            self._handle_voice_command(text.lower())
            
        except sr.UnknownValueError:
            print("🤔 Não consegui entender...")
        except sr.RequestError as e:
            print(f"❌ Erro no serviço de reconhecimento: {e}")
    
    def _handle_voice_command(self, text: str):
        """Processa comando de voz"""
        # Verificar comandos especiais
        for command, emotion in self.commands.items():
            if command in text:
                if emotion in ['dance', 'wave', 'jump']:
                    self._perform_action(emotion)
                else:
                    self.blob.set_emotion(emotion)
                    self.speak(f"Agora estou {command}!")
                return
        
        # Respostas contextuais
        if 'nome' in text:
            self.speak("Eu sou BLOB, sua amoeba amarela amiga!")
        elif 'como' in text and ('você' in text or 'está' in text):
            self.speak("Estou ótimo! Sou uma amoeba feliz e gelatinosa!")
        elif 'cor' in text:
            self.speak("Sou amarelo brilhante! Posso mudar um pouco dependendo do meu humor.")
        elif 'idade' in text:
            self.speak("Sou uma amoeba imortal! Não tenho idade específica.")
        elif 'dançar' in text or 'dança' in text:
            self._perform_action('dance')
        elif 'pular' in text or 'pula' in text:
            self._perform_action('jump')
        elif 'tchau' in text or 'adeus' in text:
            self.speak("Tchau! Foi ótimo conversar com você!")
        else:
            # Resposta genérica inteligente
            responses = [
                "Interessante! Conte-me mais sobre isso.",
                "Que legal! Sou uma amoeba curiosa.",
                "Hmm, isso é fascinante para uma amoeba como eu!",
                "Adorei ouvir isso! Sou toda gelatinosa de alegria!",
                "Como uma amoeba, eu acho isso incrível!"
            ]
            self.speak(random.choice(responses))
    
    def _perform_action(self, action: str):
        """Executa ação especial"""
        if action == 'dance':
            self.blob.set_emotion('excited')
            self.speak("Vou dançar para você!")
            # Trigger animação de dança
            for _ in range(3):
                self.blob.energy_level = 1.0
                time.sleep(0.5)
        elif action == 'jump':
            self.speak("Olha só como eu pulo!")
            # Animação de pulo
            self.blob.position.y += 2
            threading.Timer(1.0, lambda: setattr(self.blob.position, 'y', 0)).start()
        elif action == 'wave':
            self.speak("Oi! Estou acenando para você!")
            self.blob.set_emotion('happy')
    
    def speak(self, text: str):
        """Fala texto com animações"""
        if not self.enabled or self.is_speaking:
            return
        
        self.is_speaking = True
        self.blob.is_speaking = True
        self.blob.set_emotion('speaking')
        
        def speak_thread():
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"Erro TTS: {e}")
            finally:
                self.is_speaking = False
                self.blob.is_speaking = False
                self.blob.set_emotion('neutral')
        
        threading.Thread(target=speak_thread, daemon=True).start()

class Camera3D:
    """Sistema de câmera 3D avançado"""
    
    def __init__(self):
        self.distance = 8.0
        self.angle_x = 20.0
        self.angle_y = 0.0
        self.target = Vector3(0, 0, 0)
        self.min_distance = 3.0
        self.max_distance = 20.0
        
    def update(self, mouse_dx: float = 0, mouse_dy: float = 0, scroll: float = 0):
        """Atualiza câmera com controles de mouse"""
        # Rotação com mouse
        self.angle_y += mouse_dx * 0.5
        self.angle_x += mouse_dy * 0.5
        
        # Limitar ângulo vertical
        self.angle_x = max(-80, min(80, self.angle_x))
        
        # Zoom com scroll
        self.distance -= scroll * 0.5
        self.distance = max(self.min_distance, min(self.max_distance, self.distance))
    
    def apply(self):
        """Aplica transformações da câmera"""
        glLoadIdentity()
        gluLookAt(
            self.distance * math.cos(math.radians(self.angle_x)) * math.cos(math.radians(self.angle_y)),
            self.distance * math.sin(math.radians(self.angle_x)),
            self.distance * math.cos(math.radians(self.angle_x)) * math.sin(math.radians(self.angle_y)),
            self.target.x, self.target.y, self.target.z,
            0, 1, 0
        )

class BLOB3DAdvanced:
    """Aplicação principal do BLOB 3D Avançado"""
    
    def __init__(self):
        self.width = 1200
        self.height = 800
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Componentes principais
        self.blob = AmoebaBlob()
        self.camera = Camera3D()
        self.voice_system = AdvancedVoiceSystem(self.blob)
        
        # Controles
        self.mouse_pressed = False
        self.last_mouse_pos = (0, 0)
        
        # Interface
        self.show_help = True
        self.help_timer = 10.0  # Mostrar ajuda por 10 segundos
        
    def init_opengl(self):
        """Inicializa OpenGL"""
        pygame.init()
        pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("🌟 BLOB 3D Advanced - Amoeba Amarela Interativa")
        
        # Configurações OpenGL
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Configurar iluminação
        glLightfv(GL_LIGHT0, GL_POSITION, [5, 5, 5, 1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
        
        # Configurar perspectiva
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.width / self.height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
        # Fundo gradiente
        glClearColor(0.1, 0.15, 0.3, 1.0)
    
    def handle_events(self):
        """Processa eventos"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Toggle sistema de voz
                    if self.voice_system.is_listening:
                        self.voice_system.stop_listening()
                        print("🔇 Sistema de voz desligado")
                    else:
                        self.voice_system.start_listening()
                        print("🎤 Sistema de voz ligado - fale comigo!")
                elif event.key == pygame.K_1:
                    self.blob.set_emotion('happy')
                elif event.key == pygame.K_2:
                    self.blob.set_emotion('sad')
                elif event.key == pygame.K_3:
                    self.blob.set_emotion('excited')
                elif event.key == pygame.K_4:
                    self.blob.set_emotion('thinking')
                elif event.key == pygame.K_5:
                    self.blob.set_emotion('neutral')
                elif event.key == pygame.K_h:
                    self.show_help = not self.show_help
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo
                    self.mouse_pressed = True
                    self.last_mouse_pos = pygame.mouse.get_pos()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_pressed = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_pressed:
                    mouse_pos = pygame.mouse.get_pos()
                    dx = mouse_pos[0] - self.last_mouse_pos[0]
                    dy = mouse_pos[1] - self.last_mouse_pos[1]
                    self.camera.update(dx, dy)
                    self.last_mouse_pos = mouse_pos
            
            elif event.type == pygame.MOUSEWHEEL:
                self.camera.update(scroll=event.y)
    
    def draw_environment(self):
        """Desenha ambiente 3D"""
        # Chão
        glDisable(GL_LIGHTING)
        glColor3f(0.2, 0.3, 0.2)
        glBegin(GL_QUADS)
        size = 10
        glVertex3f(-size, -3, -size)
        glVertex3f(size, -3, -size)
        glVertex3f(size, -3, size)
        glVertex3f(-size, -3, size)
        glEnd()
        
        # Grid no chão
        glColor3f(0.3, 0.4, 0.3)
        glBegin(GL_LINES)
        for i in range(-10, 11, 2):
            glVertex3f(i, -2.99, -10)
            glVertex3f(i, -2.99, 10)
            glVertex3f(-10, -2.99, i)
            glVertex3f(10, -2.99, i)
        glEnd()
        
        glEnable(GL_LIGHTING)
    
    def draw_ui(self):
        """Desenha interface 2D sobre o 3D"""
        if not self.show_help:
            return
        
        # Salvar estado OpenGL
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        
        # Fundo semi-transparente
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0, 0, 0, 0.7)
        glBegin(GL_QUADS)
        glVertex2f(20, 20)
        glVertex2f(400, 20)
        glVertex2f(400, 300)
        glVertex2f(20, 300)
        glEnd()
        glDisable(GL_BLEND)
        
        # Restaurar estado
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    def run(self):
        """Loop principal da aplicação"""
        print("🌟 Iniciando BLOB 3D Advanced...")
        print("="*50)
        print("🎮 CONTROLES:")
        print("  🖱️  Mouse: Rotacionar câmera")
        print("  🎡 Scroll: Zoom in/out")
        print("  🎤 SPACE: Ligar/desligar sistema de voz")
        print("  📊 1-5: Alterar emoções")
        print("  ❓ H: Mostrar/ocultar ajuda")
        print("  🚪 ESC: Sair")
        print()
        print("🗣️  COMANDOS DE VOZ:")
        print("  • 'feliz', 'triste', 'animado', 'pensando'")
        print("  • 'nome', 'como você está', 'dança', 'pula'")
        print("="*50)
        
        self.init_opengl()
        
        # Iniciar sistema de voz automaticamente
        if VOICE_AVAILABLE:
            self.voice_system.start_listening()
            print("🎤 Sistema de voz ativo - fale comigo!")
        
        last_time = time.time()
        
        while self.running:
            current_time = time.time()
            time_delta = current_time - last_time
            last_time = current_time
            
            # Atualizar timer de ajuda
            if self.help_timer > 0:
                self.help_timer -= time_delta
                if self.help_timer <= 0:
                    self.show_help = False
            
            self.handle_events()
            
            # Atualizar componentes
            self.blob.update(time_delta)
            
            # Renderizar
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Aplicar câmera
            self.camera.apply()
            
            # Desenhar ambiente
            self.draw_environment()
            
            # Desenhar BLOB
            self.blob.render()
            
            # Interface 2D
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        # Cleanup
        if self.voice_system.enabled:
            self.voice_system.stop_listening()
        pygame.quit()

def main():
    """Função principal"""
    try:
        app = BLOB3DAdvanced()
        app.run()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()