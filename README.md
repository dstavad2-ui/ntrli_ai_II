# NTRLI' AI App

**Android Application for NTRLI' AI**

```
┌─────────────────────────────────────────────────────────┐
│                    NTRLI' AI App                        │
│                                                         │
│       UI │ Android │ Product Logic │ User Experience    │
│                                                         │
│            Depends on Core as Submodule                 │
└─────────────────────────────────────────────────────────┘
```

## Repository Structure

This is the **application layer** branch (`ntrli-app`).

| Branch | Contents | Purpose |
|--------|----------|---------|
| `main` | NTRLI' AI Core | Engine: execution, planning, validation, autonomy rules |
| `ntrli-app` | Application | UI, Android app, product logic |

**Why separate?** App can't break core - they're isolated.

## App Components

```
ntrli-app/
├── android_app/
│   ├── main.py           # Self-contained Kivy app
│   ├── buildozer.spec    # APK build configuration
│   └── README.md         # App documentation
├── .github/workflows/
│   └── build_apk.yml     # Automated APK builder
├── settings.json.example # Configuration template
└── core/                 # NTRLI' AI Core (submodule)
```

## Features

- Clean, modern mobile UI
- Provider selection (Groq, OpenAI, DeepSeek)
- Real-time execution output with streaming
- Offline mode with cached knowledge
- Settings management
- 10 Behavioral Laws embedded

## Self-Contained Design

The Android app embeds all core logic:

```python
# No external ntrli_ai imports - all embedded:
# - LLM providers (OpenAI, Groq, DeepSeek)
# - Planner with JSON schema validation
# - Step executor
# - KnowledgeCache for offline mode
# - HTTPClient with retry logic
```

This follows NTRLI' AI principles:
- **No guessing** - all dependencies validated at startup
- **No silent failure** - comprehensive error handling
- **Deterministic behavior** - consistent state management

## Build APK

### Automated (GitHub Actions)

1. Go to **Actions** → **Build Android APK**
2. Click **Run workflow**
3. Select debug or release
4. Download APK from artifacts

### Manual Build

```bash
pip install buildozer cython
cd android_app
buildozer android debug
# APK in android_app/bin/
```

## Configuration

Copy `settings.json.example` and configure:

```json
{
  "api_keys": {
    "groq": "gsk_...",
    "openai": "sk-...",
    "deepseek": "sk-..."
  },
  "router": {
    "strategy": "fastest"
  }
}
```

## App Screens

| Screen | Purpose |
|--------|---------|
| **Execute** | Enter instructions, run AI, view results |
| **Settings** | API keys, provider config, cache |
| **About** | 10 Behavioral Laws, version info |

## Build Requirements

**Minimal dependencies for fast, small APK:**

```
python3
kivy==2.3.0
requests
certifi
```

**Target platforms:**
- ARM64-v8a (modern devices)
- ARMeabi-v7a (older devices)
- Android API 24+ (Android 7.0+)

## Core Submodule

To add core functionality:

```bash
git submodule add -b main ../ntrli_ai_II.git core
git submodule update --init
```

---

**Core repository:** See `main` branch for NTRLI' AI engine.
