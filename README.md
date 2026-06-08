# OpenAI in Python

A Python project for interacting with LLMs via the OpenAI SDK and OpenRouter's free models. Includes an interactive REPL chat and a temperature comparison tool.

**Project Reference:** [OpenAI API in Python - roadmap.sh](https://roadmap.sh/projects/openai-api-python)

## Project Structure

```
OpenAI in Py/
├── .env                      # API key (not tracked)
├── .gitignore
├── requirements.txt
├── main.py                   # Interactive chat REPL
├── compare_temps.py          # Temperature comparison tool
└── openai_in_py/
    ├── __init__.py
    └── client.py             # Shared client, retry logic, defaults
```

## Prerequisites

- Python 3.9+
- An [OpenRouter](https://openrouter.ai/) account with an API key

## Setup

```powershell
# Clone or download the project
cd "OpenAI in Py"

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-or-v1-your-key-here
```

Get your key from [OpenRouter Settings](https://openrouter.ai/settings/keys).

## Usage

### Interactive Chat (REPL)

```powershell
python main.py
```

```
Model: openai/gpt-oss-120b:free
Temperature: 0.7
Max tokens: 1024
System: You are a helpful assistant.
----------------------------------------
Type /quit to exit.

You > Hello
Assistant > Hi there! How can I help you today?

You > /quit
Bye!
```

#### CLI Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `openai/gpt-oss-120b:free` | OpenRouter model ID |
| `--temperature` | `0.7` | Randomness (0.0 = deterministic, 2.0 = max creative) |
| `--max-tokens` | `1024` | Max response length |
| `--system` | `"You are a helpful assistant."` | System message |

#### Examples

```powershell
# Use a different model
python main.py --model meta-llama/llama-3.3-70b-instruct:free

# Set custom temperature and max tokens
python main.py --temperature 0.3 --max-tokens 512

# Roleplay as a pirate
python main.py --system "You are a pirate. Respond only in pirate speak."
```

---

### Temperature Comparison

```powershell
python compare_temps.py "Tell me a joke in one sentence"
```

> **Note:** The default model (`gpt-oss-20b`) is a standard chat model that respects temperature. Reasoning models like `gpt-oss-120b` ignore temperature and will produce near-identical outputs across values. Free-tier models can be slow — use `--model` to switch if needed.

```
Model: openai/gpt-oss-20b:free
Prompt: Tell me a joke in one sentence
Temperatures: [0.0, 0.7, 1.5, 2.0]
============================================================

--- Temperature: 0.0 ---

Why did the scarecrow win an award? Because he was outstanding in his field!

--- Temperature: 0.7 ---

Why did the scarecrow become a motivational speaker? Because he was outstanding in his field!

--- Temperature: 1.5 ---

What do you call a fake noodle? An impasta!

--- Temperature: 2.0 ---

Why did the scarecrow win an award? Because he was outstanding in his field.
```

#### CLI Flags

| Flag | Default | Description |
|------|---------|-------------|
| `prompt` (required) | — | The prompt to send |
| `--model` | `openai/gpt-oss-20b:free` | OpenRouter model ID |
| `--max-tokens` | `1024` | Max response length |
| `--system` | `"You are a helpful assistant."` | System message |
| `--temps` | `0.0 0.7 1.5 2.0` | Space-separated temperature values |

#### Examples

```powershell
# Custom temperatures
python compare_temps.py "Write a haiku about coding" --temps 0.0 0.5 1.0 1.5 2.0

# Different model
python compare_temps.py "Explain quantum physics" --model meta-llama/llama-3.3-70b-instruct:free
```

---

## Available Free Models

All models below cost $0 on OpenRouter:

| Model ID | Size | Best For |
|----------|------|----------|
| `openai/gpt-oss-120b:free` | 117B MoE | General purpose (default) |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | 550B MoE | Complex reasoning |
| `qwen/qwen3-coder:free` | 480B MoE | Code generation |
| `qwen/qwen3-next-80b-a3b-instruct:free` | 80B MoE | Chat |
| `meta-llama/llama-3.3-70b-instruct:free` | 70B | General purpose |
| `openai/gpt-oss-20b:free` | 21B MoE | Fast responses |
| `openrouter/free` | — | Auto-routes to any free model |

Full list: [openrouter.ai/models](https://openrouter.ai/models?max_price=0)

---

## How It Works

1. **OpenAI SDK** — The project uses the official `openai` Python package
2. **OpenRouter routing** — Requests are sent to OpenRouter's API (`https://openrouter.ai/api/v1`) which routes to the chosen model provider
3. **Shared client** — `openai_in_py/client.py` provides `build_client()` and `chat_with_retry()` used by both scripts
4. **Environment variables** — The API key is loaded from `.env` via `python-dotenv`
5. **Retry logic** — Free models are rate-limited. Both scripts automatically retry up to 3 times with the provider's suggested wait time
6. **History capping** — The REPL limits conversation history to 20 messages to avoid token limits
7. **Request timeout** — 60-second timeout prevents hanging on slow free-tier responses

### Package Architecture

```
openai_in_py/client.py
├── build_client()          → OpenAI client configured for OpenRouter
├── chat_with_retry()       → API call with automatic retry on 429
├── DEFAULT_MODEL           → "openai/gpt-oss-120b:free"
├── DEFAULT_TEMPERATURE     → 0.7
├── DEFAULT_MAX_TOKENS      → 1024
├── DEFAULT_SYSTEM          → "You are a helpful assistant."
├── MAX_RETRIES             → 3
└── REQUEST_TIMEOUT         → 60
```

## API Key Safety

The `.env` file is included in `.gitignore` and will not be committed. Never share your API key publicly.

## License

This project is for educational purposes.
