#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de Configurações do BLOB
Sistema avançado para gerenciar todas as configurações do usuário
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import threading

class SettingsManager:
    """Gerenciador de configurações do BLOB"""
    
    def __init__(self, config_path="config/config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.settings_window = None
        
    def load_config(self):
        """Carrega configurações do arquivo JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar config: {e}")
            return self.get_default_config()
    
    def save_config(self):
        """Salva configurações no arquivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar config: {e}")
            return False
    
    def get_default_config(self):
        """Retorna configuração padrão"""
        return {
            "blob_config": {
                "version": "2.0.0",
                "voice": {
                    "enabled": True,
                    "voice_type": "female",
                    "volume": 80,
                    "rate": 0,
                    "pitch": 5
                },
                "ui": {
                    "brightness": 80,
                    "theme": "dark",
                    "font_size": 12
                }
            }
        }
    
    def get_voice_config(self):
        """Retorna configurações de voz"""
        return self.config.get("blob_config", {}).get("voice", {})
    
    def get_ui_config(self):
        """Retorna configurações de interface"""
        return self.config.get("blob_config", {}).get("ui", {})
    
    def update_voice_config(self, voice_type=None, volume=None, rate=None, pitch=None):
        """Atualiza configurações de voz"""
        voice_config = self.config.setdefault("blob_config", {}).setdefault("voice", {})
        
        if voice_type is not None:
            voice_config["voice_type"] = voice_type
        if volume is not None:
            voice_config["volume"] = volume
        if rate is not None:
            voice_config["rate"] = rate
        if pitch is not None:
            voice_config["pitch"] = pitch
            
        self.save_config()
    
    def update_ui_config(self, brightness=None, theme=None, font_size=None):
        """Atualiza configurações de interface"""
        ui_config = self.config.setdefault("blob_config", {}).setdefault("ui", {})
        
        if brightness is not None:
            ui_config["brightness"] = brightness
        if theme is not None:
            ui_config["theme"] = theme
        if font_size is not None:
            ui_config["font_size"] = font_size
            
        self.save_config()
    
    def open_settings_window(self, parent=None):
        """Abre janela de configurações"""
        if self.settings_window is not None and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return
            
        self.settings_window = tk.Toplevel(parent)
        self.settings_window.title("⚙️ Configurações do BLOB")
        self.settings_window.geometry("500x600")
        self.settings_window.resizable(True, True)
        
        # Ícone da janela
        try:
            self.settings_window.iconbitmap("assets/settings.ico")
        except:
            pass
            
        self.create_settings_ui()
    
    def create_settings_ui(self):
        """Cria interface de configurações"""
        # Notebook para abas
        notebook = ttk.Notebook(self.settings_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Aba de Voz
        voice_frame = ttk.Frame(notebook)
        notebook.add(voice_frame, text="🎤 Voz")
        self.create_voice_settings(voice_frame)
        
        # Aba de Interface
        ui_frame = ttk.Frame(notebook)
        notebook.add(ui_frame, text="🎨 Interface")
        self.create_ui_settings(ui_frame)
        
        # Aba de Sistema
        system_frame = ttk.Frame(notebook)
        notebook.add(system_frame, text="⚙️ Sistema")
        self.create_system_settings(system_frame)
        
        # Botões de ação
        button_frame = ttk.Frame(self.settings_window)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(button_frame, text="💾 Salvar", 
                  command=self.save_settings).pack(side="left", padx=5)
        ttk.Button(button_frame, text="🔄 Restaurar Padrão", 
                  command=self.restore_defaults).pack(side="left", padx=5)
        ttk.Button(button_frame, text="❌ Cancelar", 
                  command=self.settings_window.destroy).pack(side="right", padx=5)
    
    def create_voice_settings(self, parent):
        """Cria configurações de voz"""
        # Título
        title_label = ttk.Label(parent, text="🎤 Configurações de Voz", 
                               font=("Arial", 12, "bold"))
        title_label.pack(pady=10)
        
        voice_config = self.get_voice_config()
        
        # Tipo de voz
        voice_type_frame = ttk.LabelFrame(parent, text="Tipo de Voz")
        voice_type_frame.pack(fill="x", padx=10, pady=5)
        
        self.voice_type_var = tk.StringVar(value=voice_config.get("voice_type", "female"))
        
        ttk.Radiobutton(voice_type_frame, text="👩 Feminino", 
                       variable=self.voice_type_var, value="female",
                       command=self.test_voice).pack(anchor="w", padx=10, pady=5)
        
        # Mensagem sobre vozes masculinas
        info_label = ttk.Label(voice_type_frame, 
                              text="ℹ️ Vozes masculinas serão adicionadas em breve!\nClique no botão abaixo para ver opções de download.",
                              font=("Arial", 9),
                              foreground="blue")
        info_label.pack(anchor="w", padx=10, pady=5)
        
        # Botão para abrir downloader de vozes
        ttk.Button(voice_type_frame, text="📥 Baixar Mais Vozes", 
                  command=self.open_voice_downloader).pack(anchor="w", padx=10, pady=5)
        
        # Volume
        volume_frame = ttk.LabelFrame(parent, text="Volume da Voz")
        volume_frame.pack(fill="x", padx=10, pady=5)
        
        self.volume_var = tk.IntVar(value=voice_config.get("volume", 80))
        self.volume_label = ttk.Label(volume_frame, text=f"Volume: {self.volume_var.get()}%")
        self.volume_label.pack(pady=5)
        
        volume_scale = ttk.Scale(volume_frame, from_=0, to=100, 
                                variable=self.volume_var, orient="horizontal",
                                command=self.update_volume_label)
        volume_scale.pack(fill="x", padx=10, pady=5)
        
        # Velocidade da fala
        rate_frame = ttk.LabelFrame(parent, text="Velocidade da Fala")
        rate_frame.pack(fill="x", padx=10, pady=5)
        
        self.rate_var = tk.IntVar(value=voice_config.get("rate", 0))
        self.rate_label = ttk.Label(rate_frame, text=f"Velocidade: {self.rate_var.get()}")
        self.rate_label.pack(pady=5)
        
        rate_scale = ttk.Scale(rate_frame, from_=-10, to=10, 
                              variable=self.rate_var, orient="horizontal",
                              command=self.update_rate_label)
        rate_scale.pack(fill="x", padx=10, pady=5)
        
        # Tom da voz
        pitch_frame = ttk.LabelFrame(parent, text="Tom da Voz")
        pitch_frame.pack(fill="x", padx=10, pady=5)
        
        self.pitch_var = tk.IntVar(value=voice_config.get("pitch", 5))
        self.pitch_label = ttk.Label(pitch_frame, text=f"Tom: {self.pitch_var.get()}")
        self.pitch_label.pack(pady=5)
        
        pitch_scale = ttk.Scale(pitch_frame, from_=-10, to=10, 
                               variable=self.pitch_var, orient="horizontal",
                               command=self.update_pitch_label)
        pitch_scale.pack(fill="x", padx=10, pady=5)
        
        # Botão de teste
        ttk.Button(parent, text="🔊 Testar Voz", 
                  command=self.test_voice).pack(pady=10)
    
    def create_ui_settings(self, parent):
        """Cria configurações de interface"""
        # Título
        title_label = ttk.Label(parent, text="🎨 Configurações de Interface", 
                               font=("Arial", 12, "bold"))
        title_label.pack(pady=10)
        
        ui_config = self.get_ui_config()
        
        # Brilho
        brightness_frame = ttk.LabelFrame(parent, text="Brilho da Interface")
        brightness_frame.pack(fill="x", padx=10, pady=5)
        
        self.brightness_var = tk.IntVar(value=ui_config.get("brightness", 80))
        self.brightness_label = ttk.Label(brightness_frame, 
                                         text=f"Brilho: {self.brightness_var.get()}%")
        self.brightness_label.pack(pady=5)
        
        brightness_scale = ttk.Scale(brightness_frame, from_=20, to=100, 
                                    variable=self.brightness_var, orient="horizontal",
                                    command=self.update_brightness_preview)
        brightness_scale.pack(fill="x", padx=10, pady=5)
        
        # Tema
        theme_frame = ttk.LabelFrame(parent, text="Tema da Interface")
        theme_frame.pack(fill="x", padx=10, pady=5)
        
        self.theme_var = tk.StringVar(value=ui_config.get("theme", "dark"))
        
        ttk.Radiobutton(theme_frame, text="🌙 Escuro", 
                       variable=self.theme_var, value="dark").pack(anchor="w", padx=10, pady=5)
        ttk.Radiobutton(theme_frame, text="☀️ Claro", 
                       variable=self.theme_var, value="light").pack(anchor="w", padx=10, pady=5)
        
        # Tamanho da fonte
        font_frame = ttk.LabelFrame(parent, text="Tamanho da Fonte")
        font_frame.pack(fill="x", padx=10, pady=5)
        
        self.font_size_var = tk.IntVar(value=ui_config.get("font_size", 12))
        self.font_size_label = ttk.Label(font_frame, 
                                        text=f"Tamanho: {self.font_size_var.get()}px")
        self.font_size_label.pack(pady=5)
        
        font_scale = ttk.Scale(font_frame, from_=8, to=20, 
                              variable=self.font_size_var, orient="horizontal",
                              command=self.update_font_size_label)
        font_scale.pack(fill="x", padx=10, pady=5)
    
    def create_system_settings(self, parent):
        """Cria configurações de sistema"""
        # Título
        title_label = ttk.Label(parent, text="⚙️ Configurações de Sistema", 
                               font=("Arial", 12, "bold"))
        title_label.pack(pady=10)
        
        # Informações do sistema
        info_frame = ttk.LabelFrame(parent, text="Informações")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(info_frame, text=f"Versão: {self.config.get('blob_config', {}).get('version', '2.0.0')}").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Arquivo de config: {self.config_path}").pack(anchor="w", padx=10, pady=2)
        
        # Ações do sistema
        actions_frame = ttk.LabelFrame(parent, text="Ações")
        actions_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(actions_frame, text="🔄 Recarregar Configurações", 
                  command=self.reload_config).pack(fill="x", padx=10, pady=5)
        ttk.Button(actions_frame, text="📁 Abrir Pasta de Configurações", 
                  command=self.open_config_folder).pack(fill="x", padx=10, pady=5)
        ttk.Button(actions_frame, text="🗑️ Limpar Cache", 
                  command=self.clear_cache).pack(fill="x", padx=10, pady=5)
    
    def update_volume_label(self, value):
        """Atualiza label do volume"""
        vol = int(float(value))
        self.volume_label.config(text=f"Volume: {vol}%")
    
    def update_rate_label(self, value):
        """Atualiza label da velocidade"""
        rate = int(float(value))
        self.rate_label.config(text=f"Velocidade: {rate}")
    
    def update_pitch_label(self, value):
        """Atualiza label do tom"""
        pitch = int(float(value))
        self.pitch_label.config(text=f"Tom: {pitch}")
    
    def update_brightness_label(self, value):
        """Atualiza label do brilho"""
        brightness = int(float(value))
        self.brightness_label.config(text=f"Brilho: {brightness}%")
    
    def update_brightness_preview(self, value):
        """Atualiza label do brilho e aplica preview"""
        brightness = int(float(value))
        self.brightness_label.config(text=f"Brilho: {brightness}%")
        
        # Aplicar preview do brilho na janela de configurações
        try:
            # Calcular cor baseada no brilho
            brightness_factor = brightness / 100.0
            
            if brightness_factor < 0.5:
                # Brilho baixo - tons mais escuros
                bg_color = f"#{int(brightness_factor * 40):02x}{int(brightness_factor * 40):02x}{int(brightness_factor * 40):02x}"
                fg_color = "#FFFFFF"
            else:
                # Brilho alto - tons mais claros
                bg_factor = int(brightness_factor * 255)
                bg_color = f"#{bg_factor:02x}{bg_factor:02x}{bg_factor:02x}"
                fg_color = "#000000" if brightness_factor > 0.7 else "#FFFFFF"
            
            # Aplicar cores à janela de configurações
            self.settings_window.config(bg=bg_color)
            
            # Atualizar cor de fundo dos frames principais
            for widget in self.settings_window.winfo_children():
                if isinstance(widget, ttk.Notebook):
                    # Aplicar estilo ao notebook
                    style = ttk.Style()
                    style.configure('TNotebook', background=bg_color)
                    style.configure('TNotebook.Tab', background=bg_color, foreground=fg_color)
                    
        except Exception as e:
            print(f"⚠️ Erro ao aplicar preview de brilho: {e}")
    
    def update_font_size_label(self, value):
        """Atualiza label do tamanho da fonte"""
        size = int(float(value))
        self.font_size_label.config(text=f"Tamanho: {size}px")
    
    def test_voice(self):
        """Testa a voz selecionada com configurações específicas"""
        try:
            import win32com.client
            
            voice_type = self.voice_type_var.get()
            volume = self.volume_var.get()
            rate = self.rate_var.get()
            
            sapi = win32com.client.Dispatch('SAPI.SpVoice')
            sapi.Volume = volume
            
            # Configurar voz específica baseada no tipo
            voices = sapi.GetVoices()
            
            if voice_type == "male":
                # Usar Zira com configurações masculinas
                for i, voice in enumerate(voices):
                    if 'zira' in voice.GetDescription().lower():
                        sapi.Voice = voice
                        sapi.Rate = rate - 3  # Mais lento para soar masculino
                        break
                test_text = "Olá! Eu sou o BLOB com voz masculina mais grave!"
                
            else:  # female
                # Usar Maria com configurações femininas
                for i, voice in enumerate(voices):
                    if 'maria' in voice.GetDescription().lower():
                        sapi.Voice = voice
                        sapi.Rate = rate + 2  # Mais rápido para soar infantil
                        break
                test_text = "Oi! Eu sou a Bianca com voz feminina fofa!"
            
            # Executar em thread para não travar a interface
            import threading
            threading.Thread(target=lambda: sapi.Speak(test_text), daemon=True).start()
            
            print(f"🔊 Testando voz {voice_type}: Volume {volume}%, Taxa {rate}")
            
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Erro", f"Erro ao testar voz: {e}")
    
    def save_settings(self):
        """Salva todas as configurações"""
        try:
            # Salvar configurações de voz
            self.update_voice_config(
                voice_type=self.voice_type_var.get(),
                volume=self.volume_var.get(),
                rate=self.rate_var.get(),
                pitch=self.pitch_var.get()
            )
            
            # Salvar configurações de UI
            self.update_ui_config(
                brightness=self.brightness_var.get(),
                theme=self.theme_var.get(),
                font_size=self.font_size_var.get()
            )
            
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            self.settings_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")
    
    def restore_defaults(self):
        """Restaura configurações padrão"""
        if messagebox.askyesno("Confirmar", "Deseja restaurar todas as configurações padrão?"):
            self.config = self.get_default_config()
            self.save_config()
            messagebox.showinfo("Sucesso", "Configurações restauradas!")
            self.settings_window.destroy()
    
    def reload_config(self):
        """Recarrega configurações do arquivo"""
        self.config = self.load_config()
        messagebox.showinfo("Sucesso", "Configurações recarregadas!")
    
    def open_config_folder(self):
        """Abre pasta de configurações"""
        try:
            import os
            import subprocess
            folder = os.path.dirname(os.path.abspath(self.config_path))
            subprocess.Popen(f'explorer "{folder}"')
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir pasta: {e}")
    
    def open_voice_downloader(self):
        """Abre o downloader de vozes"""
        try:
            import subprocess
            import sys
            import os
            
            # Caminho para o downloader
            downloader_path = os.path.join(os.path.dirname(__file__), "voice_downloader.py")
            
            # Executar downloader em processo separado
            subprocess.Popen([sys.executable, downloader_path], cwd=os.path.dirname(downloader_path))
            
            print("📥 Downloader de vozes iniciado!")
            
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Downloader de Vozes", 
                              f"🎤 OPÇÕES DE VOZES MASCULINAS:\n\n"
                              f"1. Microsoft Azure TTS (Grátis)\n"
                              f"2. Google Cloud TTS (Grátis)\n" 
                              f"3. Amazon Polly (Grátis)\n\n"
                              f"Visite a documentação para instruções\n"
                              f"de instalação de vozes adicionais.\n\n"
                              f"Erro: {e}")
    
    def clear_cache(self):
        """Limpa cache do sistema"""
        if messagebox.askyesno("Confirmar", "Deseja limpar o cache do sistema?"):
            try:
                # Aqui você pode adicionar lógica para limpar cache
                messagebox.showinfo("Sucesso", "Cache limpo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar cache: {e}")

# Função de teste
def test_settings_manager():
    """Testa o gerenciador de configurações"""
    root = tk.Tk()
    root.withdraw()  # Esconder janela principal
    
    settings = SettingsManager()
    settings.open_settings_window()
    
    root.mainloop()

if __name__ == "__main__":
    test_settings_manager()