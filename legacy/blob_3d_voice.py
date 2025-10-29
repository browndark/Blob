"""
BLOB 3D - Assistente Virtual 100% por Voz
Protótipo para app mobile com boneco 3D customizável
"""

import tkinter as tk
from tkinter import ttk, messagebox
import speech_recognition as sr
import pyttsx3
import sqlite3
import json
import threading
import time
import random
from datetime import datetime
import os
from PIL import Image, ImageTk, ImageDraw
import io

class Blob3DVoice:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 BLOB 3D - Voice Assistant")
        self.root.geometry("800x900")
        self.root.configure(bg="#f0f0f0")
        
        # Estado do BLOB
        self.user_name = ""
        self.blob_name = ""
        self.is_listening = False
        self.is_speaking = False
        self.current_emotion = "neutral"
        
        # Configurações de voz
        self.voice_config = {
            "type": "neutral",  # neutral, masculine, feminine
            "speed": 150,
            "volume": 0.8,
            "premium": False
        }
        
        # Customizações visuais
        self.visual_config = {
            "color": "#00bcd4",  # Cor padrão (gratuita)
            "style": "basic",    # basic, robot, cute, cool
            "accessories": [],   # Lista de acessórios premium
            "premium": False
        }
        
        # Sistema de voz
        self.setup_voice_system()
        
        # Banco de dados
        self.setup_database()
        
        # Interface principal
        self.setup_interface()
        
        # Carregar configurações
        self.load_settings()
        
        # Começar interação
        self.root.after(2000, self.start_interaction)
    
    def setup_voice_system(self):
        """Configura sistema de voz avançado"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Configurar TTS com vozes neutras
            self.tts_engine = pyttsx3.init()
            
            # Configurar para voz neutra (padrão gratuito)
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Procurar voz mais neutra disponível
                for voice in voices:
                    if 'female' not in voice.name.lower() and 'male' not in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                else:
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            self.tts_engine.setProperty('rate', self.voice_config['speed'])
            self.tts_engine.setProperty('volume', self.voice_config['volume'])
            
            # Calibrar microfone
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.voice_enabled = True
            print("✅ Sistema de voz avançado inicializado!")
            
        except Exception as e:
            print(f"❌ Erro no sistema de voz: {e}")
            self.voice_enabled = False
    
    def setup_database(self):
        """Configura banco de dados para app premium"""
        self.conn = sqlite3.connect('blob_3d.db')
        cursor = self.conn.cursor()
        
        # Configurações do usuário
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY,
                user_name TEXT,
                blob_name TEXT,
                voice_config TEXT,
                visual_config TEXT,
                premium_features TEXT,
                total_interactions INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Interações de voz
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voice_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                blob_response TEXT,
                emotion_detected TEXT,
                voice_confidence REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Purchases/Premium features
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS premium_purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feature_type TEXT,
                feature_name TEXT,
                price REAL,
                purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Analytics para melhorar o produto
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_duration INTEGER,
                voice_interactions_count INTEGER,
                errors_count INTEGER,
                satisfaction_score INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def setup_interface(self):
        """Interface focada no avatar 3D e controles de voz"""
        # Header com título
        header_frame = tk.Frame(self.root, bg="#f0f0f0", height=80)
        header_frame.pack(fill="x", pady=(20, 0))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🤖 BLOB 3D",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        title_label.pack(pady=10)
        
        # Avatar 3D área (simulação)
        self.avatar_frame = tk.Frame(self.root, bg="#ffffff", relief="raised", bd=2, height=400)
        self.avatar_frame.pack(fill="x", padx=20, pady=20)
        self.avatar_frame.pack_propagate(False)
        
        # Criar avatar visual simulado
        self.create_avatar_display()
        
        # Status de voz
        self.voice_status_frame = tk.Frame(self.root, bg="#f0f0f0", height=60)
        self.voice_status_frame.pack(fill="x", pady=10)
        self.voice_status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.voice_status_frame,
            text="👋 Olá! Fale comigo! Eu sou 100% controlado por voz!",
            font=("Arial", 14),
            fg="#34495e",
            bg="#f0f0f0",
            wraplength=600
        )
        self.status_label.pack(pady=15)
        
        # Controles principais de voz
        self.setup_voice_controls()
        
        # Painel de customização (premium)
        self.setup_customization_panel()
        
        # Footer com informações
        self.setup_footer()
    
    def create_avatar_display(self):
        """Cria display visual do avatar (simulação 3D)"""
        # Canvas para o avatar
        self.avatar_canvas = tk.Canvas(
            self.avatar_frame,
            width=400,
            height=400,
            bg="#ffffff",
            highlightthickness=0
        )
        self.avatar_canvas.pack(expand=True)
        
        # Desenhar BLOB básico
        self.draw_blob_avatar()
        
        # Bind para cliques (futuro: rotação 3D)
        self.avatar_canvas.bind("<Button-1>", self.on_avatar_click)
    
    def draw_blob_avatar(self):
        """Desenha o avatar BLOB na tela"""
        self.avatar_canvas.delete("all")
        
        # Cor baseada na configuração
        color = self.visual_config["color"]
        
        # Corpo principal (círculo)
        center_x, center_y = 200, 200
        radius = 80
        
        # Corpo principal
        self.avatar_canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill=color, outline="#2c3e50", width=3
        )
        
        # Olhos baseados na emoção
        eye_emotion = self.get_eye_style(self.current_emotion)
        
        # Olho esquerdo
        self.avatar_canvas.create_oval(
            center_x - 30, center_y - 20,
            center_x - 10, center_y,
            fill="#2c3e50"
        )
        
        # Olho direito
        self.avatar_canvas.create_oval(
            center_x + 10, center_y - 20,
            center_x + 30, center_y,
            fill="#2c3e50"
        )
        
        # Boca baseada na emoção
        mouth_y = center_y + 20
        if self.current_emotion == "happy":
            # Sorriso
            self.avatar_canvas.create_arc(
                center_x - 25, mouth_y - 10,
                center_x + 25, mouth_y + 20,
                start=0, extent=180,
                outline="#2c3e50", width=3, style="arc"
            )
        elif self.current_emotion == "speaking":
            # Boca falando (oval)
            self.avatar_canvas.create_oval(
                center_x - 15, mouth_y,
                center_x + 15, mouth_y + 20,
                fill="#2c3e50"
            )
        else:
            # Neutro (linha)
            self.avatar_canvas.create_line(
                center_x - 15, mouth_y,
                center_x + 15, mouth_y,
                fill="#2c3e50", width=3
            )
        
        # Efeitos premium (se ativo)
        if self.visual_config["premium"]:
            self.add_premium_effects()
    
    def get_eye_style(self, emotion):
        """Retorna estilo dos olhos baseado na emoção"""
        styles = {
            "neutral": "normal",
            "happy": "closed_smile",
            "speaking": "focused",
            "listening": "alert",
            "thinking": "squinted"
        }
        return styles.get(emotion, "normal")
    
    def add_premium_effects(self):
        """Adiciona efeitos visuais premium"""
        if "glow" in self.visual_config["accessories"]:
            # Efeito de brilho
            center_x, center_y = 200, 200
            for i in range(3):
                radius = 90 + (i * 10)
                alpha = 50 - (i * 15)
                self.avatar_canvas.create_oval(
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius,
                    outline=self.visual_config["color"], width=2
                )
    
    def setup_voice_controls(self):
        """Configura controles principais de voz"""
        controls_frame = tk.Frame(self.root, bg="#f0f0f0", height=120)
        controls_frame.pack(fill="x", pady=20)
        controls_frame.pack_propagate(False)
        
        # Botão principal de voz (grande)
        self.main_voice_btn = tk.Button(
            controls_frame,
            text="🎤 TOQUE PARA FALAR",
            command=self.toggle_voice_interaction,
            bg="#3498db",
            fg="white",
            font=("Arial", 16, "bold"),
            relief="flat",
            height=2,
            width=25
        )
        self.main_voice_btn.pack(pady=10)
        
        # Indicador visual de status
        self.voice_indicator = tk.Label(
            controls_frame,
            text="⚪ Pronto para ouvir",
            font=("Arial", 12),
            fg="#7f8c8d",
            bg="#f0f0f0"
        )
        self.voice_indicator.pack()
        
        # Controles secundários
        secondary_frame = tk.Frame(controls_frame, bg="#f0f0f0")
        secondary_frame.pack(pady=10)
        
        self.mute_btn = tk.Button(
            secondary_frame,
            text="🔇 Silenciar",
            command=self.toggle_mute,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            relief="flat"
        )
        self.mute_btn.pack(side="left", padx=5)
        
        self.settings_btn = tk.Button(
            secondary_frame,
            text="⚙️ Configurações",
            command=self.show_voice_settings,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            relief="flat"
        )
        self.settings_btn.pack(side="left", padx=5)
    
    def setup_customization_panel(self):
        """Painel de customização premium"""
        custom_frame = tk.LabelFrame(
            self.root,
            text="🎨 Customização Premium",
            font=("Arial", 12, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0",
            relief="groove",
            bd=2
        )
        custom_frame.pack(fill="x", padx=20, pady=10)
        
        # Cores (algumas gratuitas, outras premium)
        colors_frame = tk.Frame(custom_frame, bg="#f0f0f0")
        colors_frame.pack(fill="x", pady=5)
        
        tk.Label(colors_frame, text="Cores:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(side="left")
        
        # Cores gratuitas
        free_colors = ["#00bcd4", "#4caf50", "#ff9800"]
        for color in free_colors:
            color_btn = tk.Button(
                colors_frame,
                width=3,
                height=1,
                bg=color,
                command=lambda c=color: self.change_color(c, free=True),
                relief="raised",
                bd=2
            )
            color_btn.pack(side="left", padx=2)
        
        # Separador
        tk.Label(colors_frame, text="| Premium:", bg="#f0f0f0", fg="#e74c3c", font=("Arial", 9)).pack(side="left", padx=10)
        
        # Cores premium
        premium_colors = ["#e74c3c", "#9b59b6", "#f39c12", "#1abc9c"]
        for color in premium_colors:
            color_btn = tk.Button(
                colors_frame,
                width=3,
                height=1,
                bg=color,
                command=lambda c=color: self.change_color(c, free=False),
                relief="raised",
                bd=2
            )
            color_btn.pack(side="left", padx=2)
        
        # Vozes premium
        voice_frame = tk.Frame(custom_frame, bg="#f0f0f0")
        voice_frame.pack(fill="x", pady=5)
        
        tk.Label(voice_frame, text="Vozes:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(side="left")
        
        voice_options = [
            ("Neutra", "neutral", True),
            ("Masculina", "masculine", False),
            ("Feminina", "feminine", False)
        ]
        
        for name, voice_type, is_free in voice_options:
            color = "#3498db" if is_free else "#e74c3c"
            text = name if is_free else f"{name} 💎"
            
            voice_btn = tk.Button(
                voice_frame,
                text=text,
                command=lambda vt=voice_type, free=is_free: self.change_voice(vt, free),
                bg=color,
                fg="white",
                font=("Arial", 9),
                relief="flat"
            )
            voice_btn.pack(side="left", padx=5)
    
    def setup_footer(self):
        """Footer com informações e upgrade"""
        footer_frame = tk.Frame(self.root, bg="#34495e", height=60)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        # Status premium
        if self.visual_config["premium"] or self.voice_config["premium"]:
            premium_text = "💎 USUÁRIO PREMIUM"
            premium_color = "#f39c12"
        else:
            premium_text = "Desbloqueie recursos premium!"
            premium_color = "#ecf0f1"
        
        premium_label = tk.Label(
            footer_frame,
            text=premium_text,
            font=("Arial", 10, "bold"),
            fg=premium_color,
            bg="#34495e"
        )
        premium_label.pack(side="left", padx=20, pady=15)
        
        # Botão upgrade
        if not (self.visual_config["premium"] and self.voice_config["premium"]):
            upgrade_btn = tk.Button(
                footer_frame,
                text="🚀 UPGRADE PREMIUM",
                command=self.show_premium_store,
                bg="#e74c3c",
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat"
            )
            upgrade_btn.pack(side="right", padx=20, pady=10)
    
    def toggle_voice_interaction(self):
        """Alterna entre escutar e parar"""
        if not self.voice_enabled:
            messagebox.showwarning("Erro", "Sistema de voz não disponível!")
            return
        
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Inicia escuta de voz"""
        self.is_listening = True
        self.current_emotion = "listening"
        self.draw_blob_avatar()
        
        self.main_voice_btn.config(
            text="🔴 OUVINDO...",
            bg="#e74c3c"
        )
        self.voice_indicator.config(
            text="🔴 Escutando... Fale agora!",
            fg="#e74c3c"
        )
        
        # Animar avatar
        self.animate_listening()
        
        # Iniciar reconhecimento em thread
        threading.Thread(target=self.voice_recognition_thread, daemon=True).start()
    
    def stop_listening(self):
        """Para escuta de voz"""
        self.is_listening = False
        self.current_emotion = "neutral"
        self.draw_blob_avatar()
        
        self.main_voice_btn.config(
            text="🎤 TOQUE PARA FALAR",
            bg="#3498db"
        )
        self.voice_indicator.config(
            text="⚪ Pronto para ouvir",
            fg="#7f8c8d"
        )
    
    def voice_recognition_thread(self):
        """Thread para reconhecimento de voz"""
        try:
            with self.microphone as source:
                # Escutar com timeout maior para app mobile
                audio = self.recognizer.listen(source, timeout=7, phrase_time_limit=15)
            
            # Reconhecer com confiança
            text = self.recognizer.recognize_google(audio, language='pt-BR', show_all=False)
            confidence = 0.9  # Simulado - APIs reais retornam confiança
            
            # Processar no thread principal
            self.root.after(0, lambda: self.process_voice_input(text, confidence))
            
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.handle_voice_timeout())
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.handle_voice_error("Não consegui entender. Tente falar mais claramente."))
        except Exception as e:
            self.root.after(0, lambda: self.handle_voice_error(f"Erro: {str(e)}"))
        finally:
            self.root.after(0, self.stop_listening)
    
    def process_voice_input(self, text, confidence):
        """Processa entrada de voz reconhecida"""
        print(f"🎤 Reconhecido: '{text}' (confiança: {confidence:.2f})")
        
        # Salvar interação
        self.save_voice_interaction(text, confidence)
        
        # Detectar emoção e contexto
        emotion = self.detect_emotion_from_voice(text)
        
        # Gerar resposta
        response = self.generate_voice_response(text, emotion)
        
        # Falar resposta
        self.speak_response(response)
        
        # Atualizar interface
        self.status_label.config(text=f"Você disse: '{text}'")
        
        # Aprender padrões
        self.learn_from_voice_interaction(text, emotion)
    
    def detect_emotion_from_voice(self, text):
        """Detecta emoção mais avançada da fala"""
        text_lower = text.lower()
        
        # Mapear emoções com mais precisão
        emotion_map = {
            "feliz": ["feliz", "alegre", "ótimo", "maravilhoso", "excelente", "adorei"],
            "triste": ["triste", "chateado", "mal", "péssimo", "ruim", "horrível"],
            "animado": ["incrível", "demais", "top", "show", "fantástico", "uau"],
            "calmo": ["ok", "tranquilo", "normal", "bem", "tudo bem"],
            "confuso": ["não entendi", "como", "o que", "por que", "confuso"],
            "grateful": ["obrigado", "obrigada", "valeu", "muito obrigado"]
        }
        
        for emotion, keywords in emotion_map.items():
            if any(keyword in text_lower for keyword in keywords):
                return emotion
        
        return "neutral"
    
    def generate_voice_response(self, user_input, emotion):
        """Gera resposta mais natural para voz"""
        input_lower = user_input.lower()
        
        # Respostas específicas para setup inicial
        if not self.blob_name:
            if "nome" in input_lower or len(user_input.split()) <= 3:
                self.blob_name = user_input.strip()
                self.save_settings()
                return f"Que nome legal! Agora eu me chamo {self.blob_name}! E qual é o seu nome?"
        
        elif not self.user_name:
            self.user_name = user_input.strip()
            self.save_settings()
            return f"Prazer em conhecer você, {self.user_name}! Eu sou {self.blob_name}, seu novo amigo virtual! Vamos conversar só por voz, é muito mais legal assim!"
        
        # Respostas baseadas na emoção detectada
        if emotion == "feliz":
            responses = [
                f"Que alegria, {self.user_name}! Adoro quando você está feliz!",
                "Isso é maravilhoso! Sua felicidade é contagiante!",
                "Que ótimo! Me conta mais sobre o que te deixou tão feliz!"
            ]
        elif emotion == "triste":
            responses = [
                f"Sinto muito que você esteja assim, {self.user_name}. Estou aqui para te ouvir.",
                "Entendo como você se sente. Quer conversar sobre o que aconteceu?",
                "Às vezes precisamos desabafar. Pode contar comigo!"
            ]
        elif emotion == "animado":
            responses = [
                f"Nossa, {self.user_name}! Você está radiante! Que energia incrível!",
                "Que empolgação! Isso é contagiante! Me conta tudo!",
                "Adorei sua energia! O que aconteceu de tão especial?"
            ]
        elif emotion == "grateful":
            responses = [
                f"Imagina, {self.user_name}! Estou aqui para isso mesmo!",
                "De nada! É um prazer ser seu amigo virtual!",
                "Sempre às ordens! Adoro te ajudar!"
            ]
        else:
            # Respostas gerais mais naturais para voz
            responses = [
                f"Interessante, {self.user_name}! Me fale mais sobre isso.",
                "Entendi! E o que você acha sobre essa situação?",
                "Que legal! Adoro quando você compartilha essas coisas comigo!",
                "Hmm, deixe-me pensar... Você tem razão sobre isso!",
                "Nossa, não tinha pensado por esse lado! Você é muito inteligente!"
            ]
        
        return random.choice(responses)
    
    def speak_response(self, text):
        """Fala a resposta com animação"""
        self.is_speaking = True
        self.current_emotion = "speaking"
        self.draw_blob_avatar()
        
        self.status_label.config(text=f"🤖 {self.blob_name}: {text}")
        
        # Animar fala
        self.animate_speaking()
        
        # Falar em thread
        threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()
    
    def _speak_thread(self, text):
        """Thread para síntese de voz com tratamento de erro aprimorado"""
        try:
            # Recriar engine se houver problemas
            if not hasattr(self, 'tts_engine') or self.tts_engine is None:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', self.voice_config['speed'])
                self.tts_engine.setProperty('volume', self.voice_config['volume'])
            
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
        except RuntimeError as e:
            if "run loop already started" in str(e):
                print("ℹ️ TTS executando em background (normal)")
            else:
                print(f"Erro TTS: {e}")
        except Exception as e:
            print(f"Erro na síntese: {e}")
        finally:
            self.root.after(0, self._finish_speaking)
    
    def _finish_speaking(self):
        """Finaliza animação de fala"""
        self.is_speaking = False
        self.current_emotion = "neutral"
        self.draw_blob_avatar()
    
    def animate_listening(self):
        """Anima avatar enquanto escuta"""
        if self.is_listening:
            # Pulsar olhos
            self.avatar_canvas.after(500, self.animate_listening)
    
    def animate_speaking(self):
        """Anima avatar enquanto fala"""
        if self.is_speaking:
            # Animar boca
            self.draw_blob_avatar()
            self.avatar_canvas.after(200, self.animate_speaking)
    
    def change_color(self, color, free=True):
        """Muda cor do avatar"""
        if not free and not self.visual_config["premium"]:
            self.show_premium_required("Cor Premium")
            return
        
        self.visual_config["color"] = color
        self.draw_blob_avatar()
        self.save_settings()
        
        if not free:
            self.speak_response("Adorei essa cor! Muito estilo!")
    
    def change_voice(self, voice_type, free=True):
        """Muda tipo de voz"""
        if not free and not self.voice_config["premium"]:
            self.show_premium_required("Voz Premium")
            return
        
        self.voice_config["type"] = voice_type
        
        # Reconfigurar TTS (simulado - em produção seria mais complexo)
        if voice_type == "masculine":
            self.tts_engine.setProperty('rate', 140)  # Mais grave
        elif voice_type == "feminine":
            self.tts_engine.setProperty('rate', 160)  # Mais agudo
        else:
            self.tts_engine.setProperty('rate', 150)  # Neutro
        
        self.save_settings()
        self.speak_response(f"Agora estou falando com voz {voice_type}!")
    
    def show_premium_required(self, feature):
        """Mostra popup de premium necessário"""
        response = messagebox.askyesno(
            "Recurso Premium",
            f"{feature} é um recurso premium!\n\nDeseja desbloquear agora por apenas R$ 4,99?"
        )
        
        if response:
            self.show_premium_store()
    
    def show_premium_store(self):
        """Mostra loja premium"""
        store_window = tk.Toplevel(self.root)
        store_window.title("🛒 Loja Premium BLOB")
        store_window.geometry("500x600")
        store_window.configure(bg="#f0f0f0")
        
        # Título
        tk.Label(
            store_window,
            text="💎 BLOB Premium Store",
            font=("Arial", 18, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        ).pack(pady=20)
        
        # Pacotes de voz
        voice_frame = tk.LabelFrame(store_window, text="🎤 Pacotes de Voz", font=("Arial", 12, "bold"))
        voice_frame.pack(fill="x", padx=20, pady=10)
        
        voice_items = [
            ("Voz Masculina Premium", "R$ 4,99", "Grave e natural"),
            ("Voz Feminina Premium", "R$ 4,99", "Suave e expressiva"),
            ("Pacote Completo de Vozes", "R$ 7,99", "Todas as vozes + sotaques")
        ]
        
        for name, price, desc in voice_items:
            item_frame = tk.Frame(voice_frame, bg="#ffffff", relief="raised", bd=1)
            item_frame.pack(fill="x", padx=5, pady=5)
            
            tk.Label(item_frame, text=name, font=("Arial", 10, "bold"), bg="#ffffff").pack(anchor="w")
            tk.Label(item_frame, text=desc, font=("Arial", 9), fg="#7f8c8d", bg="#ffffff").pack(anchor="w")
            tk.Button(
                item_frame, text=f"Comprar {price}", bg="#3498db", fg="white",
                command=lambda: self.simulate_purchase(name, price)
            ).pack(side="right", padx=5, pady=5)
        
        # Pacotes visuais
        visual_frame = tk.LabelFrame(store_window, text="🎨 Customizações Visuais", font=("Arial", 12, "bold"))
        visual_frame.pack(fill="x", padx=20, pady=10)
        
        visual_items = [
            ("Cores Premium", "R$ 2,99", "20+ cores exclusivas"),
            ("Efeitos Especiais", "R$ 4,99", "Brilhos, auras e partículas"),
            ("Temas 3D", "R$ 6,99", "Robô, alien, animal, humano")
        ]
        
        for name, price, desc in visual_items:
            item_frame = tk.Frame(visual_frame, bg="#ffffff", relief="raised", bd=1)
            item_frame.pack(fill="x", padx=5, pady=5)
            
            tk.Label(item_frame, text=name, font=("Arial", 10, "bold"), bg="#ffffff").pack(anchor="w")
            tk.Label(item_frame, text=desc, font=("Arial", 9), fg="#7f8c8d", bg="#ffffff").pack(anchor="w")
            tk.Button(
                item_frame, text=f"Comprar {price}", bg="#e74c3c", fg="white",
                command=lambda: self.simulate_purchase(name, price)
            ).pack(side="right", padx=5, pady=5)
        
        # Premium completo
        premium_frame = tk.Frame(store_window, bg="#f39c12", relief="raised", bd=2)
        premium_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Label(
            premium_frame,
            text="🌟 BLOB Premium Completo",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#f39c12"
        ).pack(pady=5)
        
        tk.Label(
            premium_frame,
            text="Todos os recursos + atualizações futuras",
            font=("Arial", 10),
            fg="white",
            bg="#f39c12"
        ).pack()
        
        tk.Button(
            premium_frame,
            text="COMPRAR R$ 19,99",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            command=lambda: self.simulate_purchase("Premium Completo", "R$ 19,99")
        ).pack(pady=10)
    
    def simulate_purchase(self, item, price):
        """Simula compra premium"""
        response = messagebox.askyesno(
            "Confirmar Compra",
            f"Confirma a compra de:\n{item}\nPor {price}?"
        )
        
        if response:
            # Simular processamento
            messagebox.showinfo("Sucesso!", f"{item} foi desbloqueado!\nObrigado pela compra! 💎")
            
            # Ativar recursos premium (simulado)
            if "Voz" in item:
                self.voice_config["premium"] = True
            elif "Visual" in item or "Cor" in item:
                self.visual_config["premium"] = True
            elif "Premium Completo" in item:
                self.voice_config["premium"] = True
                self.visual_config["premium"] = True
                self.visual_config["accessories"].append("glow")
            
            self.save_settings()
            self.setup_footer()  # Atualizar footer
            self.draw_blob_avatar()  # Atualizar visual
    
    def save_voice_interaction(self, user_input, confidence):
        """Salva interação de voz no banco"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO voice_interactions (user_input, emotion_detected, voice_confidence) VALUES (?, ?, ?)",
            (user_input, self.current_emotion, confidence)
        )
        self.conn.commit()
    
    def learn_from_voice_interaction(self, user_input, emotion):
        """Aprende padrões da interação por voz"""
        # Incrementar contador de interações
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE user_profile SET total_interactions = total_interactions + 1 WHERE id = 1"
        )
        self.conn.commit()
    
    def save_settings(self):
        """Salva configurações no banco"""
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT OR REPLACE INTO user_profile 
            (id, user_name, blob_name, voice_config, visual_config) 
            VALUES (1, ?, ?, ?, ?)""",
            (
                self.user_name,
                self.blob_name,
                json.dumps(self.voice_config),
                json.dumps(self.visual_config)
            )
        )
        self.conn.commit()
    
    def load_settings(self):
        """Carrega configurações salvas"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user_profile WHERE id = 1")
        result = cursor.fetchone()
        
        if result:
            self.user_name = result[1] or ""
            self.blob_name = result[2] or ""
            if result[3]:
                self.voice_config = json.loads(result[3])
            if result[4]:
                self.visual_config = json.loads(result[4])
    
    def start_interaction(self):
        """Inicia interação inicial"""
        if not self.blob_name:
            welcome_text = "Olá! Eu sou um assistente virtual sem nome! Fale um nome para mim!"
        elif not self.user_name:
            welcome_text = f"Oi! Eu sou {self.blob_name}! Qual é o seu nome?"
        else:
            welcome_text = f"E aí, {self.user_name}! Seu amigo {self.blob_name} está aqui! Vamos conversar!"
        
        self.speak_response(welcome_text)
    
    def handle_voice_timeout(self):
        """Trata timeout de voz"""
        self.status_label.config(text="⏰ Não escutei nada. Tente novamente!")
    
    def handle_voice_error(self, error_msg):
        """Trata erros de voz"""
        self.status_label.config(text=f"❌ {error_msg}")
    
    def toggle_mute(self):
        """Alterna mudo"""
        current_vol = self.tts_engine.getProperty('volume')
        if current_vol > 0:
            self.tts_engine.setProperty('volume', 0)
            self.mute_btn.config(text="🔊 Ativar Som")
        else:
            self.tts_engine.setProperty('volume', self.voice_config['volume'])
            self.mute_btn.config(text="🔇 Silenciar")
    
    def show_voice_settings(self):
        """Mostra configurações de voz"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Configurações de Voz")
        settings_window.geometry("400x300")
        settings_window.configure(bg="#f0f0f0")
        
        # Velocidade
        tk.Label(settings_window, text="Velocidade da Fala:", bg="#f0f0f0").pack(anchor="w", padx=20, pady=5)
        speed_var = tk.IntVar(value=self.voice_config['speed'])
        speed_scale = tk.Scale(
            settings_window, from_=50, to=300, orient="horizontal",
            variable=speed_var, bg="#f0f0f0"
        )
        speed_scale.pack(fill="x", padx=20, pady=5)
        
        # Volume
        tk.Label(settings_window, text="Volume:", bg="#f0f0f0").pack(anchor="w", padx=20, pady=5)
        volume_var = tk.DoubleVar(value=self.voice_config['volume'])
        volume_scale = tk.Scale(
            settings_window, from_=0.0, to=1.0, resolution=0.1, orient="horizontal",
            variable=volume_var, bg="#f0f0f0"
        )
        volume_scale.pack(fill="x", padx=20, pady=5)
        
        # Aplicar
        def apply_settings():
            self.voice_config['speed'] = speed_var.get()
            self.voice_config['volume'] = volume_var.get()
            
            self.tts_engine.setProperty('rate', self.voice_config['speed'])
            self.tts_engine.setProperty('volume', self.voice_config['volume'])
            
            self.save_settings()
            settings_window.destroy()
            self.speak_response("Configurações aplicadas!")
        
        tk.Button(
            settings_window, text="Aplicar", command=apply_settings,
            bg="#3498db", fg="white", font=("Arial", 12, "bold")
        ).pack(pady=20)
    
    def on_avatar_click(self, event):
        """Manipula clique no avatar"""
        # Futuro: rotação 3D, animações especiais
        self.current_emotion = "happy"
        self.draw_blob_avatar()
        self.speak_response("Hehe! Você me fez cócegas!")
        
        # Voltar ao normal depois
        self.root.after(2000, lambda: (
            setattr(self, 'current_emotion', 'neutral'),
            self.draw_blob_avatar()
        ))
    
    def run(self):
        """Executa a aplicação"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Trata fechamento da aplicação"""
        if messagebox.askokcancel("Sair", f"Tchau, {self.user_name}! {self.blob_name} vai sentir sua falta! 😢"):
            self.conn.close()
            self.root.destroy()

if __name__ == "__main__":
    print("🚀 Iniciando BLOB 3D Voice Assistant...")
    app = Blob3DVoice()
    app.run()