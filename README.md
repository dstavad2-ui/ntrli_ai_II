# NTRLI' AI

**Deterministic, Execution-First Artificial Intelligence System**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build APK](https://img.shields.io/badge/build-APK-green.svg)](#android-app)

## Overview

NTRLI' AI is a command-driven execution engine that performs real work—planning, research, coding, validation, and GitHub administration—under strict mechanical constraints.

**Key Principles:**
- No output without a plan
- No execution without verification
- No hallucination, no filler, no goal drift
- No silent failure, no autonomy

See the [Whitepaper](WHITEPAPER.md) for complete documentation.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/ntrli_ai_II.git
cd ntrli_ai_II

# Install dependencies
pip install -r requirements.txt

# Initialize configuration
cd ntrli_ai
python cli.py config init

# Set at least one API key
export OPENAI_API_KEY=sk-...
# or
export GROQ_API_KEY=gsk_...

# Run NTRLI' AI
python main.py "Research Python best practices"
```

## Configuration

NTRLI' AI uses a simple, Claude Code-style configuration system.

### Configuration Commands

```bash
# Show current configuration
python cli.py config

# Get a specific setting
python cli.py config get router.strategy

# Set a value
python cli.py config set router.strategy fastest

# Reset to defaults
python cli.py config reset

# Initialize config files
python cli.py config init
```

### Provider Management

```bash
# List all providers
python cli.py providers

# Enable a provider
python cli.py providers enable groq

# Disable a provider
python cli.py providers disable replicate

# Set provider model
python cli.py providers model openai gpt-4o
```

### Configuration Files

Settings are loaded from (in order):
1. Default values
2. User config: `~/.ntrli_ai/settings.json`
3. Project config: `.ntrli_ai.json` (in project root)
4. Environment variables

Copy `settings.json.example` to customize:
```bash
cp settings.json.example ~/.ntrli_ai/settings.json
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `ROUTER_STRATEGY` | Router strategy override |
| `NTRLI_VERBOSE` | Enable verbose output |
| `NTRLI_JSON_OUTPUT` | Output in JSON format |
| `NTRLI_SANDBOX_TIMEOUT` | Execution timeout (seconds) |

## Supported Providers

| Provider | Best For | Pricing | Priority |
|----------|----------|---------|----------|
| Groq | Speed (276 tok/sec) | $0.59/1M tokens | 0 (fastest) |
| Claude | Coding (93.7% accuracy) | $3-$15/1M tokens | 1 |
| OpenAI | General purpose | $5-$15/1M tokens | 2 |
| Gemini | Multimodal, cheapest | $1.25-$7/1M tokens | 3 |
| Mistral | European compliance | $2-$8/1M tokens | 4 |
| Together | Cost optimization | $0.20-$0.80/1M tokens | 5 |
| DeepSeek | Ultra low cost | $0.14/1M tokens | 6 |

## Android App

NTRLI' AI includes a full Android application built with Kivy.

### Automated APK Build

APKs are automatically built via GitHub Actions:

1. Go to **Actions** → **Build Android APK**
2. Click **Run workflow**
3. Select build type (debug/release)
4. Download APK from artifacts

### Manual Build

```bash
# Install buildozer
pip install buildozer cython

# Build debug APK
cd android_app
buildozer android debug

# APK will be in android_app/bin/
```

### App Features

- Clean, modern UI for instruction input
- Provider selection and configuration
- Real-time execution output
- Settings management
- Works offline with cached knowledge

## Project Structure

```
ntrli_ai_II/
├── ntrli_ai/               # Core AI system
│   ├── main.py             # Entry point
│   ├── cli.py              # CLI interface
│   ├── config.py           # Configuration system
│   ├── control_plane.py    # Single command gate
│   ├── orchestrator.py     # Execution core
│   ├── planner.py          # Plan-first enforcement
│   ├── providers/          # LLM provider adapters
│   └── tools/              # Execution tools
├── android_app/            # Android application
│   ├── main.py             # Kivy app
│   └── buildozer.spec      # Build configuration
├── .github/workflows/
│   ├── ai_guarded.yml      # AI execution workflow
│   └── build_apk.yml       # APK build workflow
├── WHITEPAPER.md           # Full specification
├── settings.json.example   # Configuration template
└── requirements.txt        # Python dependencies
```

## GitHub Actions

### AI Execution

Trigger NTRLI' AI via GitHub Actions:

1. Go to Actions → **NTRLI AI Guarded Execution**
2. Click **Run workflow**
3. Enter your instruction
4. Select router strategy

### APK Build

Build Android APK automatically:

1. Go to Actions → **Build Android APK**
2. Click **Run workflow**
3. Select debug or release
4. Download from artifacts

## Documentation

- [Whitepaper](WHITEPAPER.md) - Complete specification
- [settings.json.example](settings.json.example) - Configuration template
- [.env.example](.env.example) - Environment variables

## License

MIT License - See LICENSE for details.
