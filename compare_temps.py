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

parser = argparse.ArgumentParser(description="Compare OpenRouter model outputs at different temperatures")
parser.add_argument("prompt", help="The prompt to send")
parser.add_argument("--model", default="openai/gpt-oss-120b:free")
parser.add_argument("--max-tokens", type=int, default=1024)
parser.add_argument("--system", default="You are a helpful assistant.")
parser.add_argument("--temps", type=float, nargs="+", default=[0.0, 0.7, 1.5, 2.0],
                    help="Temperature values to compare (default: 0.0 0.7 1.5 2.0)")
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

print(f"Model: {args.model}")
print(f"Prompt: {args.prompt}")
print(f"Temperatures: {args.temps}")
print("=" * 60)

for temp in args.temps:
    print(f"\n--- Temperature: {temp} ---\n")
    try:
        reply = chat_with_retry(
            messages=[
                {"role": "system", "content": args.system},
                {"role": "user", "content": args.prompt},
            ],
            temperature=temp,
            max_tokens=args.max_tokens,
        )
        print(reply)
    except Exception as e:
        print(f"Error: {e}")
    print()
