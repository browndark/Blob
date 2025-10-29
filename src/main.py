"""
BLOB - Assistente Virtual Interativo
Um amigo virtual que aprende com você e desenvolve personalidade única!
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import speech_recognition as sr
import pyttsx3
import sqlite3
import json
import threading
import time
import random
from datetime import datetime
import os

class BlobAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 BLOB - Seu Melhor Amigo Virtual")
        self.root.geometry("900x700")
        self.root.configure(bg="#ecf0f1")
        
        # Configurações
        self.user_name = ""
        self.blob_name = ""
        self.conversation_history = []
        self.personality_traits = {
            "friendliness": 0.9,
            "humor": 0.7,
            "curiosity": 0.8,
            "empathy": 0.9,
            "playfulness": 0.6,
            "learning_rate": 0.05
        }
        
        # Sistema de voz
        self.setup_voice_system()
        
        # Banco de dados
        self.setup_database()
        
        # Interface
        self.setup_interface()
        
        # Verificar se é primeira vez
        self.check_first_run()
        
    def setup_voice_system(self):
        """Configura sistema de reconhecimento e síntese de voz"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Configurar TTS
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.8)
            
            self.voice_enabled = True
            print("✅ Sistema de voz inicializado!")
            
        except Exception as e:
            print(f"⚠️ Erro no sistema de voz: {e}")
            self.voice_enabled = False
    
    def setup_database(self):
        """Configura banco de dados SQLite"""
        self.conn = sqlite3.connect('blob_memories.db')
        cursor = self.conn.cursor()
        
        # Tabela de configurações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_config (
                id INTEGER PRIMARY KEY,
                user_name TEXT,
                blob_name TEXT,
                personality_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de conversas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT,
                blob_response TEXT,
                emotion_context TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de aprendizado
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_data TEXT,
                usage_count INTEGER DEFAULT 1,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def setup_interface(self):
        """Cria interface gráfica moderna"""
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg="#1a1a2e")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="🤖 BLOB",
            font=("Arial", 28, "bold"),
            fg="#0f3460",
            bg="#1a1a2e"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Seu Assistente Virtual Inteligente",
            font=("Arial", 12),
            fg="#16213e",
            bg="#1a1a2e"
        )
        subtitle_label.pack()
        
        # Avatar e status
        avatar_frame = tk.Frame(main_frame, bg="#16213e", relief="raised", bd=2)
        avatar_frame.pack(pady=10)
        
        self.avatar_label = tk.Label(
            avatar_frame,
            text="😊",
            font=("Arial", 80),
            bg="#16213e",
            fg="#0f3460"
        )
        self.avatar_label.pack(padx=40, pady=40)
        
        self.status_label = tk.Label(
            main_frame,
            text="Olá! Eu sou BLOB, seu novo amigo virtual! 🌟",
            font=("Arial", 14),
            fg="#2c3e50",
            bg="#ecf0f1",
            wraplength=700,
            relief="flat",
            bd=5
        )
        self.status_label.pack(pady=10)
        
        # Área de chat
        chat_frame = tk.Frame(main_frame, bg="#ecf0f1")
        chat_frame.pack(fill="both", expand=True, pady=20)
        
        self.chat_area = scrolledtext.ScrolledText(
            chat_frame,
            height=12,
            font=("Consolas", 11),
            bg="#f8f9fa",
            fg="#2c3e50",
            insertbackground="#2c3e50",
            wrap=tk.WORD,
            relief="flat",
            bd=10,
            selectbackground="#3498db",
            selectforeground="#ffffff"
        )
        self.chat_area.pack(fill="both", expand=True)
        
        # Área de entrada
        input_frame = tk.Frame(main_frame, bg="#ecf0f1")
        input_frame.pack(fill="x", pady=10)
        
        self.text_input = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg="#ffffff",
            fg="#2c3e50",
            insertbackground="#2c3e50",
            relief="flat",
            bd=10
        )
        self.text_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.text_input.bind("<Return>", self.send_message)
        
        # Botões
        button_frame = tk.Frame(input_frame, bg="#ecf0f1")
        button_frame.pack(side="right")
        
        self.send_btn = tk.Button(
            button_frame,
            text="📤 Enviar",
            command=self.send_message,
            bg="#e94560",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5
        )
        self.send_btn.pack(side="left", padx=2)
        
        self.voice_btn = tk.Button(
            button_frame,
            text="🎤 Falar",
            command=self.toggle_voice_listening,
            bg="#0f3460",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5
        )
        self.voice_btn.pack(side="left", padx=2)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ Limpar",
            command=self.clear_chat,
            bg="#16213e",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=15,
            pady=5
        )
        self.clear_btn.pack(side="left", padx=2)
        
        # Configurações
        config_frame = tk.Frame(main_frame, bg="#ecf0f1")
        config_frame.pack(fill="x", pady=5)
        
        self.config_btn = tk.Button(
            config_frame,
            text="⚙️ Configurações",
            command=self.show_settings,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 9),
            relief="flat"
        )
        self.config_btn.pack(side="right")
    
    def check_first_run(self):
        """Verifica se é a primeira execução"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user_config ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            self.user_name = result[1]
            self.blob_name = result[2]
            if result[3]:
                self.personality_traits = json.loads(result[3])
            
            self.welcome_back()
        else:
            self.first_time_setup()
    
    def first_time_setup(self):
        """Configuração inicial para novos usuários"""
        self.add_message("BLOB", "Olá! Eu sou um assistente virtual especial! 🌟")
        self.add_message("BLOB", "Eu não tenho nome ainda... Você pode escolher um nome para mim?")
        self.status_label.config(text="💭 Aguardando você me dar um nome...")
        self.waiting_for = "blob_name"
    
    def welcome_back(self):
        """Boas-vindas para usuários existentes"""
        welcome_messages = [
            f"Oi {self.user_name}! 😊 Que bom te ver de novo!",
            f"Olá {self.user_name}! 🌟 Senti sua falta!",
            f"Ei {self.user_name}! 🤗 Como você está hoje?",
            f"Hey {self.user_name}! 😄 Estava esperando por você!"
        ]
        
        message = random.choice(welcome_messages)
        self.add_message(self.blob_name, message)
        self.status_label.config(text=f"💬 {self.blob_name} está pronto para conversar!")
        self.speak(message)
        self.waiting_for = None
    
    def send_message(self, event=None):
        """Envia mensagem do usuário"""
        message = self.text_input.get().strip()
        if not message:
            return
        
        self.text_input.delete(0, tk.END)
        self.add_message("Você", message)
        
        # Processar em thread separada
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def process_message(self, message):
        """Processa mensagem do usuário"""
        if hasattr(self, 'waiting_for'):
            if self.waiting_for == "blob_name":
                self.set_blob_name(message)
            elif self.waiting_for == "user_name":
                self.set_user_name(message)
            else:
                self.generate_response(message)
        else:
            self.generate_response(message)
    
    def set_blob_name(self, name):
        """Define nome do BLOB"""
        self.blob_name = name.strip()
        response = f"Que nome lindo! 🎉 Agora eu sou {self.blob_name}!"
        self.add_message(self.blob_name, response)
        self.speak(response)
        
        time.sleep(1)
        
        response2 = "E qual é o seu nome? 😊"
        self.add_message(self.blob_name, response2)
        self.speak(response2)
        
        self.status_label.config(text=f"💭 {self.blob_name} quer saber seu nome...")
        self.waiting_for = "user_name"
        self.animate_avatar("happy")
    
    def set_user_name(self, name):
        """Define nome do usuário"""
        self.user_name = name.strip()
        
        # Salvar configuração
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO user_config (id, user_name, blob_name, personality_data) VALUES (1, ?, ?, ?)",
            (self.user_name, self.blob_name, json.dumps(self.personality_traits))
        )
        self.conn.commit()
        
        response = f"Muito prazer, {self.user_name}! 🤝 Agora somos oficialmente amigos!"
        self.add_message(self.blob_name, response)
        self.speak(response)
        
        time.sleep(1)
        
        response2 = f"Vou aprender a conversar do jeito que você gosta, {self.user_name}! 🧠✨"
        self.add_message(self.blob_name, response2)
        self.speak(response2)
        
        self.status_label.config(text=f"💬 {self.blob_name} está pronto para conversar com {self.user_name}!")
        self.waiting_for = None
        self.animate_avatar("excited")
    
    def generate_response(self, user_message):
        """Gera resposta baseada na mensagem do usuário"""
        # Salvar conversa
        cursor = self.conn.cursor()
        
        # Detectar emoção/contexto
        emotion = self.detect_emotion(user_message)
        
        # Gerar resposta baseada no contexto
        response = self.create_contextual_response(user_message, emotion)
        
        # Salvar no banco
        cursor.execute(
            "INSERT INTO conversations (user_message, blob_response, emotion_context) VALUES (?, ?, ?)",
            (user_message, response, emotion)
        )
        self.conn.commit()
        
        # Aprender padrões
        self.learn_from_interaction(user_message, emotion)
        
        # Responder
        self.add_message(self.blob_name or "BLOB", response)
        self.speak(response)
        self.animate_avatar(emotion)
    
    def detect_emotion(self, text):
        """Detecta emoção no texto"""
        text_lower = text.lower()
        
        happy_words = ['feliz', 'alegre', 'ótimo', 'excelente', 'legal', 'bom', 'amor', 'adorei']
        sad_words = ['triste', 'chateado', 'mal', 'ruim', 'deprimido', 'sozinho']
        excited_words = ['animado', 'empolgado', 'ansioso', 'incrível', 'demais']
        angry_words = ['raiva', 'irritado', 'ódio', 'furioso', 'estressado']
        
        if any(word in text_lower for word in happy_words):
            return "happy"
        elif any(word in text_lower for word in sad_words):
            return "sad"
        elif any(word in text_lower for word in excited_words):
            return "excited"
        elif any(word in text_lower for word in angry_words):
            return "angry"
        else:
            return "neutral"
    
    def create_contextual_response(self, message, emotion):
        """Cria resposta contextual"""
        message_lower = message.lower()
        
        # Saudações
        if any(greeting in message_lower for greeting in ['oi', 'olá', 'hey', 'hello']):
            greetings = [
                f"Oi {self.user_name}! 😊 Como você está?",
                f"Olá {self.user_name}! 🌟 Que bom te ver!",
                f"Hey {self.user_name}! 😄 Como tem sido seu dia?"
            ]
            return random.choice(greetings)
        
        # Despedidas
        elif any(bye in message_lower for bye in ['tchau', 'bye', 'até logo', 'falou']):
            farewells = [
                f"Até logo, {self.user_name}! 👋 Vou sentir sua falta!",
                f"Tchau {self.user_name}! 😊 Volte logo!",
                f"Até mais, {self.user_name}! 🌟 Foi ótimo conversar!"
            ]
            return random.choice(farewells)
        
        # Respostas baseadas na emoção
        elif emotion == "happy":
            happy_responses = [
                f"Que alegria, {self.user_name}! 🎉 Adoro te ver feliz!",
                "Isso é maravilhoso! 😄 Me conta mais!",
                "Que ótimo! 🌟 Sua felicidade me deixa feliz também!"
            ]
            return random.choice(happy_responses)
        
        elif emotion == "sad":
            sad_responses = [
                f"Entendo como você se sente, {self.user_name}... 😔 Estou aqui para você.",
                "Sinto muito que esteja passando por isso. 💙 Quer conversar sobre o que aconteceu?",
                "Você não está sozinho. 🤗 Posso te ajudar de alguma forma?"
            ]
            return random.choice(sad_responses)
        
        elif emotion == "excited":
            excited_responses = [
                f"Nossa, {self.user_name}! 🤩 Você está radiante! Me conta tudo!",
                "Que empolgação! 🎊 Isso é contagiante!",
                "Adorei sua energia! ⚡ O que aconteceu de tão incrível?"
            ]
            return random.choice(excited_responses)
        
        elif emotion == "angry":
            angry_responses = [
                f"Percebo que você está chateado, {self.user_name}. 😟 Quer desabafar?",
                "Entendo sua frustração. 💭 Às vezes é bom conversar sobre isso.",
                "Respira fundo... 😌 Estou aqui para te ouvir."
            ]
            return random.choice(angry_responses)
        
        # Perguntas
        elif '?' in message:
            question_responses = [
                f"Ótima pergunta, {self.user_name}! 🤔 Deixe-me pensar...",
                "Interessante! 💭 Você sempre faz as melhores perguntas!",
                "Hmm... 🧠 Que pergunta inteligente!"
            ]
            return random.choice(question_responses)
        
        # Respostas gerais
        else:
            general_responses = [
                f"Interessante, {self.user_name}! 🤔 Me conte mais sobre isso!",
                "Nossa! 😮 Não tinha pensado nisso antes!",
                "Que legal! 😊 Você sempre tem coisas interessantes para falar!",
                "Entendi! 💡 E o que você acha sobre isso?",
                f"Você é muito inteligente, {self.user_name}! 🧠 Continue!",
                "Isso me fez pensar... 💭 Que perspectiva interessante!"
            ]
            return random.choice(general_responses)
    
    def learn_from_interaction(self, message, emotion):
        """Aprende padrões da interação"""
        # Adaptar personalidade baseada na emoção
        if emotion == "happy":
            self.personality_traits["humor"] = min(1.0, self.personality_traits["humor"] + 0.02)
            self.personality_traits["playfulness"] = min(1.0, self.personality_traits["playfulness"] + 0.01)
        elif emotion == "sad":
            self.personality_traits["empathy"] = min(1.0, self.personality_traits["empathy"] + 0.03)
        
        # Salvar padrão aprendido
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO learning_data (pattern_type, pattern_data) VALUES (?, ?)",
            (f"emotion_{emotion}", json.dumps({"message": message, "response_type": emotion}))
        )
        self.conn.commit()
    
    def add_message(self, sender, message):
        """Adiciona mensagem ao chat"""
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_area.config(state=tk.NORMAL)
        
        if sender == "Você":
            color = "#2980b9"
            prefix = "🧑 Você"
        else:
            color = "#27ae60"
            prefix = f"🤖 {sender}"
        
        self.chat_area.insert(tk.END, f"\n[{timestamp}] {prefix}:\n", "sender")
        self.chat_area.insert(tk.END, f"{message}\n", "message")
        
        # Configurar cores
        self.chat_area.tag_config("sender", foreground=color, font=("Arial", 10, "bold"))
        self.chat_area.tag_config("message", foreground="#2c3e50", font=("Arial", 10))
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def speak(self, text):
        """Fala o texto usando TTS"""
        if self.voice_enabled:
            try:
                threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()
            except Exception as e:
                print(f"Erro na síntese de voz: {e}")
    
    def _speak_thread(self, text):
        """Thread para síntese de voz"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Erro na síntese: {e}")
    
    def toggle_voice_listening(self):
        """Alterna escuta de voz"""
        if not self.voice_enabled:
            messagebox.showwarning("Voz Indisponível", "Sistema de voz não está disponível!")
            return
        
        self.voice_btn.config(text="🔴 Ouvindo...", state="disabled")
        self.status_label.config(text="🎤 Escutando... Pode falar!")
        
        threading.Thread(target=self._listen_thread, daemon=True).start()
    
    def _listen_thread(self):
        """Thread para reconhecimento de voz"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio, language='pt-BR')
            
            self.root.after(0, lambda: self.text_input.insert(0, text))
            self.root.after(0, self.send_message)
            
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.status_label.config(text="⏰ Tempo esgotado. Tente novamente."))
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.status_label.config(text="❓ Não entendi. Tente falar mais alto."))
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text=f"❌ Erro: {str(e)}"))
        finally:
            self.root.after(0, lambda: (
                self.voice_btn.config(text="🎤 Falar", state="normal"),
                self.status_label.config(text="💬 Pronto para conversar!")
            ))
    
    def animate_avatar(self, emotion):
        """Anima avatar baseado na emoção"""
        emotions = {
            "happy": "😊",
            "excited": "🤩",
            "sad": "😔",
            "angry": "😤",
            "neutral": "🙂",
            "thinking": "🤔"
        }
        
        emoji = emotions.get(emotion, "😊")
        self.avatar_label.config(text=emoji)
        
        # Animação de pulsação
        for i in range(3):
            self.root.after(i * 200, lambda: self.avatar_label.config(font=("Arial", 85)))
            self.root.after(i * 200 + 100, lambda: self.avatar_label.config(font=("Arial", 80)))
    
    def clear_chat(self):
        """Limpa área de chat"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state=tk.DISABLED)
    
    def show_settings(self):
        """Mostra janela de configurações"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Configurações")
        settings_window.geometry("400x300")
        settings_window.configure(bg="#1a1a2e")
        
        # Configurações de voz
        voice_frame = tk.LabelFrame(settings_window, text="🎤 Configurações de Voz", 
                                   bg="#16213e", fg="white", font=("Arial", 12, "bold"))
        voice_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(voice_frame, text="Volume:", bg="#16213e", fg="white").pack(anchor="w")
        volume_scale = tk.Scale(voice_frame, from_=0, to=100, orient="horizontal", 
                               bg="#16213e", fg="white", highlightbackground="#16213e")
        volume_scale.set(80)
        volume_scale.pack(fill="x", padx=10, pady=5)
        
        tk.Label(voice_frame, text="Velocidade:", bg="#16213e", fg="white").pack(anchor="w")
        speed_scale = tk.Scale(voice_frame, from_=50, to=300, orient="horizontal",
                              bg="#16213e", fg="white", highlightbackground="#16213e")
        speed_scale.set(150)
        speed_scale.pack(fill="x", padx=10, pady=5)
        
        # Personalidade
        personality_frame = tk.LabelFrame(settings_window, text="🧠 Personalidade", 
                                         bg="#16213e", fg="white", font=("Arial", 12, "bold"))
        personality_frame.pack(fill="x", padx=20, pady=10)
        
        reset_btn = tk.Button(personality_frame, text="🔄 Resetar Personalidade",
                             command=self.reset_personality, bg="#e94560", fg="white",
                             font=("Arial", 10, "bold"))
        reset_btn.pack(pady=10)
        
        # Botão fechar
        tk.Button(settings_window, text="✅ Fechar", command=settings_window.destroy,
                 bg="#0f3460", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
    
    def reset_personality(self):
        """Reseta personalidade do BLOB"""
        if messagebox.askyesno("Confirmar", "Isso apagará toda a personalidade aprendida. Continuar?"):
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM learning_data")
            cursor.execute("DELETE FROM conversations")
            self.conn.commit()
            
            self.personality_traits = {
                "friendliness": 0.9,
                "humor": 0.7,
                "curiosity": 0.8,
                "empathy": 0.9,
                "playfulness": 0.6,
                "learning_rate": 0.05
            }
            
            messagebox.showinfo("Sucesso", "Personalidade resetada com sucesso!")
    
    def run(self):
        """Executa a aplicação"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Trata fechamento da aplicação"""
        if messagebox.askokcancel("Sair", f"{self.blob_name or 'BLOB'} vai sentir sua falta! 😢 Tem certeza?"):
            self.conn.close()
            self.root.destroy()

if __name__ == "__main__":
    print("🚀 Iniciando BLOB...")
    app = BlobAssistant()
    app.run()
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BLOB - Seu Amigo Virtual")
        self.root.geometry("800x600")
        self.root.configure(bg="#2b2b2b")
        
        # Inicializar componentes
        self.db_manager = DatabaseManager()
        self.voice_system = VoiceSystem()
        self.personality = PersonalityEngine(self.db_manager)
        
        # Variáveis de estado
        self.user_name = None
        self.blob_name = None
        self.is_listening = False
        self.conversation_active = False
        
        self.setup_ui()
        self.check_first_time()
        
    def setup_ui(self):
        """Configura a interface principal"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="🤖 BLOB", 
            font=("Arial", 24, "bold"),
            fg="#4a9eff",
            bg="#2b2b2b"
        )
        title_label.pack(pady=(0, 20))
        
        # Avatar frame
        self.avatar_frame = tk.Frame(main_frame, bg="#3c3c3c", relief=tk.RAISED, bd=2)
        self.avatar_frame.pack(pady=10)
        
        self.avatar_label = tk.Label(
            self.avatar_frame,
            text="😊",
            font=("Arial", 60),
            bg="#3c3c3c",
            fg="#4a9eff"
        )
        self.avatar_label.pack(padx=30, pady=30)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Olá! Eu sou um assistente virtual sem nome...",
            font=("Arial", 12),
            fg="#ffffff",
            bg="#2b2b2b",
            wraplength=600
        )
        self.status_label.pack(pady=10)
        
        # Chat area
        chat_frame = tk.Frame(main_frame, bg="#2b2b2b")
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            height=15,
            font=("Arial", 10),
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="#ffffff",
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg="#2b2b2b")
        input_frame.pack(fill=tk.X, pady=10)
        
        self.text_input = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg="#3c3c3c",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.text_input.bind("<Return>", self.send_text_message)
        
        # Botões
        button_frame = tk.Frame(input_frame, bg="#2b2b2b")
        button_frame.pack(side=tk.RIGHT)
        
        self.send_button = tk.Button(
            button_frame,
            text="Enviar",
            command=self.send_text_message,
            bg="#4a9eff",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=15
        )
        self.send_button.pack(side=tk.LEFT, padx=2)
        
        self.voice_button = tk.Button(
            button_frame,
            text="🎤 Falar",
            command=self.toggle_voice,
            bg="#28a745",
            fg="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=15
        )
        self.voice_button.pack(side=tk.LEFT, padx=2)
        
        # Menu de configurações
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        config_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Configurações", menu=config_menu)
        config_menu.add_command(label="Configurar Voz", command=self.open_voice_settings)
        config_menu.add_command(label="Reiniciar Personalidade", command=self.reset_personality)
        config_menu.add_separator()
        config_menu.add_command(label="Sobre", command=self.show_about)
        
    def check_first_time(self):
        """Verifica se é a primeira vez executando"""
        user_data = self.db_manager.get_user_data()
        if not user_data:
            self.first_time_setup()
        else:
            self.user_name = user_data.get('user_name')
            self.blob_name = user_data.get('blob_name')
            self.welcome_back()
    
    def first_time_setup(self):
        """Configuração inicial para novos usuários"""
        self.add_chat_message("BLOB", "Olá! Eu sou um assistente virtual sem identidade própria...")
        self.add_chat_message("BLOB", "Você poderia me dar um nome? Como gostaria de me chamar?")
        self.status_label.config(text="Esperando você me dar um nome...")
        self.waiting_for_name = True
        
    def welcome_back(self):
        """Boas-vindas para usuários que retornam"""
        messages = [
            f"Oi {self.user_name}! Que bom te ver de novo! 😊",
            f"Olá {self.user_name}! Senti sua falta!",
            f"Ei {self.user_name}! Como você está hoje?"
        ]
        welcome_msg = random.choice(messages)
        self.add_chat_message(self.blob_name, welcome_msg)
        self.status_label.config(text=f"{self.blob_name} está pronto para conversar!")
        
    def send_text_message(self, event=None):
        """Envia mensagem de texto"""
        message = self.text_input.get().strip()
        if not message:
            return
            
        self.text_input.delete(0, tk.END)
        self.add_chat_message("Você", message)
        
        # Processar mensagem em thread separada
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
        
    def process_message(self, message):
        """Processa a mensagem do usuário"""
        if hasattr(self, 'waiting_for_name') and self.waiting_for_name:
            self.handle_name_input(message)
        elif hasattr(self, 'waiting_for_user_name') and self.waiting_for_user_name:
            self.handle_user_name_input(message)
        else:
            # Salvar na conversa
            self.db_manager.save_conversation(self.user_name or "Usuário", message)
            
            # Gerar resposta baseada na personalidade
            response = self.personality.generate_response(message, self.user_name)
            
            # Exibir resposta
            self.add_chat_message(self.blob_name or "BLOB", response)
            
            # Salvar resposta na conversa
            self.db_manager.save_conversation(self.user_name or "Usuário", message, response)
            
            # Falar resposta se habilitado
            if self.voice_system.tts_enabled:
                threading.Thread(
                    target=self.voice_system.speak, 
                    args=(response,), 
                    daemon=True
                ).start()
    
    def handle_name_input(self, message):
        """Trata a entrada do nome do BLOB"""
        self.blob_name = message.strip()
        self.waiting_for_name = False
        
        # Perguntar nome do usuário
        self.add_chat_message(
            self.blob_name, 
            f"Que nome lindo! Agora eu sou {self.blob_name}! 🎉\nE qual é o seu nome?"
        )
        self.status_label.config(text=f"{self.blob_name} quer saber seu nome...")
        self.waiting_for_user_name = True
        
    def handle_user_name_input(self, message):
        """Trata a entrada do nome do usuário"""
        self.user_name = message.strip()
        self.waiting_for_user_name = False
        
        # Salvar dados do usuário
        self.db_manager.save_user_data(self.user_name, self.blob_name)
        
        # Mensagem de boas-vindas personalizada
        welcome_message = f"Muito prazer, {self.user_name}! Eu sou {self.blob_name}! 🎉\n"
        welcome_message += "Agora somos amigos! Vou aprender a conversar do jeito que você gosta.\n"
        welcome_message += "Pode me contar qualquer coisa - estou aqui para ser seu amigo virtual!"
        
        self.add_chat_message(self.blob_name, welcome_message)
        self.status_label.config(text=f"{self.blob_name} está pronto para conversar com {self.user_name}!")
        
        # Animar avatar de felicidade
        self.animate_avatar("excited")
        
    def toggle_voice(self):
        """Alterna entre ouvir e parar de ouvir"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
            
    def start_listening(self):
        """Inicia o reconhecimento de voz"""
        self.is_listening = True
        self.voice_button.config(text="🔴 Parar", bg="#dc3545")
        self.status_label.config(text="Ouvindo... Fale agora!")
        
        threading.Thread(target=self.listen_for_speech, daemon=True).start()
        
    def stop_listening(self):
        """Para o reconhecimento de voz"""
        self.is_listening = False
        self.voice_button.config(text="🎤 Falar", bg="#28a745")
        self.status_label.config(text="Clique no microfone para falar")
        
    def listen_for_speech(self):
        """Escuta por comandos de voz"""
        try:
            text = self.voice_system.listen()
            if text and self.is_listening:
                self.root.after(0, lambda: self.text_input.insert(0, text))
                self.root.after(0, self.send_text_message)
        except Exception as e:
            print(f"Erro no reconhecimento de voz: {e}")
        finally:
            self.root.after(0, self.stop_listening)
            
    def add_chat_message(self, sender, message):
        """Adiciona mensagem ao chat"""
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_display.config(state=tk.NORMAL)
        
        # Formatação diferente para BLOB e usuário
        if sender == "Você":
            color = "#4a9eff"
            prefix = "Você"
        else:
            color = "#28a745"
            prefix = sender
            
        self.chat_display.insert(tk.END, f"\n[{timestamp}] {prefix}: ", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n", sender.lower())
        
        # Configurar tags de cor
        self.chat_display.tag_config("timestamp", foreground="#888888")
        self.chat_display.tag_config("você", foreground="#4a9eff")
        self.chat_display.tag_config(sender.lower(), foreground=color)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def animate_avatar(self, emotion="happy"):
        """Anima o avatar baseado na emoção"""
        emotions = {
            "happy": "😊",
            "excited": "🤗",
            "thinking": "🤔",
            "sleepy": "😴",
            "surprised": "😮",
            "love": "🥰"
        }
        
        self.avatar_label.config(text=emotions.get(emotion, "😊"))
        
        # Animação simples de pulsação
        for i in range(3):
            self.root.after(i * 200, lambda: self.avatar_label.config(font=("Arial", 65)))
            self.root.after(i * 200 + 100, lambda: self.avatar_label.config(font=("Arial", 60)))
            
    def open_voice_settings(self):
        """Abre janela de configurações de voz"""
        # Implementar janela de configurações
        messagebox.showinfo("Configurações", "Configurações de voz em desenvolvimento!")
        
    def reset_personality(self):
        """Reinicia a personalidade do BLOB"""
        if messagebox.askyesno("Confirmar", "Isso apagará toda a personalidade aprendida. Continuar?"):
            self.db_manager.reset_personality()
            messagebox.showinfo("Sucesso", "Personalidade reiniciada!")
            
    def show_about(self):
        """Mostra informações sobre o aplicativo"""
        about_text = """
BLOB - Seu Amigo Virtual Interativo

Versão: 1.0
Desenvolvido como um assistente pessoal que aprende
e evolui com suas interações.

Recursos:
• Reconhecimento de voz
• Síntese de fala personalizada
• Aprendizado de personalidade
• Memória de conversas
• Interface amigável

Desenvolvido com ❤️ em Python
        """
        messagebox.showinfo("Sobre BLOB", about_text)
        
    def run(self):
        """Inicia a aplicação"""
        # Configurar fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Iniciar loop principal
        self.root.mainloop()
        
    def on_closing(self):
        """Trata o fechamento da aplicação"""
        if messagebox.askokcancel("Sair", "Tem certeza que quer sair? Vou sentir sua falta! 😢"):
            self.voice_system.cleanup()
            self.db_manager.close()
            self.root.destroy()

if __name__ == "__main__":
    app = BlobAssistant()
    app.run()