import sys
import argparse

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from openai_in_py.client import (
    build_client,
    chat_with_retry,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    DEFAULT_SYSTEM,
)

MAX_HISTORY = 20

parser = argparse.ArgumentParser(description="OpenRouter Chat REPL")
parser.add_argument("--model", default=DEFAULT_MODEL)
parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
parser.add_argument("--system", default=DEFAULT_SYSTEM)
args = parser.parse_args()

client = build_client()
messages = [{"role": "system", "content": args.system}]

print(f"Model: {args.model}")
print(f"Temperature: {args.temperature}")
print(f"Max tokens: {args.max_tokens}")
print(f"System: {args.system}")
print("-" * 40)
print("Type /quit to exit.\n")

while True:
    try:
        user_input = input("You > ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
        break

    if not user_input:
        continue
    if user_input in ("/quit", "exit"):
        print("Bye!")
        break

    messages.append({"role": "user", "content": user_input})

    if len(messages) > MAX_HISTORY:
        messages = [messages[0]] + [messages[-(MAX_HISTORY - 1):]]

    try:
        reply = chat_with_retry(
            client, args.model, messages, args.temperature, args.max_tokens
        )
        print(f"\nAssistant > {reply}\n")
        messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        print(f"\nError: {e}\n")
        messages.pop()
