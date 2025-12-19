# NTRLI' AI

**Deterministic, Execution-First Artificial Intelligence System**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

# Set at least one API key
export OPENAI_API_KEY=sk-...
# or
export GROQ_API_KEY=gsk_...

# Run NTRLI' AI
cd ntrli_ai
python main.py "Research Python best practices"
```

## Supported Providers

| Provider | Best For | Pricing |
|----------|----------|---------|
| OpenAI | General purpose | $5-$15/1M tokens |
| Claude | Coding (93.7% accuracy) | $3-$15/1M tokens |
| Gemini | Multimodal, cheapest | $1.25-$7/1M tokens |
| Groq | Speed (276 tok/sec) | $0.59/1M tokens |
| Mistral | European compliance | $2-$8/1M tokens |
| Together | Cost optimization | $0.20-$0.80/1M tokens |
| DeepSeek | Ultra low cost | $0.14/1M tokens |

## Project Structure

```
ntrli_ai/
├── main.py              # Entry point
├── control_plane.py     # Single command gate
├── orchestrator.py      # Execution core
├── planner.py           # Plan-first enforcement
├── step_executor.py     # Step execution
├── capabilities.py      # Self-knowledge
├── providers/           # LLM provider adapters
├── tools/               # Execution tools
└── github/              # GitHub integration
```

## Documentation

- [Whitepaper](WHITEPAPER.md) - Complete specification and reference implementation
- [.env.example](.env.example) - Environment configuration template

## GitHub Actions

Trigger NTRLI' AI via GitHub Actions:

1. Go to Actions → "NTRLI AI Guarded Execution"
2. Click "Run workflow"
3. Enter your instruction
4. Select router strategy (fastest/cheapest/smartest/fallback)

## License

MIT License - See LICENSE for details.
