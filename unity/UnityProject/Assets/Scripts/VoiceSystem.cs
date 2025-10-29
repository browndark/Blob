using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace BLOB
{
    /// <summary>
    /// Sistema de reconhecimento de voz e síntese de fala para o BLOB
    /// Integração com Windows Speech API
    /// </summary>
    public class VoiceSystem : MonoBehaviour
    {
        [Header("Voice Settings")]
        [SerializeField] private bool enableVoiceRecognition = true;
        [SerializeField] private bool enableTextToSpeech = true;
        [SerializeField] private float speechVolume = 0.8f;
        [SerializeField] private int speechRate = 150;

        [Header("Recognition Settings")]
        [SerializeField] private float recognitionThreshold = 0.5f;
        [SerializeField] private string activationWord = "blob";
        [SerializeField] private bool continuousListening = true;

        [Header("Response Database")]
        [SerializeField] private VoiceResponse[] voiceResponses;

        private BLOBController blobController;
        private bool isListening = false;
        private bool isSpeaking = false;
        private AudioSource audioSource;

        // Dicionário de respostas organizadas por emoção
        private Dictionary<string, VoiceResponse> responseDatabase;

        [System.Serializable]
        public class VoiceResponse
        {
            public string keyword;
            public BLOBController.EmotionType emotionTrigger;
            public string[] responses;
            public AudioClip[] audioClips;
        }

        /// <summary>
        /// Inicializa o sistema de voz
        /// </summary>
        public void Initialize(BLOBController controller)
        {
            blobController = controller;
            audioSource = GetComponent<AudioSource>();
            
            if (audioSource == null)
            {
                audioSource = gameObject.AddComponent<AudioSource>();
            }

            // Configurar áudio
            audioSource.volume = speechVolume;
            audioSource.playOnAwake = false;

            // Construir banco de dados de respostas
            BuildResponseDatabase();

            // Inicializar reconhecimento de voz se habilitado
            if (enableVoiceRecognition)
            {
                InitializeVoiceRecognition();
            }

            Debug.Log("Voice System initialized successfully!");
        }

        /// <summary>
        /// Constrói o banco de dados de respostas
        /// </summary>
        private void BuildResponseDatabase()
        {
            responseDatabase = new Dictionary<string, VoiceResponse>();

            // Respostas padrão se não configuradas no inspector
            if (voiceResponses == null || voiceResponses.Length == 0)
            {
                voiceResponses = CreateDefaultResponses();
            }

            // Adicionar ao dicionário
            foreach (var response in voiceResponses)
            {
                if (!responseDatabase.ContainsKey(response.keyword.ToLower()))
                {
                    responseDatabase.Add(response.keyword.ToLower(), response);
                }
            }
        }

        /// <summary>
        /// Cria respostas padrão
        /// </summary>
        private VoiceResponse[] CreateDefaultResponses()
        {
            return new VoiceResponse[]
            {
                new VoiceResponse
                {
                    keyword = "feliz",
                    emotionTrigger = BLOBController.EmotionType.Happy,
                    responses = new[] { "Que alegria! Estou muito feliz também!", "Eba! Adoro quando você está feliz!", "Sua felicidade me deixa radiante!" }
                },
                new VoiceResponse
                {
                    keyword = "triste",
                    emotionTrigger = BLOBController.EmotionType.Sad,
                    responses = new[] { "Não fique triste! Estou aqui para te animar!", "Que pena... vamos encontrar algo para te alegrar!", "Tudo vai ficar bem, eu acredito!" }
                },
                new VoiceResponse
                {
                    keyword = "animado",
                    emotionTrigger = BLOBController.EmotionType.Excited,
                    responses = new[] { "Uau! Que energia incrível!", "Estou super animado também!", "Vamos celebrar essa energia!" }
                },
                new VoiceResponse
                {
                    keyword = "bravo",
                    emotionTrigger = BLOBController.EmotionType.Angry,
                    responses = new[] { "Vamos respirar fundo juntos!", "Calma, tudo vai dar certo!", "Que tal relaxarmos um pouco?" }
                },
                new VoiceResponse
                {
                    keyword = "surpreso",
                    emotionTrigger = BLOBController.EmotionType.Surprised,
                    responses = new[] { "Nossa! Que surpresa incrível!", "Uau! Não esperava por isso!", "Que coisa mais surpreendente!" }
                },
                new VoiceResponse
                {
                    keyword = "pensando",
                    emotionTrigger = BLOBController.EmotionType.Thinking,
                    responses = new[] { "Hmm, deixe-me pensar sobre isso...", "Interessante... preciso refletir!", "Que pergunta complexa!" }
                },
                new VoiceResponse
                {
                    keyword = "oi",
                    emotionTrigger = BLOBController.EmotionType.Happy,
                    responses = new[] { "Oi! Como você está hoje?", "Olá! É muito bom te ver!", "Oi! Estava esperando por você!" }
                },
                new VoiceResponse
                {
                    keyword = "tchau",
                    emotionTrigger = BLOBController.EmotionType.Neutral,
                    responses = new[] { "Tchau! Foi ótimo conversar com você!", "Até logo! Volte sempre!", "Tchau! Mal posso esperar para te ver novamente!" }
                }
            };
        }

        /// <summary>
        /// Inicializa o reconhecimento de voz
        /// </summary>
        private void InitializeVoiceRecognition()
        {
            if (continuousListening)
            {
                StartListening();
            }
        }

        /// <summary>
        /// Inicia a escuta contínua
        /// </summary>
        public void StartListening()
        {
            if (!isListening && enableVoiceRecognition)
            {
                isListening = true;
                StartCoroutine(ContinuousListening());
                Debug.Log("Voice recognition started - say '" + activationWord + "' + command");
            }
        }

        /// <summary>
        /// Para a escuta
        /// </summary>
        public void StopListening()
        {
            isListening = false;
            Debug.Log("Voice recognition stopped");
        }

        /// <summary>
        /// Corrotina para escuta contínua
        /// </summary>
        private IEnumerator ContinuousListening()
        {
            while (isListening)
            {
                if (!isSpeaking)
                {
                    // Simular detecção de voz (em implementação real, usaria Windows Speech API)
                    yield return StartCoroutine(SimulateVoiceDetection());
                }
                
                yield return new WaitForSeconds(0.1f);
            }
        }

        /// <summary>
        /// Simula detecção de voz para demonstração
        /// TODO: Integrar com Windows Speech Recognition API
        /// </summary>
        private IEnumerator SimulateVoiceDetection()
        {
            // Esta é uma simulação - na implementação real seria substituída por:
            // - Windows.Speech.Recognition (UWP)
            // - Unity.Services.CloudCode com Google Speech API
            // - Plugin nativo para Windows Speech API
            
            yield return new WaitForSeconds(1f);
            
            // Simulação aleatória para demonstração
            if (Random.value < 0.01f) // 1% chance por verificação
            {
                string[] simulatedCommands = { "feliz", "triste", "animado", "oi", "surpreso" };
                string command = activationWord + " " + simulatedCommands[Random.Range(0, simulatedCommands.Length)];
                ProcessVoiceInput(command);
            }
        }

        /// <summary>
        /// Processa entrada de voz detectada
        /// </summary>
        public void ProcessVoiceInput(string input)
        {
            if (string.IsNullOrEmpty(input))
                return;

            input = input.ToLower().Trim();
            
            // Verificar se contém palavra de ativação
            if (!input.Contains(activationWord.ToLower()))
                return;

            // Remover palavra de ativação
            string command = input.Replace(activationWord.ToLower(), "").Trim();
            
            Debug.Log($"Voice command received: {command}");
            
            // Procurar resposta apropriada
            ProcessCommand(command);
        }

        /// <summary>
        /// Processa comando reconhecido
        /// </summary>
        private void ProcessCommand(string command)
        {
            VoiceResponse response = null;
            
            // Procurar palavra-chave exata
            foreach (var kvp in responseDatabase)
            {
                if (command.Contains(kvp.Key))
                {
                    response = kvp.Value;
                    break;
                }
            }

            // Se não encontrou resposta específica, usar resposta padrão
            if (response == null)
            {
                response = new VoiceResponse
                {
                    keyword = "default",
                    emotionTrigger = BLOBController.EmotionType.Speaking,
                    responses = new[] { "Interessante! Me conte mais sobre isso!", "Não entendi bem, mas adorei ouvir você!", "Que legal! Continue falando!" }
                };
            }

            // Executar resposta
            ExecuteResponse(response);
        }

        /// <summary>
        /// Executa a resposta encontrada
        /// </summary>
        private void ExecuteResponse(VoiceResponse response)
        {
            // Mudar emoção do BLOB
            blobController.SetEmotion(response.emotionTrigger);

            // Escolher resposta aleatória
            string textResponse = response.responses[Random.Range(0, response.responses.Length)];

            // Falar resposta
            StartCoroutine(SpeakResponse(textResponse, response.audioClips));
        }

        /// <summary>
        /// Corrotina para falar resposta
        /// </summary>
        private IEnumerator SpeakResponse(string text, AudioClip[] audioClips)
        {
            isSpeaking = true;
            blobController.SetEmotion(BLOBController.EmotionType.Speaking);

            if (enableTextToSpeech)
            {
                // Se há clipes de áudio, tocar um aleatório
                if (audioClips != null && audioClips.Length > 0)
                {
                    AudioClip clip = audioClips[Random.Range(0, audioClips.Length)];
                    audioSource.PlayOneShot(clip);
                    yield return new WaitForSeconds(clip.length);
                }
                else
                {
                    // Simular duração da fala baseada no comprimento do texto
                    float duration = Mathf.Max(1f, text.Length * 0.05f);
                    
                    // TODO: Integrar com Windows Speech Synthesis API
                    // System.Speech.Synthesis.SpeechSynthesizer (Windows)
                    
                    yield return new WaitForSeconds(duration);
                }
            }

            Debug.Log($"BLOB said: {text}");
            
            isSpeaking = false;
            blobController.SetEmotion(BLOBController.EmotionType.Neutral);
        }

        /// <summary>
        /// Método público para falar texto específico
        /// </summary>
        public void Speak(string text)
        {
            if (!isSpeaking)
            {
                StartCoroutine(SpeakResponse(text, null));
            }
        }

        /// <summary>
        /// Método para teste manual de comandos
        /// </summary>
        [ContextMenu("Test Voice Command")]
        public void TestVoiceCommand()
        {
            string[] testCommands = { "blob feliz", "blob triste", "blob animado", "blob oi" };
            string command = testCommands[Random.Range(0, testCommands.Length)];
            ProcessVoiceInput(command);
        }

        /// <summary>
        /// Propriedades públicas
        /// </summary>
        public bool IsListening => isListening;
        public bool IsSpeaking => isSpeaking;
        public bool VoiceRecognitionEnabled => enableVoiceRecognition;
        public bool TextToSpeechEnabled => enableTextToSpeech;

        /// <summary>
        /// Métodos de configuração
        /// </summary>
        public void SetActivationWord(string word) => activationWord = word;
        public void SetSpeechVolume(float volume) 
        { 
            speechVolume = Mathf.Clamp01(volume);
            if (audioSource != null)
                audioSource.volume = speechVolume;
        }
        public void SetSpeechRate(int rate) => speechRate = Mathf.Clamp(rate, 50, 300);

        /// <summary>
        /// Controles de sistema
        /// </summary>
        public void EnableVoiceRecognition() 
        { 
            enableVoiceRecognition = true;
            if (!isListening) StartListening();
        }
        
        public void DisableVoiceRecognition() 
        { 
            enableVoiceRecognition = false;
            StopListening();
        }
        
        public void EnableTextToSpeech() => enableTextToSpeech = true;
        public void DisableTextToSpeech() => enableTextToSpeech = false;
    }
}