using UnityEngine;
using System.Collections;

namespace BLOB
{
    /// <summary>
    /// Sistema responsável por gerenciar as emoções visuais do BLOB
    /// </summary>
    public class EmotionSystem : MonoBehaviour
    {
        [Header("Emotion Colors")]
        [SerializeField] private Color neutralColor = Color.yellow;
        [SerializeField] private Color happyColor = Color.yellow;
        [SerializeField] private Color sadColor = new Color(0.9f, 0.8f, 0f);
        [SerializeField] private Color excitedColor = Color.white;
        [SerializeField] private Color angryColor = new Color(1f, 0.7f, 0f);
        [SerializeField] private Color thinkingColor = new Color(1f, 0.8f, 0.2f);
        [SerializeField] private Color speakingColor = new Color(1f, 0.95f, 0.5f);
        [SerializeField] private Color surprisedColor = new Color(1f, 0.9f, 0.1f);

        [Header("Transition Settings")]
        [SerializeField] private float colorTransitionSpeed = 2f;
        [SerializeField] private AnimationCurve emotionCurve = AnimationCurve.EaseInOut(0, 0, 1, 1);

        private BLOBController blobController;
        private Renderer[] renderers;
        private Material[] originalMaterials;
        private Color currentTargetColor;
        private Coroutine colorTransition;

        /// <summary>
        /// Inicializa o sistema de emoções
        /// </summary>
        public void Initialize(BLOBController controller, Material[] emotionMaterials)
        {
            blobController = controller;
            
            // Encontrar todos os renderers do BLOB
            renderers = GetComponentsInChildren<Renderer>();
            
            // Armazenar materiais originais
            originalMaterials = new Material[renderers.Length];
            for (int i = 0; i < renderers.Length; i++)
            {
                originalMaterials[i] = renderers[i].material;
            }

            // Definir cor inicial
            currentTargetColor = neutralColor;
            SetColor(neutralColor);
        }

        /// <summary>
        /// Chamado quando a emoção muda
        /// </summary>
        public void OnEmotionChanged(BLOBController.EmotionType emotion)
        {
            Color targetColor = GetEmotionColor(emotion);
            TransitionToColor(targetColor);
        }

        /// <summary>
        /// Retorna a cor associada à emoção
        /// </summary>
        private Color GetEmotionColor(BLOBController.EmotionType emotion)
        {
            switch (emotion)
            {
                case BLOBController.EmotionType.Neutral:
                    return neutralColor;
                case BLOBController.EmotionType.Happy:
                    return happyColor;
                case BLOBController.EmotionType.Sad:
                    return sadColor;
                case BLOBController.EmotionType.Excited:
                    return excitedColor;
                case BLOBController.EmotionType.Angry:
                    return angryColor;
                case BLOBController.EmotionType.Thinking:
                    return thinkingColor;
                case BLOBController.EmotionType.Speaking:
                    return speakingColor;
                case BLOBController.EmotionType.Surprised:
                    return surprisedColor;
                default:
                    return neutralColor;
            }
        }

        /// <summary>
        /// Transição suave para nova cor
        /// </summary>
        private void TransitionToColor(Color targetColor)
        {
            if (colorTransition != null)
            {
                StopCoroutine(colorTransition);
            }

            currentTargetColor = targetColor;
            colorTransition = StartCoroutine(ColorTransitionCoroutine(targetColor));
        }

        /// <summary>
        /// Corrotina para transição de cor
        /// </summary>
        private IEnumerator ColorTransitionCoroutine(Color targetColor)
        {
            Color startColor = GetCurrentColor();
            float elapsed = 0f;
            float duration = 1f / colorTransitionSpeed;

            while (elapsed < duration)
            {
                elapsed += Time.deltaTime;
                float progress = elapsed / duration;
                
                // Usar curva de animação para suavidade
                float curveValue = emotionCurve.Evaluate(progress);
                Color currentColor = Color.Lerp(startColor, targetColor, curveValue);
                
                SetColor(currentColor);
                
                yield return null;
            }

            SetColor(targetColor);
        }

        /// <summary>
        /// Define a cor de todos os renderers
        /// </summary>
        private void SetColor(Color color)
        {
            foreach (Renderer renderer in renderers)
            {
                if (renderer != null && renderer.material != null)
                {
                    // Usar _BaseColor para HDRP/URP ou _Color para Standard
                    if (renderer.material.HasProperty("_BaseColor"))
                    {
                        renderer.material.SetColor("_BaseColor", color);
                    }
                    else if (renderer.material.HasProperty("_Color"))
                    {
                        renderer.material.SetColor("_Color", color);
                    }
                }
            }
        }

        /// <summary>
        /// Retorna a cor atual do primeiro renderer
        /// </summary>
        private Color GetCurrentColor()
        {
            if (renderers.Length > 0 && renderers[0] != null && renderers[0].material != null)
            {
                if (renderers[0].material.HasProperty("_BaseColor"))
                {
                    return renderers[0].material.GetColor("_BaseColor");
                }
                else if (renderers[0].material.HasProperty("_Color"))
                {
                    return renderers[0].material.GetColor("_Color");
                }
            }
            
            return Color.white;
        }

        /// <summary>
        /// Adiciona efeito de brilho para emoções especiais
        /// </summary>
        public void AddGlowEffect(BLOBController.EmotionType emotion)
        {
            switch (emotion)
            {
                case BLOBController.EmotionType.Excited:
                    StartCoroutine(PulseGlow(2f, 0.5f));
                    break;
                case BLOBController.EmotionType.Happy:
                    StartCoroutine(PulseGlow(1.5f, 1f));
                    break;
                case BLOBController.EmotionType.Surprised:
                    StartCoroutine(FlashGlow());
                    break;
            }
        }

        /// <summary>
        /// Efeito de pulso brilhante
        /// </summary>
        private IEnumerator PulseGlow(float intensity, float duration)
        {
            float elapsed = 0f;
            Color originalColor = currentTargetColor;

            while (elapsed < duration)
            {
                elapsed += Time.deltaTime;
                float pulse = Mathf.Sin(elapsed * Mathf.PI * 4) * 0.5f + 0.5f;
                Color glowColor = Color.Lerp(originalColor, Color.white, pulse * intensity * 0.3f);
                SetColor(glowColor);
                yield return null;
            }

            SetColor(originalColor);
        }

        /// <summary>
        /// Efeito de flash brilhante
        /// </summary>
        private IEnumerator FlashGlow()
        {
            Color originalColor = currentTargetColor;
            
            // Flash rápido para branco
            SetColor(Color.white);
            yield return new WaitForSeconds(0.1f);
            
            // Retornar à cor original
            SetColor(originalColor);
        }

        /// <summary>
        /// Propriedades públicas
        /// </summary>
        public Color CurrentTargetColor => currentTargetColor;

        /// <summary>
        /// Métodos de configuração dinâmica
        /// </summary>
        public void SetNeutralColor(Color color) => neutralColor = color;
        public void SetHappyColor(Color color) => happyColor = color;
        public void SetSadColor(Color color) => sadColor = color;
        public void SetExcitedColor(Color color) => excitedColor = color;
        public void SetAngryColor(Color color) => angryColor = color;
        public void SetThinkingColor(Color color) => thinkingColor = color;
        public void SetSpeakingColor(Color color) => speakingColor = color;
        public void SetSurprisedColor(Color color) => surprisedColor = color;
    }
}