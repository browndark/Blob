using UnityEngine;
using UnityEditor;

namespace BLOB
{
    /// <summary>
    /// Script para configuração automática do projeto BLOB Unity
    /// Cria a estrutura necessária e configura componentes
    /// </summary>
    public class BLOBSetup : MonoBehaviour
    {
        [Header("Auto Setup")]
        [SerializeField] private bool autoSetupOnStart = true;
        [SerializeField] private bool createBLOBPrefab = true;
        [SerializeField] private bool configureCameraSettings = true;
        [SerializeField] private bool setupLighting = true;

        [Header("BLOB Configuration")]
        [SerializeField] private Vector3 blobPosition = Vector3.zero;
        [SerializeField] private Vector3 blobScale = Vector3.one;
        [SerializeField] private Material blobMaterial;

        void Start()
        {
            if (autoSetupOnStart)
            {
                SetupBLOBProject();
            }
        }

        /// <summary>
        /// Configura o projeto BLOB automaticamente
        /// </summary>
        [ContextMenu("Setup BLOB Project")]
        public void SetupBLOBProject()
        {
            Debug.Log("🚀 Starting BLOB Project Setup...");

            // 1. Configurar câmera
            if (configureCameraSettings)
            {
                SetupCamera();
            }

            // 2. Configurar iluminação
            if (setupLighting)
            {
                SetupLighting();
            }

            // 3. Criar BLOB se não existir
            GameObject existingBLOB = GameObject.Find("BLOB");
            if (existingBLOB == null)
            {
                CreateBLOBCharacter();
            }
            else
            {
                Debug.Log("✅ BLOB already exists in scene");
                ConfigureBLOBComponents(existingBLOB);
            }

            // 4. Criar prefab se solicitado
            if (createBLOBPrefab)
            {
                CreateBLOBPrefab();
            }

            Debug.Log("🎉 BLOB Project Setup Complete!");
        }

        /// <summary>
        /// Configura as configurações da câmera
        /// </summary>
        private void SetupCamera()
        {
            Camera mainCamera = Camera.main;
            if (mainCamera == null)
            {
                Debug.LogWarning("⚠️ Main Camera not found");
                return;
            }

            // Configurações otimizadas para o BLOB
            mainCamera.transform.position = new Vector3(0, 1, -5);
            mainCamera.transform.rotation = Quaternion.identity;
            mainCamera.fieldOfView = 60f;
            mainCamera.backgroundColor = new Color(0.2f, 0.3f, 0.5f, 1f);
            mainCamera.clearFlags = CameraClearFlags.SolidColor;

            Debug.Log("📷 Camera configured successfully");
        }

        /// <summary>
        /// Configura a iluminação da cena
        /// </summary>
        private void SetupLighting()
        {
            // Encontrar ou criar luz direcional
            Light directionalLight = FindObjectOfType<Light>();
            if (directionalLight == null)
            {
                GameObject lightObject = new GameObject("Directional Light");
                directionalLight = lightObject.AddComponent<Light>();
            }

            // Configurar luz direcional
            directionalLight.type = LightType.Directional;
            directionalLight.intensity = 1.2f;
            directionalLight.color = Color.white;
            directionalLight.shadows = LightShadows.Soft;
            directionalLight.transform.rotation = Quaternion.Euler(50f, -30f, 0f);

            // Configurar ambiente
            RenderSettings.ambientMode = UnityEngine.Rendering.AmbientMode.Trilight;
            RenderSettings.ambientSkyColor = new Color(0.5f, 0.7f, 1f);
            RenderSettings.ambientEquatorColor = new Color(0.4f, 0.4f, 0.4f);
            RenderSettings.ambientGroundColor = new Color(0.2f, 0.2f, 0.2f);

            Debug.Log("💡 Lighting configured successfully");
        }

        /// <summary>
        /// Cria o personagem BLOB
        /// </summary>
        private void CreateBLOBCharacter()
        {
            // Criar GameObject principal
            GameObject blobObject = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            blobObject.name = "BLOB";
            blobObject.transform.position = blobPosition;
            blobObject.transform.localScale = blobScale;

            // Configurar componentes
            ConfigureBLOBComponents(blobObject);

            Debug.Log("🟡 BLOB character created successfully");
        }

        /// <summary>
        /// Configura os componentes do BLOB
        /// </summary>
        private void ConfigureBLOBComponents(GameObject blobObject)
        {
            // Adicionar AudioSource se não existir
            AudioSource audioSource = blobObject.GetComponent<AudioSource>();
            if (audioSource == null)
            {
                audioSource = blobObject.AddComponent<AudioSource>();
            }
            audioSource.playOnAwake = false;
            audioSource.volume = 0.8f;

            // Configurar material se fornecido
            if (blobMaterial != null)
            {
                Renderer renderer = blobObject.GetComponent<Renderer>();
                if (renderer != null)
                {
                    renderer.material = blobMaterial;
                }
            }

            // Adicionar scripts do BLOB se não existirem
            if (blobObject.GetComponent<BLOBController>() == null)
            {
                blobObject.AddComponent<BLOBController>();
            }

            if (blobObject.GetComponent<EmotionSystem>() == null)
            {
                blobObject.AddComponent<EmotionSystem>();
            }

            if (blobObject.GetComponent<VoiceSystem>() == null)
            {
                blobObject.AddComponent<VoiceSystem>();
            }

            if (blobObject.GetComponent<AnimationSystem>() == null)
            {
                blobObject.AddComponent<AnimationSystem>();
            }

            Debug.Log("🔧 BLOB components configured successfully");
        }

        /// <summary>
        /// Cria um prefab do BLOB
        /// </summary>
        private void CreateBLOBPrefab()
        {
#if UNITY_EDITOR
            GameObject blobObject = GameObject.Find("BLOB");
            if (blobObject != null)
            {
                // Criar diretório de prefabs se não existir
                string prefabPath = "Assets/Prefabs/";
                if (!AssetDatabase.IsValidFolder(prefabPath))
                {
                    AssetDatabase.CreateFolder("Assets", "Prefabs");
                }

                // Criar prefab
                string prefabFullPath = prefabPath + "BLOB.prefab";
                PrefabUtility.SaveAsPrefabAsset(blobObject, prefabFullPath);
                
                Debug.Log("📦 BLOB prefab created at: " + prefabFullPath);
            }
#endif
        }

        /// <summary>
        /// Valida a configuração atual
        /// </summary>
        [ContextMenu("Validate BLOB Setup")]
        public void ValidateSetup()
        {
            Debug.Log("🔍 Validating BLOB Setup...");

            // Verificar BLOB
            GameObject blobObject = GameObject.Find("BLOB");
            if (blobObject == null)
            {
                Debug.LogError("❌ BLOB object not found!");
                return;
            }

            // Verificar componentes
            bool allComponentsPresent = true;
            
            if (blobObject.GetComponent<BLOBController>() == null)
            {
                Debug.LogError("❌ BLOBController component missing!");
                allComponentsPresent = false;
            }

            if (blobObject.GetComponent<EmotionSystem>() == null)
            {
                Debug.LogError("❌ EmotionSystem component missing!");
                allComponentsPresent = false;
            }

            if (blobObject.GetComponent<VoiceSystem>() == null)
            {
                Debug.LogError("❌ VoiceSystem component missing!");
                allComponentsPresent = false;
            }

            if (blobObject.GetComponent<AnimationSystem>() == null)
            {
                Debug.LogError("❌ AnimationSystem component missing!");
                allComponentsPresent = false;
            }

            if (blobObject.GetComponent<AudioSource>() == null)
            {
                Debug.LogError("❌ AudioSource component missing!");
                allComponentsPresent = false;
            }

            // Verificar câmera
            if (Camera.main == null)
            {
                Debug.LogError("❌ Main Camera not found!");
                allComponentsPresent = false;
            }

            // Verificar iluminação
            if (FindObjectOfType<Light>() == null)
            {
                Debug.LogWarning("⚠️ No lights found in scene!");
            }

            if (allComponentsPresent)
            {
                Debug.Log("✅ BLOB Setup validation passed!");
            }
            else
            {
                Debug.LogError("❌ BLOB Setup validation failed!");
            }
        }

        /// <summary>
        /// Remove todos os objetos BLOB da cena
        /// </summary>
        [ContextMenu("Clean BLOB Setup")]
        public void CleanSetup()
        {
            GameObject[] blobObjects = GameObject.FindGameObjectsWithTag("Untagged");
            foreach (GameObject obj in blobObjects)
            {
                if (obj.name.Contains("BLOB"))
                {
                    DestroyImmediate(obj);
                    Debug.Log("🗑️ Removed: " + obj.name);
                }
            }

            Debug.Log("🧹 BLOB Setup cleaned");
        }

        /// <summary>
        /// Testa as funcionalidades do BLOB
        /// </summary>
        [ContextMenu("Test BLOB Functions")]
        public void TestBLOBFunctions()
        {
            GameObject blobObject = GameObject.Find("BLOB");
            if (blobObject == null)
            {
                Debug.LogError("❌ BLOB not found for testing!");
                return;
            }

            BLOBController controller = blobObject.GetComponent<BLOBController>();
            if (controller == null)
            {
                Debug.LogError("❌ BLOBController not found for testing!");
                return;
            }

            Debug.Log("🧪 Testing BLOB functions...");

            // Testar mudança de emoção
            StartCoroutine(TestEmotionSequence(controller));
        }

        /// <summary>
        /// Sequência de teste das emoções
        /// </summary>
        private System.Collections.IEnumerator TestEmotionSequence(BLOBController controller)
        {
            BLOBController.EmotionType[] emotions = {
                BLOBController.EmotionType.Happy,
                BLOBController.EmotionType.Sad,
                BLOBController.EmotionType.Excited,
                BLOBController.EmotionType.Angry,
                BLOBController.EmotionType.Surprised,
                BLOBController.EmotionType.Thinking,
                BLOBController.EmotionType.Neutral
            };

            foreach (var emotion in emotions)
            {
                Debug.Log($"🎭 Testing emotion: {emotion}");
                controller.SetEmotion(emotion);
                yield return new WaitForSeconds(2f);
            }

            Debug.Log("✅ Emotion test sequence completed!");
        }
    }
}