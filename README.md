# NTRLI' AI Core

**Deterministic, Execution-First Artificial Intelligence Engine**

This is the **core engine** of NTRLI' AI - the execution system that enforces the 10 Behavioral Laws.

## What This Is

The core contains:
- **Execution Engine** - Plan-first, validate-always execution
- **Planning System** - JSON schema-validated planning
- **Validation Gates** - Capability checks, code validation
- **Autonomy Rules** - The 10 non-negotiable behavioral laws
- **GitHub Runner** - Self-running AI execution workflow
- **Multi-Provider Router** - 10+ LLM providers with intelligent routing

## Behavioral Laws (Enforced in Code)

1. No output without a plan
2. No plan without validation
3. No code without intent
4. No execution without verification
5. No writing to GitHub without tests
6. No hallucination
7. No filler
8. No goal drift
9. No silent failure
10. No autonomy

## Structure

```
ntrli_ai/
├── main.py              # Entry point
├── control_plane.py     # Single EXECUTE command gate
├── orchestrator.py      # Execution core
├── planner.py           # Plan-first enforcement
├── step_executor.py     # Sequential step execution
├── capabilities.py      # Self-knowledge registry
├── failure_recovery.py  # Retry logic
├── knowledge_cache.py   # Offline resilience
├── config.py            # Configuration system
├── cli.py               # CLI interface
├── providers/           # LLM provider adapters
├── tools/               # Execution tools
├── github/              # GitHub integration
└── notebook/            # Knowledge storage
```

## Usage

```bash
# Install
pip install -r requirements.txt

# Configure
export GROQ_API_KEY=gsk_...  # or any provider key

# Run
cd ntrli_ai
python main.py "Your instruction here"
```

## For Applications

Applications should use this core as a **git submodule**:

```bash
git submodule add https://github.com/YOUR_ORG/ntrli_ai_II.git core
```

Then import from `core/ntrli_ai/`.

## Documentation

See [WHITEPAPER.md](WHITEPAPER.md) for complete specification.

## GitHub Actions

The core includes a self-running AI workflow:
- Manual trigger with instruction input
- Scheduled daily maintenance
- Issue-triggered execution (`ai-task` label)
- Auto-retry on failure
