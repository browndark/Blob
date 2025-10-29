using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace BLOB
{
    /// <summary>
    /// Script principal do BLOB - Assistente Virtual 3D
    /// Baseado no protótipo Python desenvolvido anteriormente
    /// </summary>
    public class BLOBController : MonoBehaviour
    {
        [Header("BLOB Configuration")]
        [SerializeField] private float baseSize = 1.0f;
        [SerializeField] private float animationSpeed = 1.0f;
        [SerializeField] private Transform bodyTransform;
        [SerializeField] private Transform[] armTransforms;
        [SerializeField] private Transform[] legTransforms;
        [SerializeField] private Transform[] eyeTransforms;
        [SerializeField] private Transform mouthTransform;

        [Header("Materials")]
        [SerializeField] private Material[] emotionMaterials;
        [SerializeField] private Renderer bodyRenderer;

        [Header("Audio")]
        [SerializeField] private AudioSource audioSource;
        [SerializeField] private AudioClip[] responseSounds;

        // Sistema de emoções
        public enum EmotionType
        {
            Neutral,
            Happy,
            Sad,
            Excited,
            Angry,
            Thinking,
            Speaking,
            Surprised
        }

        [Header("Current State")]
        [SerializeField] private EmotionType currentEmotion = EmotionType.Neutral;
        [SerializeField] private bool isAnimating = true;
        [SerializeField] private bool isSpeaking = false;

        // Variáveis de animação
        private float animationTime = 0f;
        private Vector3 baseScale;
        private Vector3 basePosition;
        private Coroutine currentEmotionCoroutine;

        // Componentes
        private VoiceSystem voiceSystem;
        private EmotionSystem emotionSystem;
        private AnimationSystem animationSystem;
        
        // Propriedades públicas para acesso dos outros sistemas
        public VoiceSystem VoiceSystem => voiceSystem;
        public EmotionSystem EmotionSystem => emotionSystem;
        public AnimationSystem AnimationSystem => animationSystem;

        void Start()
        {
            InitializeBLOB();
        }

        void Update()
        {
            if (isAnimating)
            {
                UpdateAnimation();
            }
        }

        /// <summary>
        /// Inicializa o BLOB e seus sistemas
        /// </summary>
        private void InitializeBLOB()
        {
            // Armazenar valores base
            baseScale = transform.localScale;
            basePosition = transform.position;

            // Inicializar sistemas
            voiceSystem = gameObject.AddComponent<VoiceSystem>();
            emotionSystem = gameObject.AddComponent<EmotionSystem>();
            animationSystem = gameObject.AddComponent<AnimationSystem>();

            // Configurar sistemas
            voiceSystem.Initialize(this);
            emotionSystem.Initialize(this, emotionMaterials);
            animationSystem.Initialize(this);

            // Definir emoção inicial
            SetEmotion(EmotionType.Neutral);

            Debug.Log("BLOB Initialized - Ready for interaction!");
        }

        /// <summary>
        /// Atualiza a animação base do BLOB
        /// </summary>
        private void UpdateAnimation()
        {
            animationTime += Time.deltaTime * animationSpeed;

            // Pulso suave baseado na emoção atual
            float pulseIntensity = GetPulseIntensity(currentEmotion);
            float pulse = 1f + (Mathf.Sin(animationTime) * 0.05f * pulseIntensity);
            
            // Aplicar escala
            transform.localScale = baseScale * pulse;

            // Movimento suave vertical
            float bobbing = Mathf.Sin(animationTime * 0.5f) * 0.02f;
            transform.position = basePosition + Vector3.up * bobbing;

            // Animar olhos (piscar ocasionalmente)
            if (Random.value < 0.002f) // 0.2% chance por frame
            {
                StartCoroutine(BlinkEyes());
            }
        }

        /// <summary>
        /// Define a emoção do BLOB
        /// </summary>
        public void SetEmotion(EmotionType emotion)
        {
            currentEmotion = emotion;
            
            // Parar animação anterior se existir
            if (currentEmotionCoroutine != null)
            {
                StopCoroutine(currentEmotionCoroutine);
            }

            // Iniciar nova animação de emoção
            currentEmotionCoroutine = StartCoroutine(AnimateEmotion(emotion));

            // Notificar sistemas
            emotionSystem?.OnEmotionChanged(emotion);
            animationSystem?.OnEmotionChanged(emotion);
        }

        /// <summary>
        /// Corrotina para animar mudança de emoção
        /// </summary>
        private IEnumerator AnimateEmotion(EmotionType emotion)
        {
            float duration = 0.5f;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                elapsed += Time.deltaTime;
                float progress = elapsed / duration;

                // Animação específica baseada na emoção
                switch (emotion)
                {
                    case EmotionType.Happy:
                        AnimateHappy(progress);
                        break;
                    case EmotionType.Sad:
                        AnimateSad(progress);
                        break;
                    case EmotionType.Excited:
                        AnimateExcited(progress);
                        break;
                    case EmotionType.Angry:
                        AnimateAngry(progress);
                        break;
                    case EmotionType.Surprised:
                        AnimateSurprised(progress);
                        break;
                }

                yield return null;
            }
        }

        /// <summary>
        /// Retorna a intensidade do pulso baseada na emoção
        /// </summary>
        private float GetPulseIntensity(EmotionType emotion)
        {
            switch (emotion)
            {
                case EmotionType.Excited: return 1.5f;
                case EmotionType.Happy: return 1.2f;
                case EmotionType.Surprised: return 1.4f;
                case EmotionType.Angry: return 1.1f;
                case EmotionType.Speaking: return 1.3f;
                case EmotionType.Sad: return 0.8f;
                case EmotionType.Thinking: return 0.9f;
                default: return 1.0f;
            }
        }

        /// <summary>
        /// Animação específica para felicidade
        /// </summary>
        private void AnimateHappy(float progress)
        {
            // Movimento de "salto" para cima
            float jump = Mathf.Sin(progress * Mathf.PI) * 0.1f;
            transform.position = basePosition + Vector3.up * jump;

            // Rotação suave
            float rotation = Mathf.Sin(progress * Mathf.PI * 2) * 5f;
            transform.rotation = Quaternion.Euler(0, rotation, 0);
        }

        /// <summary>
        /// Animação específica para tristeza
        /// </summary>
        private void AnimateSad(float progress)
        {
            // Movimento para baixo
            float drop = -progress * 0.05f;
            transform.position = basePosition + Vector3.up * drop;

            // Escala ligeiramente menor
            transform.localScale = baseScale * (1f - progress * 0.1f);
        }

        /// <summary>
        /// Animação específica para excitação
        /// </summary>
        private void AnimateExcited(float progress)
        {
            // Vibração rápida
            Vector3 shake = Random.insideUnitSphere * 0.02f * progress;
            transform.position = basePosition + shake;

            // Escala aumentando
            transform.localScale = baseScale * (1f + progress * 0.2f);
        }

        /// <summary>
        /// Animação específica para raiva
        /// </summary>
        private void AnimateAngry(float progress)
        {
            // Movimento lateral agressivo
            float sway = Mathf.Sin(progress * Mathf.PI * 8) * 0.03f;
            transform.position = basePosition + Vector3.right * sway;

            // Cor mais intensa (será controlada pelo EmotionSystem)
        }

        /// <summary>
        /// Animação específica para surpresa
        /// </summary>
        private void AnimateSurprised(float progress)
        {
            // Movimento rápido para cima
            float surprise = Mathf.Sin(progress * Mathf.PI) * 0.15f;
            transform.position = basePosition + Vector3.up * surprise;

            // Escala aumentando rapidamente
            float scale = 1f + Mathf.Sin(progress * Mathf.PI) * 0.3f;
            transform.localScale = baseScale * scale;
        }

        /// <summary>
        /// Corrotina para piscar os olhos
        /// </summary>
        private IEnumerator BlinkEyes()
        {
            // Fechar olhos
            foreach (Transform eye in eyeTransforms)
            {
                eye.localScale = new Vector3(eye.localScale.x, 0.1f, eye.localScale.z);
            }

            yield return new WaitForSeconds(0.1f);

            // Abrir olhos
            foreach (Transform eye in eyeTransforms)
            {
                eye.localScale = new Vector3(eye.localScale.x, 1f, eye.localScale.z);
            }
        }

        /// <summary>
        /// Método público para sistemas externos
        /// </summary>
        public void OnVoiceCommandReceived(string command)
        {
            Debug.Log($"BLOB received command: {command}");
            
            // Processar comando de voz
            ProcessVoiceCommand(command);
        }

        /// <summary>
        /// Processa comandos de voz
        /// </summary>
        private void ProcessVoiceCommand(string command)
        {
            command = command.ToLower();

            if (command.Contains("feliz") || command.Contains("happy"))
            {
                SetEmotion(EmotionType.Happy);
                Speak("Estou muito feliz!");
            }
            else if (command.Contains("triste") || command.Contains("sad"))
            {
                SetEmotion(EmotionType.Sad);
                Speak("Que pena... não fique triste!");
            }
            else if (command.Contains("animado") || command.Contains("excited"))
            {
                SetEmotion(EmotionType.Excited);
                Speak("Que energia incrível!");
            }
            else if (command.Contains("bravo") || command.Contains("angry"))
            {
                SetEmotion(EmotionType.Angry);
                Speak("Vamos respirar fundo juntos!");
            }
            else if (command.Contains("surpreso") || command.Contains("surprised"))
            {
                SetEmotion(EmotionType.Surprised);
                Speak("Nossa! Que surpresa!");
            }
            else if (command.Contains("pensando") || command.Contains("thinking"))
            {
                SetEmotion(EmotionType.Thinking);
                Speak("Deixe-me pensar sobre isso...");
            }
            else
            {
                SetEmotion(EmotionType.Speaking);
                Speak("Interessante! Me conte mais!");
            }
        }

        /// <summary>
        /// Faz o BLOB "falar"
        /// </summary>
        public void Speak(string text)
        {
            if (!isSpeaking)
            {
                StartCoroutine(SpeakCoroutine(text));
            }
        }

        /// <summary>
        /// Corrotina para fala
        /// </summary>
        private IEnumerator SpeakCoroutine(string text)
        {
            isSpeaking = true;
            SetEmotion(EmotionType.Speaking);

            // Reproduzir som (se disponível)
            if (audioSource && responseSounds.Length > 0)
            {
                AudioClip clip = responseSounds[Random.Range(0, responseSounds.Length)];
                audioSource.PlayOneShot(clip);
                yield return new WaitForSeconds(clip.length);
            }
            else
            {
                // Simular duração da fala baseada no texto
                float duration = text.Length * 0.05f;
                yield return new WaitForSeconds(duration);
            }

            isSpeaking = false;
            SetEmotion(EmotionType.Neutral);

            Debug.Log($"BLOB said: {text}");
        }

        /// <summary>
        /// Métodos públicos para interface
        /// </summary>
        public void SetHappy() => SetEmotion(EmotionType.Happy);
        public void SetSad() => SetEmotion(EmotionType.Sad);
        public void SetExcited() => SetEmotion(EmotionType.Excited);
        public void SetAngry() => SetEmotion(EmotionType.Angry);
        public void SetSurprised() => SetEmotion(EmotionType.Surprised);
        public void SetThinking() => SetEmotion(EmotionType.Thinking);
        public void SetNeutral() => SetEmotion(EmotionType.Neutral);

        /// <summary>
        /// Propriedades públicas
        /// </summary>
        public EmotionType CurrentEmotion => currentEmotion;
        public bool IsSpeaking => isSpeaking;
        public bool IsAnimating => isAnimating;

        /// <summary>
        /// Controle de animação
        /// </summary>
        public void StartAnimation() => isAnimating = true;
        public void StopAnimation() => isAnimating = false;
    }
}