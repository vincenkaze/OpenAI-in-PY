import os
import sys
import io
import time
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError, APIStatusError

load_dotenv()

parser = argparse.ArgumentParser(description="OpenRouter Chat REPL")
parser.add_argument("--model", default="openai/gpt-oss-120b:free")
parser.add_argument("--temperature", type=float, default=0.7)
parser.add_argument("--max-tokens", type=int, default=1024)
parser.add_argument("--system", default="You are a helpful assistant.")
args = parser.parse_args()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

MAX_RETRIES = 3

def chat_with_retry(messages, temperature, max_tokens):
    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=args.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except (RateLimitError, APIStatusError) as e:
            if attempt == MAX_RETRIES - 1:
                raise
            retry_after = 30
            if hasattr(e, 'response') and hasattr(e.response, 'headers'):
                retry_after = int(e.response.headers.get('retry-after', 30))
            print(f"\nRate limited. Retrying in {retry_after}s... (attempt {attempt + 1}/{MAX_RETRIES})")
            time.sleep(retry_after)

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

    try:
        reply = chat_with_retry(messages, args.temperature, args.max_tokens)
        print(f"\nAssistant > {reply}\n")
        messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        print(f"\nError: {e}\n")
        messages.pop()
