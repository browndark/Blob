# BLOB Unity 3D - Assistente Virtual Interativo

## 📋 Visão Geral do Projeto

Este projeto implementa um assistente virtual em 3D usando Unity, com um personagem BLOB amarelo que responde a comandos de voz, expressa emoções e interage de forma natural com o usuário.

## 🎯 Funcionalidades Principais

### 🗣️ Sistema de Voz
- **Reconhecimento de Voz**: Detecta comandos falados pelo usuário
- **Síntese de Fala**: BLOB responde com voz sintetizada
- **Palavra de Ativação**: "blob" + comando
- **Linguagem**: Português brasileiro
- **Voz Neutra**: Configuração não-binária

### 😊 Sistema de Emoções
- **8 Estados Emocionais**:
  - Neutro (amarelo padrão)
  - Feliz (amarelo brilhante)
  - Triste (azul)
  - Animado (laranja vibrante)
  - Bravo (vermelho)
  - Surpreso (rosa)
  - Pensando (roxo)
  - Falando (verde)

### 🎭 Sistema de Animações
- **Animações Procedurais**: Movimento baseado em física
- **Animação Idle**: Respiração e flutuação suaves
- **Animações Emocionais**:
  - Feliz: Pulos alegres
  - Triste: Movimento lento para baixo
  - Animado: Movimento rápido e errático
  - Bravo: Tremor intenso
  - Surpreso: Expansão súbita + vibração
  - Pensando: Movimento circular suave
  - Falando: Pulso rítmico

## 🏗️ Arquitetura do Sistema

### Componentes Principais

#### 1. BLOBController.cs
- **Função**: Controle central do BLOB
- **Responsabilidades**:
  - Gerenciar estados emocionais
  - Coordenar sistemas de voz e animação
  - Processar comandos de entrada
  - Manter histórico de conversas

#### 2. EmotionSystem.cs
- **Função**: Gerenciar transições de cores/emoções
- **Responsabilidades**:
  - Transições suaves entre cores
  - Efeitos de brilho
  - Mapeamento emoção-cor

#### 3. VoiceSystem.cs
- **Função**: Processamento de voz
- **Responsabilidades**:
  - Reconhecimento de comandos
  - Síntese de fala
  - Banco de dados de respostas
  - Configurações de áudio

#### 4. AnimationSystem.cs
- **Função**: Animações procedurais
- **Responsabilidades**:
  - Animações baseadas em emoções
  - Física e movimentação
  - Deformações e efeitos visuais

## 🔧 Configuração do Projeto

### Estrutura de Pastas
```
UnityProject/
├── Assets/
│   ├── Scripts/
│   │   ├── BLOBController.cs
│   │   ├── EmotionSystem.cs
│   │   ├── VoiceSystem.cs
│   │   └── AnimationSystem.cs
│   ├── Materials/
│   │   └── BLOBMaterial.mat
│   ├── Prefabs/
│   └── Scenes/
│       └── MainScene.unity
```

### Hierarquia da Cena
```
MainScene
├── Main Camera
├── Directional Light
└── BLOB (GameObject principal)
    ├── MeshFilter (Sphere)
    ├── MeshRenderer (BLOBMaterial)
    ├── SphereCollider
    ├── AudioSource
    ├── BLOBController
    ├── EmotionSystem
    ├── VoiceSystem
    └── AnimationSystem
```

## ⚙️ Configurações Técnicas

### Material BLOB
- **Shader**: Standard
- **Cor Base**: Amarelo (1, 0.9, 0.2, 1)
- **Emissão**: Habilitada para efeitos de brilho
- **Metallic**: 0.1 (baixo)
- **Smoothness**: 0.7 (suave)

### Configurações de Áudio
- **Volume**: 0.8
- **Espacialização**: 3D
- **Rolloff**: Linear
- **Distância**: 1-500 unidades

### Performance
- **Target**: 60 FPS
- **Plataforma**: Windows Desktop
- **Future**: Mobile (iOS/Android)

## 🎮 Comandos de Voz

### Comandos Básicos
- "blob feliz" → Emoção feliz + animação de pulos
- "blob triste" → Emoção triste + movimento lento
- "blob animado" → Emoção animada + movimento rápido
- "blob bravo" → Emoção brava + tremor
- "blob surpreso" → Emoção surpresa + expansão
- "blob pensando" → Emoção pensativa + movimento circular
- "blob oi" → Cumprimento + emoção feliz
- "blob tchau" → Despedida + emoção neutra

### Respostas do Sistema
O BLOB possui respostas variadas para cada comando, escolhidas aleatoriamente:

**Exemplo - Feliz**:
- "Que alegria! Estou muito feliz também!"
- "Eba! Adoro quando você está feliz!"
- "Sua felicidade me deixa radiante!"

## 💻 Requisitos do Sistema

### Mínimos
- **OS**: Windows 10
- **Unity**: 2022.3 LTS ou superior
- **RAM**: 4GB
- **GPU**: DirectX 11 compatível
- **Microfone**: Para reconhecimento de voz
- **Alto-falantes**: Para síntese de fala

### Recomendados
- **OS**: Windows 11
- **RAM**: 8GB
- **GPU**: Dedicada
- **Microfone**: Com cancelamento de ruído

## 🚀 Como Executar

### 1. Preparar Ambiente
```bash
# Verificar se Unity está instalado
# Verificar extensões VS Code instaladas:
# - Visual Studio Tools for Unity
# - Unity Code Snippets
# - Unity Tools
# - C# Extensions
```

### 2. Abrir Projeto
1. Abrir Unity Hub
2. Adicionar projeto: `UnityProject/`
3. Abrir com Unity 2022.3 LTS+

### 3. Configurar Cena
1. Abrir `Assets/Scenes/MainScene.unity`
2. Verificar configurações do BLOB GameObject
3. Testar componentes no Inspector

### 4. Build e Execução
1. File → Build Settings
2. Selecionar Windows PC
3. Add Open Scenes
4. Build And Run

## 🧪 Teste e Debug

### Comandos de Teste no Inspector
- **BLOBController**: Botão "Test Emotion Change"
- **VoiceSystem**: Botão "Test Voice Command"
- **AnimationSystem**: Slider de velocidade/intensidade
- **EmotionSystem**: Preview de cores

### Logs de Debug
```csharp
Debug.Log("BLOB Controller initialized successfully!");
Debug.Log("Voice command received: feliz");
Debug.Log("Emotion changed to: Happy");
Debug.Log("BLOB said: Que alegria! Estou muito feliz também!");
```

### Problemas Comuns
1. **Sem áudio**: Verificar AudioSource e drivers
2. **Sem animação**: Verificar componentes ativos
3. **Comandos não funcionam**: Verificar palavra de ativação
4. **Performance baixa**: Reduzir qualidade gráfica

## 📱 Roadmap Mobile

### Próximas Etapas
1. **Configurar Build Android/iOS**
2. **Otimizar Performance Mobile**
3. **Interface Touch**
4. **Integração Cloud Speech**
5. **Sistema de Monetização**

### Configurações Mobile
```csharp
// Configurações específicas para mobile
#if UNITY_ANDROID || UNITY_IOS
    animationSpeed *= 0.8f; // Reduzir para economia de bateria
    maxParticles = 50; // Reduzir partículas
    audioQuality = AudioQuality.Medium;
#endif
```

## 📈 Monetização

### Modelo Premium
- **Versão Gratuita**: Funcionalidades básicas
- **Versão Premium**: 
  - Mais emoções
  - Personalização visual
  - Comandos avançados
  - Sincronização cloud

### In-App Purchases
- Novas skins/cores
- Pacotes de animação
- Vozes premium
- Funcionalidades exclusivas

## 👥 Contribuição

### Estrutura de Desenvolvimento
```
BLOB/
├── blob_super_simples.py (Protótipo Python)
├── UnityProject/ (Versão Unity)
├── docs/ (Documentação)
└── tests/ (Testes automatizados)
```

### Padrões de Código
- **Namespace**: `BLOB`
- **Comentários**: XML documentation
- **Indentação**: 4 espaços
- **Naming**: PascalCase para públicos, camelCase para privados

## 📄 Licença

Este projeto está em desenvolvimento para fins educacionais e demonstração de capacidades de IA conversacional.

---

## 🔗 Links Úteis

- [Unity Documentation](https://docs.unity3d.com/)
- [C# Unity Scripting](https://docs.unity3d.com/Manual/ScriptingSection.html)
- [Windows Speech API](https://docs.microsoft.com/en-us/windows/apps/speech/)
- [Unity Audio System](https://docs.unity3d.com/Manual/AudioOverview.html)

---

**Criado com ❤️ usando Unity 3D e C#**
*Assistente Virtual Inteligente - Projeto BLOB*