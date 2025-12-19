# NTRLI' AI Core

**Deterministic, Execution-First AI Engine**

```
┌─────────────────────────────────────────────────────────┐
│                    NTRLI' AI Core                       │
│                                                         │
│  Execution Engine │ Planning │ Validation │ Autonomy   │
│                                                         │
│  "No guessing. No hallucination. No goal drift."        │
└─────────────────────────────────────────────────────────┘
```

## Repository Structure

This repository uses a **two-branch architecture**:

| Branch | Contents | Purpose |
|--------|----------|---------|
| `main` | NTRLI' AI Core | Engine: execution, planning, validation, autonomy rules, GitHub runner |
| `ntrli-app` | Application | UI, Android app, product logic - depends on core as submodule |

**Why?** App can't break core - they're isolated.

## Core Components

```
ntrli_ai/
├── control_plane.py    # Single command gate (only EXECUTE allowed)
├── orchestrator.py     # Execution core
├── planner.py          # Plan-first enforcement with JSON schema
├── step_executor.py    # Validated step execution
├── failure_recovery.py # Bounded retry, no silent failure
├── capabilities.py     # Self-knowledge registry
├── knowledge_cache.py  # Offline resilience
├── config.py           # Configuration system
├── cli.py              # CLI interface
├── providers/          # 10 LLM adapters (Groq, Claude, OpenAI, etc.)
├── tools/              # Execution tools (research, code, tests)
├── github/             # GitHub administration
└── notebook/           # Persistent knowledge store
```

## 10 Behavioral Laws

These are not guidelines. They are **structural facts** enforced in code:

1. **No output without a plan** - `planner.py` validates JSON schema
2. **No plan without validation** - `jsonschema.validate()` required
3. **No code without intent** - Plan step must specify purpose
4. **No execution without verification** - Pre-execution checks
5. **No writing without tests** - Code tools include test validation
6. **No hallucination** - LLM outputs are validated, not trusted
7. **No filler** - Empty responses rejected
8. **No goal drift** - Original instruction preserved
9. **No silent failure** - All errors surface with context
10. **No autonomy** - Only EXECUTE command allowed

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Configure
cd ntrli_ai
python cli.py config init

# Set API key
export GROQ_API_KEY=gsk_...

# Run
python main.py "Research Python best practices"
```

## Configuration

```bash
python cli.py config              # Show all
python cli.py config get key      # Get value
python cli.py config set key val  # Set value
python cli.py providers           # List providers
python cli.py providers enable X  # Enable provider
```

## Providers

| Provider | Speed | Accuracy | Cost |
|----------|-------|----------|------|
| Groq | 276 tok/s | Good | $0.59/1M |
| Claude | 45 tok/s | 93.7% | $3-15/1M |
| OpenAI | 60 tok/s | Good | $5-15/1M |
| DeepSeek | 50 tok/s | Good | $0.14/1M |

## GitHub Self-Execution

The core runs autonomously via GitHub Actions:

```yaml
# .github/workflows/ai_guarded.yml
# Triggers: manual, scheduled, issue-labeled
```

## For Applications

**Use the `ntrli-app` branch** for:
- Android app
- Web UI
- CLI tools
- Any product logic

The app branch depends on core as a submodule.

---

See [WHITEPAPER.md](WHITEPAPER.md) for complete specification.
