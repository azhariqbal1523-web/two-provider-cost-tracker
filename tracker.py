
import json
import os
import sys
import time

from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

# Model settings
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Price per 1 million tokens (USD)
GEMINI_INPUT_PRICE = 0.0
GEMINI_OUTPUT_PRICE = 0.0

GROQ_INPUT_PRICE = 0.15
GROQ_OUTPUT_PRICE = 0.60


def calculate_cost(input_tokens, output_tokens, input_price, output_price):
    return (
        input_tokens * input_price / 1_000_000
        + output_tokens * output_price / 1_000_000
    )


def ask_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing from .env")

    client = genai.Client(
    api_key=api_key,
    http_options={"timeout": 30000}
)
    start = time.time()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    seconds = round(time.time() - start, 2)
    usage = response.usage_metadata

    input_tokens = usage.prompt_token_count
    output_tokens = usage.candidates_token_count

    return {
        "provider": "gemini",
        "model": GEMINI_MODEL,
        "reply": response.text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "seconds": seconds,
        "input_price_per_m": GEMINI_INPUT_PRICE,
        "output_price_per_m": GEMINI_OUTPUT_PRICE,
        "cost_usd": calculate_cost(
            input_tokens, output_tokens,
            GEMINI_INPUT_PRICE, GEMINI_OUTPUT_PRICE
        )
    }


def ask_groq(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    client = Groq(api_key=api_key)
    start = time.time()

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    seconds = round(time.time() - start, 2)
    usage = response.usage

    input_tokens = usage.prompt_tokens
    output_tokens = usage.completion_tokens

    return {
        "provider": "groq",
        "model": GROQ_MODEL,
        "reply": response.choices[0].message.content,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "seconds": seconds,
        "input_price_per_m": GROQ_INPUT_PRICE,
        "output_price_per_m": GROQ_OUTPUT_PRICE,
        "cost_usd": calculate_cost(
            input_tokens, output_tokens,
            GROQ_INPUT_PRICE, GROQ_OUTPUT_PRICE
        )
    }


def main():
    if len(sys.argv) < 2:
        print('Usage: uv run tracker.py "Your prompt here"')
        return

    prompt = " ".join(sys.argv[1:])
    results = []

    for provider_function in (ask_gemini, ask_groq):
        try:
            result = provider_function(prompt)
            results.append(result)

            print(f"\n--- {result['provider'].upper()} REPLY ---")
            print(result["reply"])

        except Exception as error:
            print(f"\nError: {error}")

    if results:
        print("\n--- COST COMPARISON ---")
        print(
            f"{'Provider':<12} {'Input':>8} {'Output':>8} "
            f"{'Seconds':>9} {'Cost USD':>12}"
        )

        for result in results:
            print(
                f"{result['provider']:<12} "
                f"{result['input_tokens']:>8} "
                f"{result['output_tokens']:>8} "
                f"{result['seconds']:>9} "
                f"${result['cost_usd']:>11.8f}"
            ) 

        old_results = []

        if os.path.exists("results.json"):
            with open("results.json", "r", encoding="utf-8") as file:
                old_results = json.load(file)

        old_results.extend(results)

        with open("results.json", "w", encoding="utf-8") as file:
            json.dump(old_results, file, indent=4, ensure_ascii=False)

        print("\nResults saved in results.json")

if __name__ == "__main__":
    main()
