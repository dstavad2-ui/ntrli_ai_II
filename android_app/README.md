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

## Branch Structure

This is the **application layer** branch (`ntrli-app`).

| Component | Location | Description |
|-----------|----------|-------------|
| Android App | `android_app/` | Kivy-based mobile app |
| APK Workflow | `.github/workflows/build_apk.yml` | Automated builds |
| Settings | `settings.json.example` | User configuration |
| Core | `core/` (submodule) | NTRLI' AI engine |

## Features

- Clean, modern mobile UI
- Provider selection (Groq, OpenAI, DeepSeek)
- Real-time execution output
- Offline mode with cached knowledge
- Settings management
- 10 Behavioral Laws embedded

## Self-Contained Design

The Android app is **completely self-contained**:

```python
# All core logic embedded - no external dependencies
# - Embedded LLM providers
# - Embedded Planner and Executor
# - Embedded KnowledgeCache
# - Minimal requirements: kivy, requests, certifi
```

This follows NTRLI' AI principles:
- No guessing - all dependencies validated at startup
- No silent failure - comprehensive error handling
- Deterministic behavior - consistent state management

## Build APK

### Automated (GitHub Actions)

1. Go to **Actions** → **Build Android APK**
2. Click **Run workflow**
3. Select debug or release
4. Download APK from artifacts

### Manual Build

```bash
# Install buildozer
pip install buildozer cython

# Build debug APK
cd android_app
buildozer android debug

# APK in android_app/bin/
```

## Configuration

```json
{
  "api_keys": {
    "groq": "gsk_...",
    "openai": "sk_...",
    "deepseek": "sk_..."
  }
}
```

Settings stored in app data directory on device.

## Screens

| Screen | Purpose |
|--------|---------|
| Execute | Enter instructions, run AI |
| Settings | API keys, cache management |
| About | 10 Laws, version info |

## Requirements

```
python3
kivy==2.3.0
requests
certifi
charset-normalizer
idna
urllib3
```

## Buildozer Spec

Key settings in `buildozer.spec`:

```ini
android.api = 33
android.minapi = 24
android.archs = arm64-v8a,armeabi-v7a
android.permissions = INTERNET,ACCESS_NETWORK_STATE
```

---

**Core repository:** See `main` branch for NTRLI' AI engine.
