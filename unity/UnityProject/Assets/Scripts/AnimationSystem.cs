using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace BLOB
{
    /// <summary>
    /// Sistema de animações procedurais para o BLOB
    /// Controla movimentos, deformações e efeitos visuais
    /// </summary>
    public class AnimationSystem : MonoBehaviour
    {
        [Header("Animation Settings")]
        [SerializeField] private float animationSpeed = 1f;
        [SerializeField] private float intensityMultiplier = 1f;
        [SerializeField] private bool enablePhysicsAnimation = true;
        [SerializeField] private bool enableIdleAnimation = true;

        [Header("Bounce Settings")]
        [SerializeField] private float bounceHeight = 0.5f;
        [SerializeField] private float bounceSpeed = 2f;
        [SerializeField] private AnimationCurve bounceCurve = AnimationCurve.EaseInOut(0, 0, 1, 1);

        [Header("Deformation Settings")]
        [SerializeField] private float maxDeformation = 0.3f;
        [SerializeField] private float deformationSpeed = 3f;
        [SerializeField] private float elasticity = 0.8f;

        [Header("Rotation Settings")]
        [SerializeField] private float rotationSpeed = 45f;
        [SerializeField] private float maxRotation = 15f;
        [SerializeField] private bool enableWobble = true;

        [Header("Scale Animation")]
        [SerializeField] private float scaleVariation = 0.1f;
        [SerializeField] private float scaleSpeed = 1.5f;
        [SerializeField] private Vector3 baseScale = Vector3.one;

        private BLOBController blobController;
        private Transform blobTransform;
        private Vector3 originalPosition;
        private Vector3 originalScale;
        private Quaternion originalRotation;

        // Estado da animação
        private bool isAnimating = false;
        private BLOBController.EmotionType currentEmotion = BLOBController.EmotionType.Neutral;
        private Coroutine currentAnimationCoroutine;
        private Coroutine idleAnimationCoroutine;

        // Componentes para animação
        private Renderer blobRenderer;
        private MaterialPropertyBlock materialPropertyBlock;

        /// <summary>
        /// Inicializa o sistema de animações
        /// </summary>
        public void Initialize(BLOBController controller)
        {
            blobController = controller;
            blobTransform = transform;
            blobRenderer = GetComponent<Renderer>();

            // Salvar estados originais
            originalPosition = blobTransform.position;
            originalScale = blobTransform.localScale;
            originalRotation = blobTransform.rotation;
            baseScale = originalScale;

            // Configurar material property block
            materialPropertyBlock = new MaterialPropertyBlock();

            // Iniciar animação idle se habilitada
            if (enableIdleAnimation)
            {
                StartIdleAnimation();
            }

            Debug.Log("Animation System initialized successfully!");
        }

        /// <summary>
        /// Inicia animação baseada na emoção
        /// </summary>
        public void PlayEmotionAnimation(BLOBController.EmotionType emotion)
        {
            currentEmotion = emotion;

            // Parar animação atual se existir
            if (currentAnimationCoroutine != null)
            {
                StopCoroutine(currentAnimationCoroutine);
            }

            // Iniciar nova animação baseada na emoção
            switch (emotion)
            {
                case BLOBController.EmotionType.Happy:
                    currentAnimationCoroutine = StartCoroutine(HappyAnimation());
                    break;
                case BLOBController.EmotionType.Sad:
                    currentAnimationCoroutine = StartCoroutine(SadAnimation());
                    break;
                case BLOBController.EmotionType.Excited:
                    currentAnimationCoroutine = StartCoroutine(ExcitedAnimation());
                    break;
                case BLOBController.EmotionType.Angry:
                    currentAnimationCoroutine = StartCoroutine(AngryAnimation());
                    break;
                case BLOBController.EmotionType.Surprised:
                    currentAnimationCoroutine = StartCoroutine(SurprisedAnimation());
                    break;
                case BLOBController.EmotionType.Thinking:
                    currentAnimationCoroutine = StartCoroutine(ThinkingAnimation());
                    break;
                case BLOBController.EmotionType.Speaking:
                    currentAnimationCoroutine = StartCoroutine(SpeakingAnimation());
                    break;
                default:
                    currentAnimationCoroutine = StartCoroutine(NeutralAnimation());
                    break;
            }
        }

        /// <summary>
        /// Animação de felicidade - pulos alegres
        /// </summary>
        private IEnumerator HappyAnimation()
        {
            isAnimating = true;
            float duration = 2f;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                float progress = elapsed / duration;
                
                // Pulos repetidos
                float bounceOffset = Mathf.Sin(progress * Mathf.PI * 4) * bounceHeight * intensityMultiplier;
                Vector3 targetPosition = originalPosition + Vector3.up * bounceOffset;

                // Rotação suave
                float rotationOffset = Mathf.Sin(progress * Mathf.PI * 8) * 10f;
                Quaternion targetRotation = originalRotation * Quaternion.Euler(0, 0, rotationOffset);

                // Escala pulsante
                float scaleOffset = 1f + Mathf.Sin(progress * Mathf.PI * 6) * 0.1f;
                Vector3 targetScale = baseScale * scaleOffset;

                // Aplicar transformações
                blobTransform.position = Vector3.Lerp(blobTransform.position, targetPosition, Time.deltaTime * animationSpeed * 5f);
                blobTransform.rotation = Quaternion.Lerp(blobTransform.rotation, targetRotation, Time.deltaTime * animationSpeed * 3f);
                blobTransform.localScale = Vector3.Lerp(blobTransform.localScale, targetScale, Time.deltaTime * animationSpeed * 4f);

                elapsed += Time.deltaTime;
                yield return null;
            }

            isAnimating = false;
            ReturnToNeutral();
        }

        /// <summary>
        /// Animação de tristeza - movimento lento para baixo
        /// </summary>
        private IEnumerator SadAnimation()
        {
            isAnimating = true;
            float duration = 3f;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                float progress = elapsed / duration;
                
                // Movimento lento para baixo
                float sadOffset = -Mathf.Sin(progress * Mathf.PI) * 0.3f * intensityMultiplier;
                Vector3 targetPosition = originalPosition + Vector3.up * sadOffset;

                // Escala diminuindo
                float scaleOffset = 1f - Mathf.Sin(progress * Mathf.PI) * 0.15f;
                Vector3 targetScale = baseScale * scaleOffset;

                // Rotação lenta
                float rotationOffset = Mathf.Sin(progress * Mathf.PI * 2) * 5f;
                Quaternion targetRotation = originalRotation * Quaternion.Euler(0, 0, rotationOffset);

                // Aplicar transformações
                blobTransform.position = Vector3.Lerp(blobTransform.position, targetPosition, Time.deltaTime * animationSpeed * 2f);
                blobTransform.localScale = Vector3.Lerp(blobTransform.localScale, targetScale, Time.deltaTime * animationSpeed * 2f);
                blobTransform.rotation = Quaternion.Lerp(blobTransform.rotation, targetRotation, Time.deltaTime * animationSpeed * 1f);

                elapsed += Time.deltaTime;
                yield return null;
            }

            isAnimating = false;
            ReturnToNeutral();
        }

        /// <summary>
        /// Animação de excitação - movimento rápido e intenso
        /// </summary>
        private IEnumerator ExcitedAnimation()
        {
            isAnimating = true;
            float duration = 2.5f;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                float progress = elapsed / duration;
                
                // Movimento rápido e errático
                float xOffset = Mathf.Sin(progress * Mathf.PI * 12) * 0.2f * intensityMultiplier;
                float yOffset = Mathf.Abs(Mathf.Sin(progress * Mathf.PI * 8)) * 0.4f * intensityMultiplier;
                Vector3 targetPosition = originalPosition + new Vector3(xOffset, yOffset, 0);

                // Rotação rápida
                float rotationOffset = Mathf.Sin(progress * Mathf.PI * 16) * 20f;
                Quaternion targetRotation = originalRotation * Quaternion.Euler(0, 0, rotationOffset);

                // Escala variável
                float scaleOffset = 1f + Mathf.Sin(progress * Mathf.PI * 10) * 0.2f;
                Vector3 targetScale = baseScale * scaleOffset;

                // Aplicar transformações
                blobTransform.position = Vector3.Lerp(blobTransform.position, targetPosition, Time.deltaTime * animationSpeed * 8f);
                blobTransform.rotation = Quaternion.Lerp(blobTransform.rotation, targetRotation, Time.deltaTime * animationSpeed * 6f);
                blobTransform.localScale = Vector3.Lerp(blobTransform.localScale, targetScale, Time.deltaTime * animationSpeed * 5f);

                elapsed += Time.deltaTime;
                yield return null;
            }

            isAnimating = false;
            ReturnToNeutral();
        }

        /// <summary>
        /// Animação de raiva - tremor intenso
        /// </summary>
        private IEnumerator AngryAnimation()
        {
            isAnimating = true;
            float duration = 2f;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                float progress = elapsed / duration;
                
                // Tremor intenso
                float xShake = Random.Range(-0.1f, 0.1f) * intensityMultiplier;
                float yShake = Random.Range(-0.05f, 0.05f) * intensityMultiplier;
                Vector3 targetPosition = originalPosition + new Vector3(xShake, yShake, 0);

                // Rotação tremula
                float rotationShake = Random.Range(-15f, 15f);
                Quaternion targetRotation = originalRotation * Quaternion.Euler(0, 0, rotationShake);

                // Escala aumentada
                float scaleOffset = 1f + Mathf.Sin(progress * Mathf.PI * 3) * 0.15f;
                Vector3 targetScale = baseScale * scaleOffset;

                // Aplicar transformações
                blobTransform.position = targetPosition;
                blobTransform.rotation = Quaternion.Lerp(blobTransform.rotation, targetRotation, Time.deltaTime * animationSpeed * 10f);
                blobTransform.localScale = Vector3.Lerp(blobTransform.localScale, targetScale, Time.deltaTime * animationSpeed * 3f);

                elapsed += Time.deltaTime;
                yield return null;
            }

            isAnimating = false;
            ReturnToNeutral();
        }

        /// <summary>
        /// Animação de surpresa - expansão súbita
        /// </summary>
        private IEnumerator SurprisedAnimation()
        {
            isAnimating = true;
            
            // Fase 1: Expansão rápida
            float expandDuration = 0.3f;
            float elapsed = 0f;

            while (elapsed < expandDuration)
            {
                float progress = elapsed / expandDuration;
                float scaleOffset = 1f + Mathf.Lerp(0f, 0.4f, progress) * intensityMultiplier;
                Vector3 targetScale = baseScale * scaleOffset;

                blobTransform.localScale = Vector3.Lerp(blobTransform.localScale, targetScale, Time.deltaTime * animationSpeed * 8f);

                elapsed += Time.deltaTime;
                yield return null;
            }

            // Fase 2: Vibração
            float vibrationDuration = 1f;
            elapsed = 0f;

            while (elapsed < vibrationDuration)
            {
                float progress = elapsed / vibrationDuration;
                
                float xVibration = Mathf.Sin(progress * Mathf.PI * 20) * 0.05f * intensityMultiplier;
                float yVibration = Mathf.Sin(progress * Mathf.PI * 25) * 0.03f * intensityMultiplier;
                Vector3 targetPosition = originalPosition + new Vector3(xVibration, yVibration, 0);

                blobTransform.position = Vector3.Lerp(blobTransform.position, targetPosition, Time.deltaTime * animationSpeed * 6f);

                elapsed += Time.deltaTime;
                yield return null;
            }

            isAnimating = false;
            ReturnToNeutral();
        }

        /// <summary>
        /// Animação de pensamento - movimento circular suave
        /// </summary>
        private IEnumerator ThinkingAnimation()
        {
            isAnimating = true;
            float duration = 4f;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                float progress = elapsed / duration;
                
                // Movimento circular suave
                float angle = progress * Mathf.PI * 2;
                float radius = 0.1f * intensityMultiplier;
                float xOffset = Mathf.Cos(angle) * radius;
                float yOffset = Mathf.Sin(angle * 0.5f) * radius * 0.5f;
                Vector3 targetPosition = originalPosition + new Vector3(xOffset, yOffset, 0);

                // Rotação lenta
                float rotationOffset = progress * 360f * 0.25f;
                Quaternion targetRotation = originalRotation * Quaternion.Euler(0, 0, rotationOffset);

                // Escala pulsante lenta
                float scaleOffset = 1f + Mathf.Sin(progress * Mathf.PI * 3) * 0.05f;
                Vector3 targetScale = baseScale * scaleOffset;

                // Aplicar transformações
                blobTransform.position = Vector3.Lerp(blobTransform.position, targetPosition, Time.deltaTime * animationSpeed * 2f);
                blobTransform.rotation = Quaternion.Lerp(blobTransform.rotation, targetRotation, Time.deltaTime * animationSpeed * 1f);
                blobTransform.localScale = Vector3.Lerp(blobTransform.localScale, targetScale, Time.deltaTime * animationSpeed * 2f);

                elapsed += Time.deltaTime;
                yield return null;
            }

            isAnimating = false;
            ReturnToNeutral();
        }

        /// <summary>
        /// Animação de fala - movimento rítmico
        /// </summary>
        private IEnumerator SpeakingAnimation()
        {
            isAnimating = true;
            float duration = 3f; // Será interrompida quando a fala terminar
            float elapsed = 0f;
            
            // Verificar se o sistema de voz está falando
            bool isSpeaking = blobController.VoiceSystem != null && blobController.VoiceSystem.IsSpeaking;

            while (elapsed < duration && isSpeaking)
            {
                float progress = elapsed / duration;
                
                // Movimento rítmico da fala
                float speechOffset = Mathf.Sin(progress * Mathf.PI * 15) * 0.05f * intensityMultiplier;
                Vector3 targetPosition = originalPosition + Vector3.up * speechOffset;

                // Escala pulsante rápida
                float scaleOffset = 1f + Mathf.Sin(progress * Mathf.PI * 12) * 0.08f;
                Vector3 targetScale = baseScale * scaleOffset;

                // Rotação suave
                float rotationOffset = Mathf.Sin(progress * Mathf.PI * 6) * 3f;
                Quaternion targetRotation = originalRotation * Quaternion.Euler(0, 0, rotationOffset);

                // Aplicar transformações
                blobTransform.position = Vector3.Lerp(blobTransform.position, targetPosition, Time.deltaTime * animationSpeed * 6f);
                blobTransform.localScale = Vector3.Lerp(blobTransform.localScale, targetScale, Time.deltaTime * animationSpeed * 8f);
                blobTransform.rotation = Quaternion.Lerp(blobTransform.rotation, targetRotation, Time.deltaTime * animationSpeed * 4f);

                elapsed += Time.deltaTime;
                
                // Atualizar estado de fala periodicamente
                if (elapsed % 0.1f < Time.deltaTime)
                {
                    isSpeaking = blobController.VoiceSystem != null && blobController.VoiceSystem.IsSpeaking;
                }
                
                yield return null;
            }

            isAnimating = false;
            ReturnToNeutral();
        }

        /// <summary>
        /// Animação neutra/padrão
        /// </summary>
        private IEnumerator NeutralAnimation()
        {
            isAnimating = true;
            yield return StartCoroutine(ReturnToNeutralCoroutine());
            isAnimating = false;
        }

        /// <summary>
        /// Animação idle contínua
        /// </summary>
        private void StartIdleAnimation()
        {
            if (idleAnimationCoroutine != null)
            {
                StopCoroutine(idleAnimationCoroutine);
            }
            idleAnimationCoroutine = StartCoroutine(IdleAnimationLoop());
        }

        /// <summary>
        /// Loop da animação idle
        /// </summary>
        private IEnumerator IdleAnimationLoop()
        {
            while (enabled)
            {
                if (!isAnimating && currentEmotion == BLOBController.EmotionType.Neutral)
                {
                    // Respiração suave
                    float time = Time.time;
                    float breatheOffset = Mathf.Sin(time * 0.8f) * 0.02f;
                    Vector3 breatheScale = baseScale * (1f + breatheOffset);

                    // Flutuação suave
                    float floatOffset = Mathf.Sin(time * 0.5f) * 0.03f;
                    Vector3 floatPosition = originalPosition + Vector3.up * floatOffset;

                    // Aplicar transformações suaves
                    blobTransform.localScale = Vector3.Lerp(blobTransform.localScale, breatheScale, Time.deltaTime * 2f);
                    blobTransform.position = Vector3.Lerp(blobTransform.position, floatPosition, Time.deltaTime * 1f);
                }

                yield return null;
            }
        }

        /// <summary>
        /// Retorna às configurações neutras
        /// </summary>
        private void ReturnToNeutral()
        {
            StartCoroutine(ReturnToNeutralCoroutine());
        }

        /// <summary>
        /// Corrotina para retornar ao estado neutro
        /// </summary>
        private IEnumerator ReturnToNeutralCoroutine()
        {
            float duration = 1f;
            float elapsed = 0f;

            Vector3 startPosition = blobTransform.position;
            Vector3 startScale = blobTransform.localScale;
            Quaternion startRotation = blobTransform.rotation;

            while (elapsed < duration)
            {
                float progress = elapsed / duration;
                float smoothProgress = Mathf.SmoothStep(0f, 1f, progress);

                blobTransform.position = Vector3.Lerp(startPosition, originalPosition, smoothProgress);
                blobTransform.localScale = Vector3.Lerp(startScale, baseScale, smoothProgress);
                blobTransform.rotation = Quaternion.Lerp(startRotation, originalRotation, smoothProgress);

                elapsed += Time.deltaTime;
                yield return null;
            }

            // Garantir valores finais exatos
            blobTransform.position = originalPosition;
            blobTransform.localScale = baseScale;
            blobTransform.rotation = originalRotation;
        }

        /// <summary>
        /// Para todas as animações
        /// </summary>
        public void StopAllAnimations()
        {
            if (currentAnimationCoroutine != null)
            {
                StopCoroutine(currentAnimationCoroutine);
                currentAnimationCoroutine = null;
            }

            isAnimating = false;
            ReturnToNeutral();
        }

        /// <summary>
        /// Propriedades públicas
        /// </summary>
        public bool IsAnimating => isAnimating;
        public BLOBController.EmotionType CurrentEmotion => currentEmotion;

        /// <summary>
        /// Configurações públicas
        /// </summary>
        public void SetAnimationSpeed(float speed) => animationSpeed = Mathf.Max(0.1f, speed);
        public void SetIntensityMultiplier(float intensity) => intensityMultiplier = Mathf.Max(0.1f, intensity);
        public void EnablePhysicsAnimation() => enablePhysicsAnimation = true;
        public void DisablePhysicsAnimation() => enablePhysicsAnimation = false;
        public void EnableIdleAnimation() 
        { 
            enableIdleAnimation = true;
            StartIdleAnimation();
        }
        public void DisableIdleAnimation() 
        { 
            enableIdleAnimation = false;
            if (idleAnimationCoroutine != null)
            {
                StopCoroutine(idleAnimationCoroutine);
                idleAnimationCoroutine = null;
            }
        }
    }
}