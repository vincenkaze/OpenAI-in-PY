import os
import time
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIStatusError

load_dotenv()

DEFAULT_MODEL = "openai/gpt-oss-120b:free"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1024
DEFAULT_SYSTEM = "You are a helpful assistant."
MAX_RETRIES = 3
REQUEST_TIMEOUT = 60


def build_client():
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        timeout=REQUEST_TIMEOUT,
    )


def chat_with_retry(client, model, messages, temperature=DEFAULT_TEMPERATURE, max_tokens=DEFAULT_MAX_TOKENS):
    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except (RateLimitError, APIStatusError) as e:
            if attempt == MAX_RETRIES - 1:
                raise
            retry_after = 30
            if hasattr(e, "response") and hasattr(e.response, "headers"):
                retry_after = int(e.response.headers.get("retry-after", 30))
            print(f"\nRate limited. Retrying in {retry_after}s... (attempt {attempt + 1}/{MAX_RETRIES})")
            time.sleep(retry_after)
