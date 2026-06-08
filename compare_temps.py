import sys
import argparse

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from openai_in_py.client import (
    build_client,
    chat_with_retry,
    DEFAULT_MAX_TOKENS,
    DEFAULT_SYSTEM,
)

COMPARE_MODEL = "openai/gpt-oss-20b:free"

parser = argparse.ArgumentParser(
    description="Compare OpenRouter model outputs at different temperatures"
)
parser.add_argument("prompt", help="The prompt to send")
parser.add_argument("--model", default=COMPARE_MODEL)
parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
parser.add_argument("--system", default=DEFAULT_SYSTEM)
parser.add_argument(
    "--temps",
    type=float,
    nargs="+",
    default=[0.0, 0.7, 1.5, 2.0],
    help="Temperature values to compare (default: 0.0 0.7 1.5 2.0)",
)
args = parser.parse_args()

client = build_client()

print(f"Model: {args.model}")
print(f"Prompt: {args.prompt}")
print(f"Temperatures: {args.temps}")
print("=" * 60)

for temp in args.temps:
    print(f"\n--- Temperature: {temp} ---\n")
    try:
        reply = chat_with_retry(
            client,
            args.model,
            [
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
