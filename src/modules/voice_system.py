"""
Sistema de Voz - Reconhecimento e Síntese de Fala
"""

import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
from typing import Optional

class VoiceSystem:
    def __init__(self):
        # Inicializar reconhecedor de voz
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Inicializar TTS
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_available = True
            self.setup_tts()
        except Exception as e:
            print(f"Erro ao inicializar TTS: {e}")
            self.tts_available = False
            
        # Configurações
        self.tts_enabled = True
        self.voice_recognition_enabled = True
        self.speech_rate = 150
        self.speech_volume = 0.8
        
        # Calibração inicial do microfone
        self.calibrate_microphone()
        
        # Queue para fala
        self.speech_queue = queue.Queue()
        self.speech_thread = threading.Thread(target=self.speech_worker, daemon=True)
        self.speech_thread.start()
        
    def setup_tts(self):
        """Configura o engine de TTS"""
        if not self.tts_available:
            return
            
        # Configurar propriedades do TTS
        voices = self.tts_engine.getProperty('voices')
        
        # Tentar encontrar uma voz em português
        for voice in voices:
            if 'portuguese' in voice.name.lower() or 'brasil' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        else:
            # Se não encontrar, usar voz feminina se disponível
            for voice in voices:
                if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
                    
        # Configurar velocidade e volume
        self.tts_engine.setProperty('rate', self.speech_rate)
        self.tts_engine.setProperty('volume', self.speech_volume)
        
    def calibrate_microphone(self):
        """Calibra o microfone para o ambiente"""
        try:
            print("Calibrando microfone...")
            with self.microphone as source:
                # Ajustar para ruído ambiente
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
            # Configurações otimizadas
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.dynamic_energy_adjustment_damping = 0.15
            self.recognizer.dynamic_energy_ratio = 1.5
            self.recognizer.pause_threshold = 0.8
            self.recognizer.operation_timeout = None
            self.recognizer.phrase_threshold = 0.3
            self.recognizer.non_speaking_duration = 0.5
            
            print("Microfone calibrado!")
            
        except Exception as e:
            print(f"Erro na calibração do microfone: {e}")
            
    def listen(self, timeout: Optional[float] = 5) -> Optional[str]:
        """Escuta por fala e retorna o texto reconhecido"""
        if not self.voice_recognition_enabled:
            return None
            
        try:
            with self.microphone as source:
                print("Ouvindo...")
                
                # Escutar com timeout
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=10
                )
                
            print("Processando áudio...")
            
            # Tentar reconhecer em português primeiro
            try:
                text = self.recognizer.recognize_google(audio, language='pt-BR')
                print(f"Reconhecido (pt-BR): {text}")
                return text
                
            except sr.UnknownValueError:
                # Tentar em inglês como fallback
                try:
                    text = self.recognizer.recognize_google(audio, language='en-US')
                    print(f"Reconhecido (en-US): {text}")
                    return text
                except sr.UnknownValueError:
                    print("Não foi possível entender o áudio")
                    return None
                    
        except sr.RequestError as e:
            print(f"Erro na requisição do serviço de reconhecimento: {e}")
            return None
        except sr.WaitTimeoutError:
            print("Timeout - nenhuma fala detectada")
            return None
        except Exception as e:
            print(f"Erro no reconhecimento de voz: {e}")
            return None
            
    def speak(self, text: str, priority: bool = False):
        """Adiciona texto à fila de fala"""
        if self.tts_enabled and self.tts_available and text.strip():
            if priority:
                # Limpar fila e falar imediatamente
                with self.speech_queue.mutex:
                    self.speech_queue.queue.clear()
                    
            self.speech_queue.put(text)
            
    def speech_worker(self):
        """Worker thread para processar fila de fala"""
        while True:
            try:
                text = self.speech_queue.get(timeout=1)
                self._speak_now(text)
                self.speech_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Erro no worker de fala: {e}")
                
    def _speak_now(self, text: str):
        """Fala o texto imediatamente"""
        if not self.tts_available:
            return
            
        try:
            # Limpar texto para TTS
            clean_text = self.clean_text_for_tts(text)
            
            if clean_text:
                self.tts_engine.say(clean_text)
                self.tts_engine.runAndWait()
                
        except Exception as e:
            print(f"Erro ao falar: {e}")
            
    def clean_text_for_tts(self, text: str) -> str:
        """Limpa o texto para melhor síntese de fala"""
        # Remover emojis
        import re
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)
        text = emoji_pattern.sub('', text)
        
        # Substituições para melhor pronúncia
        replacements = {
            "😊": "sorrindo",
            "😄": "rindo",
            "😢": "triste",
            "❤️": "coração",
            "🤖": "robô",
            "👍": "legal",
            "🎉": "festa",
            "💡": "ideia",
            "🔥": "incrível",
            "⭐": "estrela",
            "rsrs": "risos",
            "kkkk": "risos",
            "haha": "risos",
            "hehe": "risos"
        }
        
        for emoji, replacement in replacements.items():
            text = text.replace(emoji, replacement)
            
        # Limpar caracteres especiais desnecessários
        text = re.sub(r'[^\w\s.,!?;:()-]', '', text)
        
        return text.strip()
        
    def get_available_voices(self) -> list:
        """Retorna lista de vozes disponíveis"""
        if not self.tts_available:
            return []
            
        voices = self.tts_engine.getProperty('voices')
        return [(voice.id, voice.name) for voice in voices]
        
    def set_voice(self, voice_id: str):
        """Define a voz a ser usada"""
        if self.tts_available:
            try:
                self.tts_engine.setProperty('voice', voice_id)
            except Exception as e:
                print(f"Erro ao definir voz: {e}")
                
    def set_speech_rate(self, rate: int):
        """Define a velocidade da fala (50-300)"""
        self.speech_rate = max(50, min(300, rate))
        if self.tts_available:
            self.tts_engine.setProperty('rate', self.speech_rate)
            
    def set_volume(self, volume: float):
        """Define o volume da fala (0.0-1.0)"""
        self.speech_volume = max(0.0, min(1.0, volume))
        if self.tts_available:
            self.tts_engine.setProperty('volume', self.speech_volume)
            
    def toggle_tts(self) -> bool:
        """Alterna TTS ligado/desligado"""
        self.tts_enabled = not self.tts_enabled
        return self.tts_enabled
        
    def toggle_voice_recognition(self) -> bool:
        """Alterna reconhecimento de voz ligado/desligado"""
        self.voice_recognition_enabled = not self.voice_recognition_enabled
        return self.voice_recognition_enabled
        
    def test_microphone(self) -> bool:
        """Testa se o microfone está funcionando"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            return True
        except Exception as e:
            print(f"Erro no teste do microfone: {e}")
            return False
            
    def test_speakers(self):
        """Testa se os alto-falantes estão funcionando"""
        self.speak("Teste de áudio. Se você está ouvindo isso, os alto-falantes estão funcionando!")
        
    def get_voice_settings(self) -> dict:
        """Retorna configurações atuais de voz"""
        return {
            "tts_enabled": self.tts_enabled,
            "voice_recognition_enabled": self.voice_recognition_enabled,
            "speech_rate": self.speech_rate,
            "speech_volume": self.speech_volume,
            "tts_available": self.tts_available,
            "current_voice": self.tts_engine.getProperty('voice') if self.tts_available else None
        }
        
    def save_settings(self, settings: dict):
        """Salva configurações de voz"""
        if "tts_enabled" in settings:
            self.tts_enabled = settings["tts_enabled"]
        if "voice_recognition_enabled" in settings:
            self.voice_recognition_enabled = settings["voice_recognition_enabled"]
        if "speech_rate" in settings:
            self.set_speech_rate(settings["speech_rate"])
        if "speech_volume" in settings:
            self.set_volume(settings["speech_volume"])
        if "voice_id" in settings:
            self.set_voice(settings["voice_id"])
            
    def cleanup(self):
        """Limpa recursos do sistema de voz"""
        try:
            if self.tts_available:
                self.tts_engine.stop()
        except Exception as e:
            print(f"Erro na limpeza do sistema de voz: {e}")
            
class VoiceTrainingSystem:
    """Sistema para treinar e adaptar o reconhecimento de voz"""
    
    def __init__(self, voice_system: VoiceSystem):
        self.voice_system = voice_system
        self.user_voice_patterns = {}
        self.pronunciation_corrections = {}
        
    def train_user_voice(self, training_phrases: list) -> dict:
        """Treina o sistema com a voz do usuário"""
        results = {
            "successful": [],
            "failed": [],
            "accuracy": 0.0
        }
        
        for phrase in training_phrases:
            print(f"Diga: '{phrase}'")
            recognized = self.voice_system.listen(timeout=10)
            
            if recognized:
                results["successful"].append({
                    "expected": phrase,
                    "recognized": recognized,
                    "accuracy": self.calculate_accuracy(phrase, recognized)
                })
            else:
                results["failed"].append(phrase)
                
        # Calcular precisão geral
        if results["successful"]:
            total_accuracy = sum(r["accuracy"] for r in results["successful"])
            results["accuracy"] = total_accuracy / len(results["successful"])
            
        return results
        
    def calculate_accuracy(self, expected: str, recognized: str) -> float:
        """Calcula a precisão entre texto esperado e reconhecido"""
        expected_words = expected.lower().split()
        recognized_words = recognized.lower().split()
        
        if not expected_words:
            return 0.0
            
        matches = 0
        for word in expected_words:
            if word in recognized_words:
                matches += 1
                
        return matches / len(expected_words)
        
    def adapt_to_accent(self, corrections: dict):
        """Adapta o sistema para o sotaque do usuário"""
        self.pronunciation_corrections.update(corrections)
        
    def get_suggested_phrases(self) -> list:
        """Retorna frases sugeridas para treinamento"""
        return [
            "Olá, como você está?",
            "Que horas são?",
            "Como está o tempo hoje?",
            "Pode me ajudar com isso?",
            "Obrigado pela ajuda",
            "Até logo, tchau!",
            "Bom dia, boa tarde, boa noite",
            "Sim, não, talvez",
            "Por favor, com licença",
            "Desculpe, não entendi"
        ]